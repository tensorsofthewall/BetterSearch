from abc import ABC, abstractmethod
from typing import List


class BaseLLMHandler(ABC):
    """
    Abstract base class for Large Language Model (LLM) handlers.

    This class defines a basic structure for LLM handlers, including generating text,
    getting a tokenizer, and getting a device. Subclasses must implement the abstract
    methods to provide concrete functionality.

    Methods:
        generate(prompts, **kwargs): Generate text based on the given prompts.
        get_tokenizer(): Get the tokenizer for the LLM.
        get_device(): Get the device for the LLM.
    """
    @abstractmethod
    def generate(self, prompts: List[str] | str, **kwargs):
        """
        Generate text based on the given prompts.

        Args:
            prompts: Prompt(s) to generate text from.
            **kwargs: Additional keyword arguments.

        Returns:
            Generated text.
        """
        pass
    
    @abstractmethod
    def get_tokenizer(self):
        """
        Get the tokenizer for the LLM.

        Returns:
            Tokenizer for the LLM.
        """
        pass
    
    @abstractmethod
    def get_device(self):
        """
        Get the device for the LLM. 
        
        Note: This method is pplicable for locally hosted LLMs. For remotely hosted LLMs / APIs, do not implement this method.

        Returns:
            str: The device type ('cpu' or 'cuda') if the LLM is hosted locally, or None if the LLM is hosted remotely / API calls are made.
        """
        pass