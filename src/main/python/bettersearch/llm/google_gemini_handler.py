from .base_handler import BaseLLMHandler
import google.generativeai as genai
import json

gemini_system_instructions = """
You are a expert assistant that converts English questions into SQL queries. The user will provide the SQL tables and the question, you must create an SQL query to answer the question using the tables provided. Do not use any tables that are not provided. Return the generated SQL query and the tables used in the SQL query using the following JSON schema:
{
    "question": "string",
    "tables_used": "string",
    "sql_query": "string",
}
"""
class GoogleGeminiHandler(BaseLLMHandler):
    """
    A handler class for Google Gemini LLMs (API access).
    
    This class provides a general implementation for handling Google Gemini models using Google's Generative AI Python SDK (https://github.com/google-gemini/generative-ai-python).
    
    Current version - 0.8.3

    Args:
        BaseLLMHandler (_type_): _description_
    """
    def __init__(self, api_key: str, model_name: str, **kwargs):
        """
        Initialize the GoogleGeminiHandler with the given parameters.

        Args:
            api_key (str): API key to use for the Gemini API.
            model_name (str): Name of the Gemini model to use.
            **kwargs: Additional keyword arguments.
        """
        
        self.model_name = model_name
        self.is_safety_set = True if 'safety_settings' in kwargs else False
        self.safety_settings = kwargs.get('safety_settings', self.get_safety_settings())
        
        genai.configure(api_key=api_key)
        
        self.llm = genai.GenerativeModel(
            self.model_name,
            system_instruction=gemini_system_instructions
        )
        
    def generate(self, prompt, **kwargs):
        """
        Generate text based on the given prompts.

        Args:
            prompts: Prompt(s) to generate text from.
            **kwargs: Additional keyword arguments.

        Returns:
            Generated text.
        """

        try:
            response = self.llm.generate_content(
                [prompt],
                request_options={"timeout": 30},
                safety_settings=self.safety_settings
            )
            return json.loads(response.text.strip("```json\n"))
        except Exception as e:
            print(f"Error generating SQL query with Google Gemini: {e}")
            return ""
    
    def get_safety_settings(self):
        """
        Get the safety settings for the Gemini model.

        If the safety settings have been set, they are returned. Otherwise, the default safety settings are returned.

        Returns:
            dict: The safety settings for the Gemini model.
        """
        default_safety_settings = {
            genai.types.HarmCategory.HARM_CATEGORY_HATE_SPEECH: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_HARASSMENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: genai.types.HarmBlockThreshold.BLOCK_NONE,
            genai.types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: genai.types.HarmBlockThreshold.BLOCK_NONE,
        }

        if self.is_safety_set:
            return self.safety_settings
        
        self.is_safety_set = True

        return default_safety_settings
    
    def set_safety_settings(self, safety_settings):
        """
        Set the safety settings for the Gemini model.

        Args:
            safety_settings (dict): Safety settings for the Gemini model.
                Should be a dictionary of harm categories and their corresponding block thresholds.

        Raises:
            ValueError: If the safety settings are invalid.
        """
        
        self.safety_settings = safety_settings
        # Sanity Checks
        if not isinstance(safety_settings, dict):
            raise ValueError("Safety settings must be a dictionary")
        for harm_category, harm_block_threshold in safety_settings.items():
            if harm_category not in genai.types.HarmCategory.__members__:
                raise ValueError(f"Invalid harm category: {harm_category}")
            if harm_block_threshold not in genai.types.HarmBlockThreshold.__members__:
                raise ValueError(
                    f"Invalid harm block threshold: {harm_block_threshold}"
                )
        
        self.safety_settings = safety_settings
        self.is_safety_set = True
    
    
    def reset_safety_settings(self):
        self.is_safety_set = False
        self.safety_settings = self.get_safety_settings()