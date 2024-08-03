from transformers import BitsAndBytesConfig
import datetime
from .util import clean_sqlcoder_output, get_file_indexer, get_prompt_format, get_model_and_tokenizer, get_table_info
from pathlib import Path
        
class BetterSearchPipeline:
    def __init__(self, model_name: str = None, cache_dir: str = None, 
                 bnb_config: BitsAndBytesConfig = None, kv_cache_flag: bool = True, 
                 num_beams: int = 4, db_path: str = "better_search_content_db") -> None:
        self.file_indexer = get_file_indexer(db_path=db_path)
        self.model, self.tokenizer = get_model_and_tokenizer(model_name, cache_dir, bnb_config, kv_cache_flag)
        self.num_beams = num_beams
        self.sqlPrompt_format = get_prompt_format(Path("./sqlcoder_prompt.md"))
        self.llamaPrompt_format = get_prompt_format(Path("./llama_prompt.md"))
        self.table_metadata_string, self.table_name = get_table_info()
    
    def answer(self, user_question):
        # First step: Initial prompt to LLM generates an SQL query which is validated and acted upon accordingly to get context for the user question (user_context)
        curr_prompt = self.sqlPrompt_format.format(
            user_question=user_question, 
            table_metadata_string=self.table_metadata_string, 
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        
        output = self.tokenizer.batch_decode(
            self.model.generate(
                **self.tokenizer(
                    curr_prompt, return_tensors="pt"
                ),
                num_return_sequences=1,
                eos_token_id=self.tokenizer.eos_token_id,
                pad_token_id=self.tokenizer.pad_token_id,
                max_new_tokens=400,
                do_sample=False,
                num_beams=self.num_beams
            ),
            skip_special_tokens=True
        )[0]
        
        output = clean_sqlcoder_output(output, self.table_metadata_string, self.table_name)
        
        # Second step: Use user_context (SQL query output or Content search) to get final answer to question.
        user_context = self.file_indexer.query(output, user_question)
        
        curr_prompt = self.llamaPrompt_format.format(
            user_question=user_question,
            user_context=user_context
        )
        
        output = self.tokenizer.batch_decode(
            self.model.generate(
                **self.tokenizer(
                    curr_prompt, return_tensors="pt"
                ),
                num_return_sequences=1,
                max_new_tokens = 256,
                eos_token_id = [self.tokenizer.eos_token_id, self.tokenizer.convert_tokens_to_ids("<|eot_id|>")],
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            ),
            skip_special_tokens=True
        )[0]
        
        return output
        
        
        
        
        
        