
import os
from operator import itemgetter
import json
import logging
import sqlite3
import pathlib
from collections import defaultdict
from typing import Callable, List, Dict
import threading
from tqdm import tqdm

import adodbapi as OleDb
import chromadb
from langchain_text_splitters import MarkdownTextSplitter, RecursiveCharacterTextSplitter

from . import constants
from .parse import parse_file_contents
from .util import create_init_config, is_sql_query, format_sqlrows_to_text, format_sqlrows_to_dict, flatten
from .embedding_model import EmbeddingModelFunction


import logging
logger = logging.getLogger(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__name__))

# Windows Search Indexer
class WindowsFileIndexer:
    def __init__(self, vector_db_path: str = "better_search_content_db", check_interval: int = 30, device: str = "cpu", **kwargs):
        """
        Initialize the WindowsFileIndexer with vector database path, check interval, and device.

        Args:
            vector_db_path (str): Path to the vector database.
            check_interval (int): Interval (in seconds) to check for file changes.
            device (str): Device to run the vector database operations on (e.g., 'cpu', 'cuda').
            **kwargs: Additional keyword arguments for the VectorDB initialization.
        """
        self.conn = OleDb.connect(constants.WIN_CONN_STRING)
        self.vector_db = VectorDB(vector_db_path=os.path.join(BASE_DIR, vector_db_path), device=device, **kwargs)
        self.check_interval = check_interval
        self.last_check = None
        
        self.callbacks = [self.vector_db.update_collection]
        self.current_state = {}
        
        self._db_ready_event = threading.Event()
        
        self.start_db_thread = threading.Thread(target=self.start_db)
        self.start_db_thread.setDaemon(True)
        self.start_db_thread.start()
        
    def register_callback(self, callback: Callable[[List[Dict]], None]):
        """
        Register callback function to be called when changes are detected.

        Args:
            callback (Callable[[List[Dict]], None]): Callback function that takes a list of changed rows as argument.
        """
        self.callbacks.append(callback)
        
    def start_db(self):
        """
        Update vector database during the start of the application.
        """
        vector_files = {k['path']: itemgetter("path", "date_modified")(defaultdict(str, k)) for k in self.vector_db.collection.get(include=['metadatas']).get('metadatas')}
        
        self.current_state = self.get_current_state(order_type="size")
        
        changes = []
        
        for path in self.current_state.keys():
            if path not in self.current_state:
                changes.append({'ChangeType': 'Deleted', **self.current_state[path]})
        
        # Detect additions and modifications
        for path, item in self.current_state.items():
            if path not in vector_files:
                changes.append({'ChangeType': 'Added', **item})
            elif self.current_state[path] != item:
                changes.append({'ChangeType': 'Modified', **item})
        
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
    
    @property
    def table_info(self):
        """
        Get table metadata information.

        Returns:
            dict: Metadata information of the table.
        """
        return constants.WIN_SYSTEMINDEX_TABLE_METADATA
    
    def get_current_state(self, columns=["path","date_modified"],order_type="date_modified"):
        """
        Get current state of the table.

        Args:
            columns (list): List of columns to retrieve.
            order_type (str): Column to order the results by.

        Returns:
            dict: Item path and item details.
        """
        query = ("""SELECT {}, {} FROM "SystemIndex" WHERE WorkId IS NOT NULL AND scope='file:' AND Contains(System.ItemType, '{}') ORDER BY {} DESC""".format(*itemgetter(*columns)(constants.WIN_COLS_TO_SYSINDEX),'" OR "'.join(constants.parsable_exts.get('mupdf')), constants.WIN_COLS_TO_SYSINDEX.get(order_type))
        )
        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            result = format_sqlrows_to_dict(result, cursor.get_description())
        return result
    
    def detect_changes(self):
        """
        Detect changes in the current state of the table.

        Returns:
            list: List of changes detected.
        """
        new_state = self.get_current_state()
        changes = []
        
        # Detect deletions
        for path in self.current_state.keys():
            if path not in new_state:
                changes.append({'ChangeType': 'Deleted', **self.current_state[path]})
        
        # Detect additions and modifications
        for path, item in new_state.items():
            if path not in self.current_state:
                changes.append({'ChangeType': 'Added', **item})
            elif self.current_state[path] != item:
                changes.append({'ChangeType': 'Modified', **item})
        
        self.current_state = new_state
        return changes
    
    def _run_monitor(self):
        """
        Monitor table for changes and call registered callbacks when changes are detected.
        """
        self._db_ready_event.wait()
        self.current_state = self.get_current_state()
        while not self.stop_event.is_set():
            changes = self.detect_changes()
            if changes:
                for callback in self.callbacks:
                    callback(changes)
            self.stop_event.wait(self.check_interval)
            
    def start_monitoring(self):
        """
        Start monitoring the Search Index for changes in a separate thread.
        """
        self.monitor_thread = threading.Thread(target=self._run_monitor)
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
        """
        self.stop_monitoring()
        self.conn.close()
        self.start_db_thread.join()
    
    def query(self, query, user_question):
        """
        Query the databases and return context that can help answer the user's question.

        Args:
            query (str): Generated SQL query.
            user_question (str): Question posed by the user.

        Returns:
            str: Context for the next generation step - from vector database or search index.
        """
        answer_preface = ""
        if any(fail in query.lower() for fail in ["i don't know", "i do not know"]):
            query_context, answer_preface = self.vector_db.query_collection(query=user_question), "I was able to check file contents for this.\n\n "
        elif is_sql_query(query):
            with self.conn:
                cursor = self.conn.cursor()
                try: 
                    cursor.execute(query)
                    result = cursor.fetchall()
                    if len(result) < 1:
                        query_context, answer_preface = self.vector_db.query_collection(query=user_question), "I was unable to query search index, the following answer may be incorrect.\n\n" 
                    else:
                        query_context, answer_preface = format_sqlrows_to_text(result, cursor.get_description()), "I was able to query search index.\n\n"
                except:
                    query_context, answer_preface = self.vector_db.query_collection(query=user_question), "I was unable to query search index, the following answer may be incorrect.\n\n"
        else:
            query_context=""
        
        return query_context, answer_preface
    

# Vector Database Class
class VectorDB:
    def __init__(self, 
                 vector_db_path: str = "better_search_content_db", 
                 embedding_model_name: str = "Alibaba-NLP/gte-base-en-v1.5", 
                 chunk_size: int = 500, chunk_overlap: int = 200, top_k: int = 5, 
                 chunk_batch_size: int = 500, cache_dir: str = None, device: str = "cpu",
                 **kwargs
                 ):
        """
        Initialize the VectorDB with configuration settings.

        Args:
            vector_db_path (str): Path to the vector database.
            embedding_model_name (str): Name of the embedding model to use.
            chunk_size (int): Size of chunks to split documents into.
            chunk_overlap (int): Overlap between chunks.
            top_k (int): Number of top results to retrieve for queries.
            batch_size (int): Batch size for adding/updating documents.
            cache_dir (str): Directory to cache model files.
            device (str): Device to run the model on (e.g., 'cpu', 'cuda').
            **kwargs: Additional keyword arguments.
        """
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model_name
        self.cache_dir = cache_dir
        self.embedding_model_fn = EmbeddingModelFunction(
            model_name=self.embedding_model_name,
            cache_dir=self.cache_dir,
            device=device
        )
        
        self.db = chromadb.PersistentClient(
            path=vector_db_path, 
            settings=chromadb.config.Settings(),   
        )
        
        self.collection = self.db.get_or_create_collection(
            name="file-content",
            embedding_function=self.embedding_model_fn,
        )
        
        self._top_k = top_k
        self.batch_size = chunk_batch_size
    
    @property
    def top_k(self):
        """
        Get the number of top results to retrieve for queries.

        Returns:
            int: Number of top results.
        """
        return self._top_k    
    
    @top_k.setter
    def top_k(self, value):
        """
        Set the number of top results to retrieve for queries.

        Args:
            value (int): Number of top results.
        """
        self._top_k = value
        
    def _create_docs_for_db(self, file_path=None, date_modified=None):
        """
        Create documents for the database from a file.

        Args:
            file_path (str): Path to the file.
            date_modified (str): Date the file was last modified.

        Returns:
            dict: Documents, metadata, and IDs.
            int: Number of documents created.
        """
        content = parse_file_contents(file_path)
        _, (_, ext) = os.path.basename(os.path.dirname(file_path)), os.path.splitext(os.path.basename(file_path))
        if isinstance(content, str):
            if pathlib.Path(file_path).suffix in constants.parsable_exts.get("mupdf"):
                splitter = MarkdownTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            
            elif pathlib.Path(file_path).suffix in constants.parsable_exts.get("text"):
                splitter = RecursiveCharacterTextSplitter(chunk_size=self.chunk_size, chunk_overlap=self.chunk_overlap)
            
            docs = [doc.page_content for doc in splitter.create_documents([content])]
            metadatas = [{"path": f"{file_path}", "fileext": f"{ext}", "date_modified": str(date_modified)} for _ in range(len(docs))]
            ids = [f"{file_path}_{i+1}" for i in range(len(docs))]
            return {"documents": docs, "metadatas": metadatas, "ids": ids}, len(docs)
        else:
            return None,None
    
    def add_to_collection(self, file_path=None,date_modified=None):
        """
        Add a file to the vector database collection.

        Args:
            file_path (str): Path to the file.
            date_modified (str): Date the file was last modified.
        """
        try:
            data, num_docs = self._create_docs_for_db(file_path=file_path, date_modified=date_modified)
            if num_docs:
                for i in range(0, num_docs, self.batch_size):
                    self.collection.add(
                        documents=data.get("documents")[i:i+self.batch_size],
                        metadatas=data.get("metadatas")[i:i+self.batch_size],
                        ids=data.get("ids")[i:i+self.batch_size],
                    )
        except Exception as e:
            logger.error(f"File failed: {file_path}")
            logger.exception(e)
            pass
    
    def update_to_collection(self, file_path=None, date_modified=None):
        """
        Update a file in the vector database collection.

        Args:
            file_path (str): Path to the file.
            date_modified (str): Date the file was last modified.
        """
        try:
            data, num_docs = self._create_docs_for_db(file_path=file_path, date_modified=date_modified)
            if num_docs:
                for i in range(0, num_docs, self.batch_size):
                    self.collection.update(
                        documents=data.get("documents")[i:i+self.batch_size],
                        metadatas=data.get("metadatas")[i:i+self.batch_size],
                        ids=data.get("ids")[i:i+self.batch_size],
                    )
        except Exception as e:
            logger.error(f"File failed: {file_path}")
            logger.exception(e)
            pass
    
    def delete_from_collection(self, file_path=None):
        """
        Delete a file from the vector database collection.

        Args:
            file_path (str): Path to the file.
        """
        self.collection.delete(
            where={"path": file_path}
        )
    
    def update_collection(self, change_list):
        """
        Update the vector database collection based on a list of changes.

        Args:
            change_list (list): List of changes detected.
        """
        for change in tqdm(change_list):
            change_type, file_path, date_modified = itemgetter("ChangeType","path","date_modified")(change)
            if change_type == 'Deleted':
                self.delete_from_collection(file_path=file_path)
            elif change_type == 'Added':
                self.add_to_collection(file_path=file_path, date_modified=date_modified)
            elif change_type == 'Modified':
                self.update_to_collection(file_path=file_path, date_modified=date_modified)
            else:
                # Change type is not defined
                pass
            
    def query_collection(self, query):
        """
        Query the vector database collection.

        Args:
            query (str): Query text.

        Returns:
            list: Query results.
        """
        docs = self.collection.query(
            query_texts=[query],
            n_results=self.top_k
        ).get('documents')[0]
        return "\n\n".join(str(x) for x in flatten(docs))
        

# WIP - Linux Search Indexer (custom) 
class LinuxFileIndexer:
    def __init__(self, db_name="better_search_index.db", vector_db_path="better_search_content.db",config_file="./config.json", log_file="indexer.log", **kwargs):
        # Setup logging
        logging.basicConfig(filename=log_file,format="%(asctime)s %(message)s",filemode='a')
        
        if not os.path.isfile(db_name):
            logger.info("Index not found, creating...")
        
        # Connect to database and enable foreign keys    
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = 1")
        
        self.config_file = config_file
        
        self.load_config()
        self.__create_tables()
    
    def save_config(self): 
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, sort_keys=True, indent=4)
            
    def load_config(self):
        if not os.path.isfile(self.config_file):
            self.config = create_init_config()
            self.save_config()
        else:
            # Load config
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
    
    def query(self, query):
        with self.conn:
            cursor = self.conn.cursor()
            cursor.executescript(query)
            result = cursor.fetchall()
        return result

    def __create_tables(self):
        with self.conn:
            # Create tables
            self.conn.executescript(f"""
                {constants.file_metadata_create};
                {constants.content_index_create};
                {constants.image_metadata_create};
                {constants.video_metadata_create};
                {constants.music_metadata_create};
                {constants.email_metadata_create};
                {constants.application_metadata_create};
                {constants.index_maintenance_create};
            """)
    
    def add_file(self, file_path):
        abs_file_path = os.path.abspath(file_path)
        if not os.path.isfile(abs_file_path):
            logger.error(f"File not found: {abs_file_path}")
            return
        
        
        file_stats = os.stat(abs_file_path)
        file_name = os.path.basename(abs_file_path)
        file_size = file_stats.st_size
        date_created = file_stats.st_ctime
        date_modified = file_stats.st_mtime
        date_accessed=  file_stats.st_atime
        
        content = parse_file_contents(abs_file_path)
        
        with self.conn:
            cursor = self.conn.cursor()
            # Update records
            cursor.execute(
                """
                INSERT OR IGNORE INTO file_metadata(
                    file_path, file_name, file_size, date_created, date_modified, date_accessed   
                ) VALUES (?, ?, ?, ?, ?, ?)
                """, (abs_file_path, file_name, file_size, date_created, date_modified, date_accessed)
            )
            file_id = cursor.lastrowid
            
            if isinstance(content, str):
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO content_index (
                        file_id, content
                    ) VALUES (?, ?)
                    """, (file_id, content)
                )
            elif isinstance(content, defaultdict):
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO image_metadata (
                        file_id, dimensions, camera_model, date_taken, gps_coordinates 
                    ) VALUES (?, ?, ?, ?, ?)
                    """, (file_id, content.get('dimensions'), content.get('camera_model'), content.get('date_taken'), content.get('gps_coordinates'))
                )
            elif isinstance(content, tuple):
                video_metadata, music_metadata = content
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO video_metadata (
                        file_id, title, duration, frame_rate, dimensions, director
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (file_id, video_metadata.get('title'), video_metadata.get('duration'), video_metadata.get('frame_rate'), video_metadata.get('dimensions'), video_metadata.get('director'))
                )
                cursor.execute(
                    """
                    INSERT OR REPLACE INTO music_metadata (
                        file_id, title, album, artist, genre, duration
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    """, (file_id, music_metadata.get('title'), music_metadata.get('album'), music_metadata.get('artist'), music_metadata.get('genre'), music_metadata.get('duration'))
                )
            elif isinstance(content, None):
                # No content to parse
                pass
                
            self.conn.commit()

    def update_file(self, file_path):
        abs_file_path = os.path.abspath(file_path)
        if not os.path.isfile(abs_file_path):
            logger.error(f"File not found: {abs_file_path}")
            return
        
        file_stat = os.stat(abs_file_path)
        file_size = file_stat.st_size
        date_modified = file_stat.st_mtime
        date_accessed = file_stat.st_atime

        content = parse_file_contents(abs_file_path)

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE file_metadata
                SET file_size = ?, date_modified = ?, date_accessed = ?
                WHERE file_path = ?
            ''', (file_size, date_modified, date_accessed, abs_file_path))
            
            if isinstance(content, str):
                cursor.execute('''
                    UPDATE content_index
                    SET content = ?
                    WHERE file_id = (SELECT file_id FROM file_metadata WHERE file_path = ?)
                ''', (content, abs_file_path))
            elif isinstance(content, defaultdict):
                cursor.execute(
                    """
                    UPDATE content_index
                    SET dimensions = ?, camera_model = ?, date_taken = ?, gps_coordinates = ? 
                    WHERE file_id = (SELECT file_id from file_metadata WHERE file_path = ?)
                    """, (content.get('dimensions'), content.get('camera_model'), content.get('date_taken'), content.get('gps_coordinates'), abs_file_path)
                )
            elif isinstance(content, tuple):
                video_metadata, music_metadata = content
                cursor.execute(
                    """
                    UPDATE video_metadata
                    SET title = ?, duration = ?, frame_rate = ?, dimensions = ?, director = ?
                    WHERE file_id = (SELECT file_id from file_metadata WHERE file_path = ?)
                    """, (video_metadata.get('title'), video_metadata.get('duration'), video_metadata.get('frame_rate'), video_metadata.get('dimensions'), video_metadata.get('director'), abs_file_path)
                )
                cursor.execute(
                    """
                    UPDATE music_metadata
                    SET title = ?, album = ?, artist = ?, genre = ?, duration = ?
                    WHERE file_id = (SELECT file_id from file_metadata WHERE file_path = ?)
                    """, (music_metadata.get('title'), music_metadata.get('album'), music_metadata.get('artist'), music_metadata.get('genre'), music_metadata.get('duration'), abs_file_path)
                )
            elif isinstance(content, None):
                # No content to update
                pass

            self.conn.commit()
            
    def list_all_files(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT file_path from file_metadata')
        return [row[0] for row in cursor.fetchall()]
                 
    def delete_file(self, file_path):
        abs_file_path = os.path.abspath(file_path)
        with self.conn:
            self.conn.execute(
                """
                DELETE FROM file_metadata WHERE file_path = ?
                """, (abs_file_path,)
            )
    
    def close(self):
        self.conn.close()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()


# WIP - OSX Search Indexer
class OSXFileIndexer:
    pass
    
