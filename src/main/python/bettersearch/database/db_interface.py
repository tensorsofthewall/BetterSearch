from typing import List, Dict
from .base_db_handler import BaseDBHandler  # Import the abstract base interface

class DBInterface:
    def __init__(self, db_instance: BaseDBHandler):
        """
        Initialize with a specific vector database instance.
        
        Args:
            db_instance (BaseDBHandler): An instance of a class that implements BaseDBHandler.
        """
        self.db_instance = db_instance

    def add_to_collection(self, file_path: str, date_modified: str):
        """
        Add a file to the vector database collection.

        Args:
            file_path (str): Path to the file.
            date_modified (str): Date the file was last modified.
        """
        self.db_instance.add_to_collection(file_path=file_path, date_modified=date_modified)

    def update_to_collection(self, file_path: str, date_modified: str):
        """
        Update a file in the vector database collection.

        Args:
            file_path (str): Path to the file.
            date_modified (str): Date the file was last modified.
        """
        self.db_instance.update_to_collection(file_path=file_path, date_modified=date_modified)

    def delete_from_collection(self, file_path: str):
        """
        Delete a file from the vector database collection.

        Args:
            file_path (str): Path to the file.
        """
        self.db_instance.delete_from_collection(file_path=file_path)

    def update_collection(self, change_list: List[Dict]):
        """
        Update the vector database collection based on a list of changes.

        Args:
            change_list (list): List of changes detected.
        """
        self.db_instance.update_collection(change_list)

    def query_collection(self, query: str) -> List[str]:
        """
        Query the vector database collection.

        Args:
            query (str): Query text.

        Returns:
            list: Query results.
        """
        return self.db_instance.query_collection(query)
