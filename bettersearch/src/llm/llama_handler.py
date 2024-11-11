from .base_handler import BaseLLMHandler
from transformers import BitsAndBytesConfig
from pathlib import Path
from ..pipeline.util import get_local_model_and_tokenizer

from typing import List


class LlamaHandler(BaseLLMHandler):
    def __init__(self, model_name: str = None, cache_dir: str | Path = None, bnb_config: BitsAndBytesConfig = None, kv_cache_flag: bool = True, **kwargs):
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
        return self.tokenizer
    
    def get_device(self):
        return self.model.device
    
    def generate(self, prompts: List[str] | str, **kwargs):
        return self.tokenizer.batch_decode(
            self.model.generate(
                **self.tokenizer(
                    prompts, return_tensors="pt"
                ).to(self.get_device),
                num_return_sequences=1,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
                max_new_tokens=400,
                do_sample=False,
                num_beams=self.num_beams,
            )
        )
