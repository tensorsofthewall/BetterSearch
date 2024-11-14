from .base_handler import BaseLLMHandler
from transformers import BitsAndBytesConfig
from pathlib import Path
from ..pipeline.util import get_local_model_and_tokenizer
import torch

from typing import List


class LlamaHandler(BaseLLMHandler):
    """
    A handler class for Llama large language models.

    This class provides a specific implementation for handling Llama models, including
    initialization, text generation, and shutdown.

    Attributes:
        model (torch.nn.Module): The Llama model instance.
        tokenizer (transformers.Tokenizer): The tokenizer instance for the Llama model.
        num_beams (int): The number of beams to use for text generation.

    Methods:
        generate(prompts, **kwargs): Generate text based on the given prompts.
        get_tokenizer(): Get the tokenizer for the LLM.
        get_device(): Get the device type where the LLM is hosted.
        shutdown(): Shutdown the LLM model and tokenizer, freeing up memory.
    """
    def __init__(self, model_name: str = None, cache_dir: str | Path = None, bnb_config: BitsAndBytesConfig = None, kv_cache_flag: bool = True, **kwargs):
        """
        Initialize the LlamaHandler with the given parameters.

        Args:
            model_name (str): Name of the model to be used.
            cache_dir (str | Path): Directory to cache the model.
            bnb_config (BitsAndBytesConfig): Configuration for bits and bytes.
            kv_cache_flag (bool): Flag to enable or disable key-value caching.
            **kwargs: Additional keyword arguments.
        """

        super().__init__()
        self.model, self.tokenizer = get_local_model_and_tokenizer(
            model_name,
            cache_dir,
            bnb_config,
            kv_cache_flag,
            **kwargs
        )
        self.num_beams = kwargs.get('num_beams', 4)
        
    def get_tokenizer(self):
        """
        Get the tokenizer for the LLM.

        Returns:
            Tokenizer for the LLM.
        """
        
        return self.tokenizer
    
    def get_device(self):
        """
        Get the device for the LLM.

        Returns:
            str: The device type ('cpu' or 'cuda') if the LLM is hosted locally, or None if the LLM is hosted remotely.
        """
        return self.model.device
    
    def generate(self, prompts: List[str] | str, **kwargs):
        """
        Generate text based on the given prompts.

        Args:
            prompts: Prompt(s) to generate text from.
            **kwargs: Additional keyword arguments.

        Returns:
            Generated text.
        """
        
        return self.tokenizer.batch_decode(
            self.model.generate(
                **self.tokenizer(
                    prompts, return_tensors="pt"
                ).to(self.get_device),
                num_return_sequences=1,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.eos_token_id,
                max_new_tokens=400,
                num_beams=self.num_beams,
                do_sample=kwargs.get('do_sample', False),
                temperature=kwargs.get('temperature', None),
                top_p=kwargs.get('top_p', None),
            ),
            skip_special_tokens=True
        )

    def shutdown(self):
        """
        Shutdown the LLM model and tokenizer, freeing up memory.

        This is important to do when you're finished using the model to avoid
        running out of memory, especially if you're running multiple models in
        the same process.
        """
        
        del self.model
        del self.tokenizer
        torch.cuda.empty_cache()
        
        self.model = None
        self.tokenizer = None