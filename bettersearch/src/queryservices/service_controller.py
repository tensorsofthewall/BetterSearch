from typing import Optional
from .base_service import BaseQueryService
import inspect
import asyncio

class ServiceController:
    """
    ServiceController allows you to manage multiple query services and switch between query services without having to restart the program. 
    """
    def __init__(self):
        """
        Initialize the service controller.
        
        This sets the service to None, effectively disabling the controller until set_service is called.
        """
        
        self.service: Optional[BaseQueryService] = None
        
    def set_service(self, service: BaseQueryService):
        """
        Set the service to be used by this controller.

        This method can be called multiple times to change the service used by this controller.

        Args:
            service (BaseQueryService): The service to use for running queries
        """

        self.service = service
    
    def run_query(self, query: str, **kwargs):
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device

        Returns:
            response (dict|obj): Query results
        """
        
        if self.service:
            if inspect.iscoroutinefunction(self.service.run_query): # Handle asynchronous queries
                return asyncio.run(self.service.run_query(query, **kwargs))
            else:
                return self.service.run_query(query, **kwargs)
        else:
            raise ValueError("No service set")
        
    def get_service(self) -> Optional[BaseQueryService]:
        """
        Get the service currently set on this controller.

        Returns:
            service (BaseQueryService|None): The service currently set on this controller, or None if no service is set
        """
        return self.service
    
    def stop_service(self):
        """
        Stop the currently set service.

        This method stops the service, if a stop method is available.
        """
        if self.service:
            self.service.stop()
            self.service = None