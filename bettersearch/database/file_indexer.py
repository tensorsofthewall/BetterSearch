import sqlite3
import os
import logging
import constants as constants
import pathlib
from parse import parse_file



class FileIndexer:
    def __init__(self, db_name="better_search_index.db", folders=[''], log_file="indexer.log"):
        # Setup logging
        logging.basicConfig(filename=log_file,format="%(asctime)s %(message)s",filemode='a')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        if not os.path.isfile(db_name):
            self.logger.info("Index not found, creating...")
        
        # Connect to database and enable foreign keys    
        self.conn = sqlite3.connect(db_name)
        self.conn.execute("PRAGMA foreign_keys = 1")
        
        self.create_tables()
    
    def create_tables(self):
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
            logging.ERROR(f"File not found: {abs_file_path}")
            return
        
        
        file_stats = os.stat(abs_file_path)
        file_name = os.path.basename(abs_file_path)
        file_size = file_stats.st_size
        date_created = file_stats.st_ctime
        date_modified = file_stats.st_mtime
        date_accessed=  file_stats.st_atime
        
        
        content = parse_file(abs_file_path)
        
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
            
            cursor.execute(
                """
                INSERT OR REPLACE INTO content_index (
                    file_id, content
                ) VALUES (?, ?)
                """, (file_id, content)
            )
            
            self.conn.commit()
            
        
    def update_file(self, file_path):
        abs_file_path = os.path.abspath(file_path)
        if not os.path.isfile(abs_file_path):
            logging.ERROR(f"File not found: {abs_file_path}")
            return
        
        file_stat = os.stat(abs_file_path)
        file_size = file_stat.st_size
        date_modified = file_stat.st_mtime
        date_accessed = file_stat.st_atime

        content = parse_file(abs_file_path)

        with self.conn:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE file_metadata
                SET file_size = ?, date_modified = ?, date_accessed = ?
                WHERE file_path = ?
            ''', (file_size, date_modified, date_accessed, abs_file_path))

            cursor.execute('''
                UPDATE content_index
                SET content = ?
                WHERE file_id = (SELECT file_id FROM file_metadata WHERE file_path = ?)
            ''', (content, abs_file_path))
            
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
        for handler in self.log.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        
        

