from collections import defaultdict
from typing import Callable
from ..database.db_interface import DBInterface
from ..queryservices.service_controller import ServiceController
import concurrent.futures
import threading
import time

class FileIndexer(object):
    """
    Monitors changes in the file system and updates the vector database accordingly.

    Args:
        db_config (dict): Keyword arguments for the DBInterface object.
        svc_config (dict): Keyword arguments for the ServiceController object.
        fs_config (dict): Keyword arguments for file system specs. Typically includes the list of directories to monitor.
        indexer_config (dict): Keyword arguments, for FileIndexer operation, e.g. check_interval for monitoring changes.
        
    Returns: 
        FileIndexer object
    """
    def __init__(self, db_config: dict = {}, svc_config: dict = {}, fs_config: dict = {}, indexer_config: dict = {}, **kwargs):
        self.dbi = DBInterface(**db_config, **kwargs)
        self.svc = ServiceController(**svc_config)
        self.fs_config = fs_config
        self.indexer_config = indexer_config
        
        # Search Index callbacks
        self.callbacks = []
        self._register_callback(self.dbi.update_collection)
        
        # Database Interface thread handling
        self._db_ready_event = threading.Event()
        
        self.start_db_thread = threading.Thread(target=self._start_db)
        self.start_db_thread.setDaemon(True)
        self.start_db_thread.start()
    
    def _register_callback(self, callback: Callable):
        self.callbacks.append(callback)
        
    def _start_db(self):
        """
        Update vector database during application start
        """
        # Wait until service is running
        while not self.svc.is_service_running():
            time.sleep(1)
        
        db_state = self.dbi.get_collection_metadata()
        self.current_dbState = self.svc.get_current_state(**self.fs_config)
        
        changes = self._detect_changes(db_state, self.current_dbState)
        
        if changes:
            for callback in self.callbacks:
                callback(changes)
        
        self._db_ready_event.set()
        self.start_monitoring()
        
    @property
    def db_ready(self):
        """
        Check if the database is ready.

        Returns:
            bool: True if the database is ready, False otherwise.
        """
        return self._db_ready_event.is_set()
        
    
    def _detect_changes(self, old_state: dict, new_state: dict):
        """Detect changes between two states.

        Args:
            old_state (dict): Previous state of the file system
            new_state (dict): Current state of the file system
        """
        def compare_states(path_item):
            if isinstance(path_item, tuple):
                path, item = path_item
                
                if path not in old_state['data']:
                    return {'ChangeType': 'Added', 'path': path,**item}
                elif old_state['data'][path]['date_modified'] != item['date_modified']:
                    return {'ChangeType': 'Modified', 'path': path,**item}
            elif isinstance(path_item, str):
                if path_item not in new_state['data']:
                    return {'ChangeType': 'Deleted', 'path': path_item}
            
            return None
    
        def process_result(result):
            if result:
                change_type = result.pop('ChangeType')
                if change_type == "Deleted":
                    return (change_type, result['path'])
                else:
                    return (change_type, result)
            return None
            
        tasks = list(old_state['data'].keys()) + list(new_state['data'].items())
        
        changes = defaultdict(list)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(compare_states, tasks)
            processed_results = executor.map(process_result, results)
            
            for result in processed_results:
                if result:
                    change_type, value = result
                    changes[change_type].append(value)
        
        return changes
    
    def detect_changes(self):
        """
        Detect changes between the previous state of the database and the current state of the file system.

        Returns:
            list: List of changes detected.
        """
        new_state = self.svc.get_current_state(**self.fs_config)
        
        changes = self._detect_changes(self.current_dbState, new_state)
        
        self.current_dbState = new_state
        
        return changes
    
    def _start_monitor(self):
        """
        Monitor table for changes and call registered callbacks when changes are detected.
        """
        self._db_ready_event.wait()
        self.current_dbState = self.svc.get_current_state(**self.fs_config)
        while not self.stop_event.is_set():
            changes = self.detect_changes()
            if changes:
                for callback in self.callbacks:
                    callback(changes)
            self.stop_event.wait(self.indexer_config.get("check_interval",30))
        
    def start_monitoring(self):
        """
        Start monitoring the Search Index for changes in a separate thread.
        """
        self.monitor_thread = threading.Thread(target=self._start_monitor)
        self.monitor_thread.setDaemon(True)
        self.stop_event = threading.Event()
        self.monitor_thread.start()
        
    def stop_monitoring(self):
        """
        Stop monitoring the Search Index for changes.
        """
        self.stop_event.set()
        self.monitor_thread.join()
        
    def close(self):
        """
        Close the database connection and stop monitoring.

        This method is used to properly shut down the FileIndexer object by stopping the monitoring thread and waiting for the database thread to finish.

        Returns:
            None
        """
        self.stop_monitoring()
        self.start_db_thread.join()
        
        
    def search(self, query, user_question, userPromptClass="Other"):
        """
        Returns context to answer the user's question

        This method identifies if the query is valid SQL (osquery-compatible) or not. Depending on this, it either runs a database query or queries the vector database directly. The results are then returned as a dictionary.

        Args:
            query (str): The search query to match against.
            user_question (str): The question being asked by the user.

        Returns:
            dict: A dictionary containing the data source, context, and error if any.
        """
        
        output = defaultdict(dict)
        
        if userPromptClass.lower() == "other":
            # Directly query the vector database without running SQL query
            try:
                dbi_response = self.dbi.query_collection(query=user_question)
                output.update({"dbi": dbi_response})
            except Exception as e:
                output.update({"dbi": {"error": f"Failed to query database: {e}", "db_context": ""}})
            
            return output
        else:
            svc_response = self.svc.run_query(query)
            
            if svc_response.get("error"):
                if "Error code" not in svc_response['error']:
                    output.update({"svc":svc_response})
                else:
                    dbi_response = self.dbi.query_collection(query=user_question)
                    output.update({"svc": svc_response, "dbi": dbi_response})
            else:
                # If no error from SVC service, query database    
                try:    
                    dbi_response = self.dbi.query_collection(query=user_question, file_filter=svc_response if 'path' in svc_response['data'].keys() else None)
                    output.update({"svc": svc_response, "dbi": dbi_response})
                except Exception as e:
                    dbi_response = self.dbi.query_collection(query=user_question)
                    output.update({"svc": svc_response,"dbi": {"error":f"Failed to query database: {e}"}})
            
            return output
            
        
        # if query.lower().startswith("select"):
        #     # Run the SQL query and handle errors
        #     response = self.svc.run_query(query)
        #     if response.get('error'):
        #         if "Error code" not in response['error']:
        #             output.update({"error": response["error"]})
        #         else:
        #             context = self.dbi.query_collection(query=user_question)
        #             output.update({"context": context, "error": response["error"]})
        #     else:
        #         try:
        #             print("Here1")
        #             context = self.dbi.query_collection(query=user_question, file_filter=response if 'path' in response['data'].keys() else None)
        #             output.update({"context": context, "svc_response": response})
        #         except Exception as e:
        #             context = self.dbi.query_collection(query=user_question)
        #             output.update({"error": "Failed to query database: {e}", "svc_response": response,"context": context})
        # else:
        #     try:
        #         context = self.dbi.query_collection(query=user_question)
        #         output.update({"context": context})
        #         print("Here2")
        #     except Exception as e:
        #         output.update({"error": f"Failed to query database: {e}", "context": ""})
            
        
        # return output
        