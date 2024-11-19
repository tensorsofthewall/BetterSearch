from abc import ABC, abstractmethod
from typing import List, Dict

class BaseDBHandler(ABC):
    @abstractmethod
    def add_to_collection(self, file_path: str, date_modified: str):
        """Add a file to the vector database collection."""
        raise NotImplementedError
    
    @abstractmethod
    def update_to_collection(self, file_path: str, date_modified: str):
        """Update a file in the vector database collection."""
        raise NotImplementedError
    
    @abstractmethod
    def delete_from_collection(self, file_path: str):
        """Delete a file from the vector database collection."""
        raise NotImplementedError
    
    @abstractmethod
    def update_collection(self, change_list: List[Dict]):
        """Update the vector database collection based on a list of changes."""
        raise NotImplementedError
    
    @abstractmethod
    def query_collection(self, query: str) -> List[str]:
        """Query the vector database collection."""
        raise NotImplementedError
