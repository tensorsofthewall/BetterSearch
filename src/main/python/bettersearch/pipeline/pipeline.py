import datetime
import json
from ..llm.llm_interface import LLMInterface
from .util import get_platform_table_info, get_compat_table_info, get_prompt_formats, get_table_groups, get_sys_specs
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
        # Table information (osquery/Fleet/Other)
        self._prepareTableVars(**kwargs)
        
        # Initialize main objects of pipeline
        self.file_indexer = FileIndexer(db_config=db_config, svc_config=svc_config, fs_config=fs_config, indexer_config=indexer_config, cache_dir=cache_dir, **kwargs)
        
        self.llm_interface = LLMInterface(**model_config, cache_dir=cache_dir, **kwargs)
        
        # Prompt formats for classification, SQL query generation, and answer generation
        self._preparePromptFormats(promptFormatDir=model_config.get("promptFormatDir", None))
        
        # Generate machine spec string
        self._generate_sys_spec_string()
        
        # Verify initialization
        self._verify_init()
    
    def _generate_sys_spec_string(self):
        machine_specs = get_sys_specs()
        self._sys_spec_string = "\n".join([f"{key} - {val}" for key, val in machine_specs.items()])
    
    def __call__(self, user_question, **kwargs):
        """
        Generate an answer to the user's question using vector database, file system, and LLM.

        Args:
            user_question (str): User question.
        
        Returns:
            str: Generated answer.
        """
        
        # Step 1: Classify the user's prompt into "Content-Related", "System-Related", or "Other"
        userPromptClassification_prompt = self.prompt_formats["qClassifierPromptFormat"].format(
            user_question=user_question
        )
        
        userPromptClass = self.llm_interface.generate_text(userPromptClassification_prompt, split_str="Classification:")[0]
        
        if userPromptClass.lower() == "other":
            # Directly query the vector database without running SQL query
            context_output = self.file_indexer.search("Tables are not related to the user's question.", user_question)
        else:
            # Second step: Generate the SQL query
            # Prompt formatting to LLM for generating SQL query
            
            table_metadata_string = self._generate_table_metadata_string(userPromptClass)
            table_join_string = self._generate_table_join_string(userPromptClass)
            
            sql_query_prompt = self.prompt_formats["sqlPromptFormat"].format(
                user_question=user_question,
                table_metadata_string = table_metadata_string,
                table_join_string = table_join_string,
                date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            )
            
            sql_query = self.llm_interface.generate_text(sql_query_prompt, split_str="```sql")[0]
            
            # Third step: Query the vector database/file system for context
            context_output = self.file_indexer.search(sql_query, user_question, userPromptClass)
        
        # Final step: Final prompt format to LLM for generating answer
        general_prompt = self.prompt_formats["outputPromptFormat"].format(
            user_question=user_question,
            svc_source=json.dumps(context_output.get("svc").get("source","")),
            svc_data=json.dumps(context_output.get("svc").get("data","")),
            svc_error=json.dumps(context_output.get("svc").get("error","")),
            dbi_source=json.dumps(context_output.get("dbi").get("source","")),
            dbi_data=json.dumps(context_output.get("dbi").get("data","")),
            dbi_error=json.dumps(context_output.get("dbi").get("error","")),
            date_time=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            sys_specs=self._sys_spec_string,
        )
        
        output = self.llm_interface.generate_text(general_prompt, split_str="Ans:")[0]
        
        return output
    
    
    def _prepareTableVars(self, **kwargs):
        self.fs_tables = get_compat_table_info(**kwargs)
        self._table_groups = get_table_groups(**kwargs)
        self.compat_table_list, self.compat_table_joins = get_platform_table_info(**kwargs)
    
    def _generate_table_metadata_string(self, selected_table_class):
        table_dict = {key: val for key, val in self.fs_tables.items() if key in (set(itertools.chain(*self.compat_table_list.values()) and set(self._table_groups[selected_table_class])))}
        table_metadata_format = '''CREATE TABLE {table_name} (\n\t{column_metadata}\n)'''
        
        column_metadata_format = '''{column_name} {column_type}, -- {column_description}'''
        
        table_metadata_string = []
        for table_name, data in table_dict.items():    
            column_metadata = "\n\t".join([column_metadata_format.format(column_name=col['name'], column_type=col['type'].upper(), column_description=col['description']) for col in data['columns']])
            table_metadata_string.append(table_metadata_format.format(table_name=table_name, column_metadata=column_metadata))
        
        return "\n\n".join(table_metadata_string)
    
    def _generate_table_join_string(self, selected_table_class):
        table_join_string = []
        for data in self.compat_table_joins.values():
            for tup in data:
                table_1, table_2 = tup[0].split(".")[0], tup[1].split(".")[0]
                if table_1 in self._table_groups[selected_table_class] and table_2 in self._table_groups[selected_table_class]:
                    table_join_string.append(f"-- {tup[0]} {'MUST' if len(tup) > 2 else 'CAN'} be joined with {tup[1]}.")
                    
        return "\n".join(table_join_string)
    
    def _generate_table_groups_string(self):
        table_groups_desc = {}
        for group, tables in self._table_groups.items():
            descriptions = [
                f"-- {table_name} - {self.fs_tables[table_name]['description']}"
                for table_name in tables if table_name in self.fs_tables
            ]
            if group == "File and Search Operations":
                descriptions.append("-- content-database - Run searches against file content that has been indexed in the content database. Does not contain information about apps or system specifications.")
            table_groups_desc[group] = "\n".join(descriptions)
        return table_groups_desc
    
    def _preparePromptFormats(self, promptFormatDir):
        self.prompt_formats = get_prompt_formats(self.llm_interface.llm_family, promptFormatDir)
        
        # Get Table Groups String
        table_groups_string = self._generate_table_groups_string()
        self.prompt_formats["qClassifierPromptFormat"] = self.prompt_formats["qClassifierPromptFormat"].format(
            content_tables = table_groups_string['File and Search Operations'],
            system_tables = table_groups_string['System and User Information']
        )
        
    
    def _verify_init(self):
        def ensure_not_none(attr, msg):
            if getattr(self, attr) is None:
                raise ValueError(msg)
        
        ensure_not_none("file_indexer", "File indexer is not initialized.")
        ensure_not_none("llm_interface", "LLM interface is not initialized.")
        ensure_not_none("fs_tables", "File system tables are not initialized.")
        ensure_not_none("compat_table_list", "Compatible table list is not initialized.")
        ensure_not_none("compat_table_joins", "Compatible table joins are not initialized.")
        # ensure_not_none("table_metadata_string", "Table metadata string is not initialized.")
        # ensure_not_none("table_join_string", "Table join string is not initialized.")

        # Check prompt formats
        if any(prfmt is None for prfmt in self.prompt_formats.values()):
            raise ValueError("Prompt formats are not initialized.")