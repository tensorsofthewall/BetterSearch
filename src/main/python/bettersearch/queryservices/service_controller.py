from typing import Optional

from ..queryservices.osquery_service import OSQueryService
from ..queryservices.fleet_service import FleetQueryService
from .base_service import BaseQueryService
import inspect
import asyncio
from collections import defaultdict

class ServiceController:
    """
    ServiceController allows you to manage multiple query services and switch between query services without having to restart the program. 
    """
    def __init__(self, **kwargs):
        """
        Initialize the service controller.
        
        This sets the service to None, effectively disabling the controller until set_service is called.
        """
        self._service_type = kwargs.get("type", "")
        self.service = self._create_service(**kwargs)
    
    def _create_service(self, **kwargs):
        if self._service_type == "osquery":
            return OSQueryService(**kwargs)
        elif self._service_type == "fleetdm":
            return FleetQueryService(**kwargs)
        elif not self._service_type:
            raise ValueError(f"Service type not specified. Please specify a valid service type.")
        else:
            raise ValueError(f"Unsupported service type: {self._service_type}")
    
    def get_service_type(self):
        return self._service_type
    
    def get_current_state(self, **kwargs):
        output = defaultdict(lambda: None)
        output.update({"source": self._service_type})
        output.update(self.service._get_current_state(**kwargs))
        return output
    
    def run_query(self, query: str, **kwargs):
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device

        Returns:
            response (dict|obj): Query results
        """
        output = defaultdict(lambda: None)
        output.update({"source": self._service_type})
        if self.service:
            if inspect.iscoroutinefunction(self.service.run_query): # Handle asynchronous queries
                output.update(asyncio.run(self.service.run_query(query, **kwargs)))
            else:
                output.update(self.service.run_query(query, **kwargs))
            
            return output
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