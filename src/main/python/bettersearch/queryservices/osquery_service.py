"""
To get all available tables on current platform in osquery:
- select distinct name from osquery_registry where registry = 'table' and active = true and internal = false
"""

from .base_service import BaseQueryService
import osquery
import pywintypes
import threading
import platform
from ..database.constants import parsable_exts
from collections import defaultdict

class OSQueryService(BaseQueryService):
    """
    A query service class for interacting with osquery.

    This class provides a way to run SQL queries on a local device using osquery.
    It initializes an instance of the osquery service and opens a connection to it.

    See Also:
        https://osquery.readthedocs.io/en/stable/ for more information on osquery.
    """
    def __init__(self, **kwargs):
        """
        Initialize query service for osquery (local device management).
        """
        
        super().__init__()
        self.instance = osquery.SpawnInstance(path=kwargs.get("path",None))
        self.instance.open()
        
        # For thread-safe stop
        self._stop_lock = threading.Lock()
        
    def _get_current_state(self, **kwargs) -> defaultdict:
        """
        Get the current file state from osquery tables [Windows Search, MDFind, File].

        Args:
            **kwargs: Additional keyword arguments

        Returns:
            defaultdict: Item path and item details.
        """
        system = platform.system().lower()
        file_cols = ", ".join(f"f.{col}" for col in kwargs.get("file_cols", []))
        max_results = kwargs.get("max_results")
        order_col = kwargs.get("order_col", "date_modified" if system == "windows" else "size")
        folder_path_filter = " OR ".join(f"'{path}'" for path in kwargs.get("folders", []))
        file_type_filter = " OR ".join(ftype.lstrip(".") for ftype in parsable_exts.get('docling'))
        
        system_queries = {
            "windows": {
                "table": "windows_search",
                "table_short": "ws",
                "table_cols": ["path","date_modified"],
                "join_table": "file",
                "join_table_short": "f",
                "join_condition": "ws.path = f.path",
                "query_filter": f"query=\"in:({folder_path_filter}) type:({file_type_filter})\" and max_results=-1",
                "order_by": f"{order_col} desc",
                "limit": max_results,
            },
            "darwin": {
                "table": "mdfind",
                "table_short": "mdfs",
                "table_cols": ["path"],
                "join_table": "file",
                "join_table_short": "f",
                "join_condition": "mdfs.path = f.path",
                "query_filter": f"mdfs.query={file_type_filter} and ({folder_path_filter})",
                "order_by": f"{order_col} desc",
                "limit": max_results,
            }
        }
        
        if system not in system_queries.keys():
            return {"error": f"Unsupported platform: {system}"}
            
        
        query_params = system_queries[system]
        table_cols = ", ".join(f"{query_params['table_short']}.{col}" for col in query_params["table_cols"]) or "*"
        query = f'''select {file_cols}, {table_cols} from {query_params["table"]} as {query_params["table_short"]} join {query_params["join_table"]} as {query_params["join_table_short"]} on {query_params["join_condition"]} where {query_params["query_filter"]} order by {query_params["order_by"]}''' 
        if query_params["limit"]:
            query += f" limit {query_params['limit']}"
        
        return self.run_query(query, **kwargs)
        

    def run_query(self, query, **kwargs) -> defaultdict:
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device
        
        Returns:
            response (dict|obj): Query results
        """
        try:
            result = self.instance.client.query(query)
            if result.status.code != 0:
                return {"error": f"Error code {result.status.code}: {result.status.message}"}
            
            formatted_response = defaultdict(lambda: {})
            for i,item in enumerate(result.response):
                if 'path' in item.keys():
                    path = item.pop('path')
                    formatted_response[path].update(item)
                else:
                    formatted_response[f'data_{i}'].update(item)
            return {"data": formatted_response}
        except Exception as e:
            return {"error": f"Failed to execute query on osquery database: {e}"}
        

    def stop(self):
        """
        Stop the OSQueryService instance.

        This is a thread-safe method. It should be called when the service is no longer needed to free up system resources.
        """
        with self._stop_lock:     
            try:
                self.instance.__del__()
            except pywintypes.error as e:
                # To handle osquery issue https://github.com/osquery/osquery-python/issues/57
                if e.args[2] == "Incorrect function.":
                    import win32file
                    win32file.CloseHandle(self.instance.connection._transport._TBufferedTransport__trans._handle)
                    self.instance.connection._transport._TBufferedTransport__trans._handle = None
                    self.instance.__del__()
                