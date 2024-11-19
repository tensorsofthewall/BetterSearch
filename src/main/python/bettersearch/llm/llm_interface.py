from .base_handler import BaseLLMHandler
from typing import List, Union, Any

from .base_handler import BaseLLMHandler


class LLMInterface:
    """
    Interface for Large Language Model (LLM) handlers.

    This class provides a clean, simple interface for making LLM calls,
    and ensures that LLM calls are independent.

    Attributes:
        llm_handler (BaseLLMHandler): The LLM handler to use for making LLM calls.

    Methods:
        generate_text(prompts, **kwargs): Generate text based on the given prompts.
        get_tokenizer(): Get the tokenizer for the LLM.
        get_device(): Get the device for the LLM.
    """

    def __init__(self, llm_handler: BaseLLMHandler, answer_preface: str = ""):
        self.llm_handler = llm_handler
        self.answer_preface = answer_preface

    def generate_text(self, prompts: Union[List[str], str], split_str: str = None, **kwargs):
        """
        Generate text based on the given prompts.

        Args:
            prompts: Prompt(s) to generate text from.
            **kwargs: Additional keyword arguments.

        Returns:
            Generated text.
        """
        return clean_llm_output(
            self.llm_handler.generate(prompts, **kwargs),
            self.answer_preface,
            split_str
        )

    def get_tokenizer(self) -> Union[Any, None]:
        """
        Get the tokenizer for the LLM.

        Returns:
            Tokenizer for the LLM.
        """
        return self.llm_handler.get_tokenizer()

    def get_device(self) -> Union[str, None]:
        """
        Get the device for the LLM.

        Note: This method is only applicable for locally hosted LLMs. For remotely hosted LLMs,
        this method should not be implemented.

        Returns:
            str: The device type ('cpu' or 'cuda') if the LLM is hosted locally, or None if the LLM is hosted remotely.
        """
        return self.llm_handler.get_device()
    
    def shutdown(self):
        """
        Shutdown the LLM model and tokenizer, freeing up memory.

        Returns:
            None
        """

        if hasattr(self.llm_handler, 'shutdown'):
            self.llm_handler.shutdown()


def clean_llm_output(llm_output: str = "", answer_preface: str = "", split_str: str = None):
    """
    Clean the output from the LLM by stripping leading and trailing whitespace and
    optionally splitting the output using a specified string.

    Args:
        llm_output (str, optional): The output from the LLM. Defaults to "".
        answer_preface (str, optional): The prefix to add to the cleaned output. Defaults to "".
        split_str (str, optional): The string to split the output by. If not specified, the
            entire output is returned. Defaults to None.

    Returns:
        List[str]: A list containing a single string which is the cleaned output.
    """
    cleaned_output = llm_output.split(split_str)[-1].strip() if split_str else llm_output.strip()
    return [
        ''.join([
            answer_preface,
            cleaned_output
        ])
    ]