import sqlite3
import os
import logging
from collections import defaultdict
import json
from . import constants
from .parse import parse_file_contents
from .util import create_init_config


# Required Only for Linux (Use Windows Search Index for Windows)
class LinuxFileIndexer:
    def __init__(self, db_name="better_search_index.db", config_file="./config.json", log_file="indexer.log"):
        # Setup logging
        logging.basicConfig(filename=log_file,format="%(asctime)s %(message)s",filemode='a')
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        
        if not os.path.isfile(db_name):
            self.logger.info("Index not found, creating...")
        
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
            self.logger.error(f"File not found: {abs_file_path}")
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
                    INSERT OR REPLACE INTO content_index (
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
            self.logger.error(f"File not found: {abs_file_path}")
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
        for handler in self.logger.handlers[:]:
            self.logger.removeHandler(handler)
            handler.close()
        
        
# 
        

