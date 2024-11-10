"""
To get all available tables on current platform in osquery:
- select distinct name from osquery_registry where registry = 'table' and active = true and internal = false
"""

from .base_service import BaseQueryService
import osquery
from platformdirs import PlatformDirs
import pywintypes
import threading 

class OSQueryService(BaseQueryService):
    def __init__(self):
        """
        Initialize query service for osquery (local device management).
        
        For more info on osquery, see https://osquery.readthedocs.io/en/stable/

        This initializes an instance of the osquery service, and opens a connection to it.
        """
        
        super().__init__()
        self.instance = osquery.SpawnInstance()
        self.instance.open()
        
        # For thread-safe stop
        self._stop_lock = threading.Lock()

    def run_query(self, query, **kwargs):
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device
        
        Returns:
            response (dict|obj): Query results
        """
        try:
            result = self.instance.client.query(query)
            if result.status.code != 0:
                return {"error": result.status.message}
            return {"source": "osquery","data": result.response}
        except Exception as e:
            return {"error": f"Failed to execute query on osquery database: {e}"}
        

    def stop(self):
        """
        Stop the OSQueryService instance.

        This is a thread-safe method. It should be called when the service is no longer needed to free up system resources.
        """
        with self._stop_lock:     
            try:
                self.instance.__del__()
            except pywintypes.error as e:
                # To handle osquery issue https://github.com/osquery/osquery-python/issues/57
                if e.args[2] == "Incorrect function.":
                    import win32file
                    win32file.CloseHandle(self.instance.connection._transport._TBufferedTransport__trans._handle)
                    self.instance.connection._transport._TBufferedTransport__trans._handle = None
                    self.instance.__del__()
                