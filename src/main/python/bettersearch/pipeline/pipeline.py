import datetime
from ..llm.llm_interface import LLMInterface
from .util import get_platform_table_names, get_prompt_format, get_compat_table_info
from ..file_indexer.file_indexer import FileIndexer
import itertools


class BetterSearchPipeline:
    def __init__(self, 
                 cache_dir: str = None, 
                 model_config: dict = {},
                 db_config: dict = {},
                 svc_config: dict = {},
                 fs_config: dict = {},
                 indexer_config: dict = {},
                **kwargs):
        self.file_indexer = FileIndexer(db_config=db_config, svc_config=svc_config, fs_config=fs_config, indexer_config=indexer_config, cache_dir=cache_dir, **kwargs)
        self.llm_interface = LLMInterface(**model_config, cache_dir=cache_dir, **kwargs)
        self.prompt_formats = get_prompt_format(self.llm_interface.llm_family, model_config.get("promptFormatDir", None))
        
        self.fs_tables = get_compat_table_info(**kwargs)
        self.compat_table_list, self.compat_table_joins = get_platform_table_names(**kwargs)
        self.table_metadata_string = self._generate_table_metadata_string()
        self.table_join_string = self.__generate_table_join_string()
        
        self._verify_init()
        
    def __call__(self, user_question, **kwargs):
        """
        Generate an answer to the user's question using vector database, file system, and LLM.

        Args:
            user_question (str): User question.
        
        Returns:
            str: Generated answer.
        """
        
        # Initial: Prompt formatting to LLM for generating SQL query
        sql_query_prompt = self.prompt_formats["sqlPromptFormat"].format(
            user_question=user_question,
            table_metadata_string = self.table_metadata_string,
            table_join_string = self.table_join_string,
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        )
        
        # First step: Generate the SQL query
        sql_query = self.llm_interface.generate_text(sql_query_prompt, split_str="```sql")[0]
        
        # Second step: Query the vector database/file system for context
        context_output = self.file_indexer.search(sql_query, user_question)
        
        # Third step: Final prompt format to LLM for generating answer
        general_prompt = self.prompt_formats["generalPromptFormat"].format(
            user_question=user_question,
            user_context=context_output["context"],
        )
        
        # Generate the final answer
        output = self.llm_interface.generate_text(general_prompt, split_str="\n")[0]
        
        return output
    
    
    def _generate_table_metadata_string(self):
        table_dict = {key: val for key, val in self.fs_tables.items() if key in itertools.chain(*self.compat_table_list.values())}
        table_metadata_format = '''CREATE TABLE {table_name} (\n\t{column_metadata}\n)'''
        
        column_metadata_format = '''{column_name} {column_type}, -- {column_description}'''
        
        table_metadata_string = []
        for table_name, data in table_dict.items():    
            column_metadata = "\n\t".join([column_metadata_format.format(column_name=col['name'], column_type=col['type'], column_description=col['description']) for col in data['columns']])
            table_metadata_string.append(table_metadata_format.format(table_name=table_name, column_metadata=column_metadata))
        
        return "\n\n".join(table_metadata_string)
    
    def __generate_table_join_string(self):
        table_join_string = []
        for data in self.compat_table_joins.values():
            for tup in data:
                table_join_string.append(f"-- {tup[0]} can be joined with {tup[1]}")
        
        return "\n".join(table_join_string)
                
    
    def _verify_init(self):
        def ensure_not_none(attr, msg):
            if getattr(self, attr) is None:
                raise ValueError(msg)
        
        ensure_not_none("file_indexer", "File indexer is not initialized.")
        ensure_not_none("llm_interface", "LLM interface is not initialized.")
        ensure_not_none("fs_tables", "File system tables are not initialized.")
        ensure_not_none("compat_table_list", "Compatible table list is not initialized.")
        ensure_not_none("compat_table_joins", "Compatible table joins are not initialized.")
        ensure_not_none("table_metadata_string", "Table metadata string is not initialized.")
        ensure_not_none("table_join_string", "Table join string is not initialized.")

        # Check prompt formats
        if any(prfmt is None for prfmt in self.prompt_formats.values()):
            raise ValueError("Prompt formats are not initialized.")