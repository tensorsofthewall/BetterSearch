from typing import List, DefaultDict, Any
from .chromadb_handler import ChromaDBHandler

class DBInterface:
    def __init__(self, **kwargs):
        """
        Initialize with a specific vector database instance.
        
        Args:
            db_instance (BaseDBHandler): An instance of a class that implements BaseDBHandler.
        """
        self.db_instance = self._create_db_handler(**kwargs)
        
    def _create_db_handler(self, **kwargs):
        db_type = kwargs.get("type", "")
        if db_type == "chroma":
            self._db_type = db_type
            return ChromaDBHandler(**kwargs)
        elif not db_type:
            raise ValueError(f"Database type not specified. Please specify a valid database type.")
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
    
    def get_collection_metadata(self):
        """
        Get file metadata from the vector database collection.
        """
        return self.db_instance.get_all_metadata()

    def update_collection(self, change_list: DefaultDict[Any, List]):
        """
        Update the vector database collection based on a list of changes.

        Args:
            change_list (list): List of changes detected.
        """
        # self.db_instance.update_collection(change_list)
        for change_type, values in change_list.items():
            if change_type == "Deleted":
                self.db_instance._delete_from_collection(file_paths=values)
            elif change_type =="Added":
                self.db_instance._add_to_collection(values)
            elif change_type == "Modified":
                self.db_instance._update_to_collection(values)

    def query_collection(self, query: str, **kwargs) -> dict:
        """
        Query the vector database collection.

        Args:
            query (str): Query text.

        Returns:
            list: Query results.
        """
        return {"source": self._db_type, **self.db_instance.query_collection(query, **kwargs)}
