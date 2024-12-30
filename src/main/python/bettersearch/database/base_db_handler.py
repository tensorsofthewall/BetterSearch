from abc import ABC, abstractmethod
from typing import List

class BaseDBHandler(ABC):
    @abstractmethod
    def _add_to_collection(self, file_path=None, date_modified=None):
        """Update the vector database collection based on a list of changes."""
        raise NotImplementedError
    @abstractmethod
    def _delete_from_collection(self, file_path=None):
        """Update the vector database collection based on a list of changes."""
        raise NotImplementedError
    @abstractmethod
    def _update_to_collection(self, file_path=None, date_modified=None):
        """Update the vector database collection based on a list of changes."""
        raise NotImplementedError
    
    @abstractmethod
    def get_all_metadata(self, collection_name: str):
        """Get all metadata from the vector database collection."""
        raise NotImplementedError
    
    @abstractmethod
    def query_collection(self, query: str) -> List[str]:
        """Query the vector database collection."""
        raise NotImplementedError
