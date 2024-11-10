from abc import ABC, abstractmethod
from platformdirs import PlatformDirs
from bettersearch import APP_NAME, VERSION

class BaseQueryService(ABC):
    @abstractmethod
    def __init__(self, **kwargs):
        """
        Initialize the service.

        This method is intended to be overridden by subclasses of BaseQueryService.

        Args:
            **kwargs: Additional keyword arguments
        """
        self.platformdirs = PlatformDirs(APP_NAME, version=VERSION)
    @abstractmethod
    def run_query(self, query, **kwargs):
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device
        
        Returns:
            response (list|obj): Query results
        """
        pass
    
    @abstractmethod
    def stop(self):
        """
        Shutdown the service.

        This method is intended to be overridden by subclasses of BaseQueryService.
        """
        pass