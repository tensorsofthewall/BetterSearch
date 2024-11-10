from .base_service import BaseQueryService
import asyncio
import aiohttp


class FleetQueryService(BaseQueryService):
    def __init__(self, url, api_key, **kwargs):
        """
        Initialize FleetQueryService.

        Args:
            url (str): URL of Fleet instance/server
            api_key (str): API key for Fleet instance/server
            **kwargs: Additional keyword arguments
        """
        super().__init__()
        self.url = url
        self.api_key = api_key

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