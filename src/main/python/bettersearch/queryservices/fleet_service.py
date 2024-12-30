from .base_service import BaseQueryService
import aiohttp


class FleetQueryService(BaseQueryService):
    """
    A query service class for interacting with FleetDM instances.

    This class provides a way to run SQL queries on a FleetDM instance and retrieve the results.
    It uses the FleetDM API to send queries and retrieve data.

    See Also:
        https://fleetdm.com/docs/ for more information on FleetDM.
    """
    def __init__(self, **kwargs):
        """
        Initialize query service for FleetDM (local, cloud, multi device management).
        Args:
            url (str): URL of Fleet instance/server
            api_key (str): API key for Fleet instance/server
            **kwargs: Additional keyword arguments
        """
        super().__init__()
        self.url = kwargs.get("url", None)
        self.api_key = kwargs.get("api_key", None)

    async def run_query(self, query, **kwargs):
        """
        Run SQL query and return results

        Args:
            query (str): SQL query to run on device

        Returns:
            response (dict|obj): Query results
        """
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = {"query": query}
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, json=data, headers=headers) as response:
                if response.status != 200:
                    return {"error": f"Failed to execute query on Fleet database: {response.status}"}
                
                response_data = await response.json()
                return {"source": "fleet","data": response_data}