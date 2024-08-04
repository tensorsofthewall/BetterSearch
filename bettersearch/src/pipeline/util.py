import os, re, sys, pathlib
import shutil
from collections import defaultdict
import sqlparse
from sqlparse.tokens import Keyword, DML
from sqlparse.sql import Identifier, IdentifierList

# Clean the output of Llama-SQLCoder by formatting and removing aliases.
def clean_sqlcoder_output(sql_query, table_info, table_name):
    columns = extract_columns_from_metadata(table_info)
    return remove_aliases_from_query(
        sqlparse.split(
            sqlparse.format(
                sql_query.split("```sql")[-1]
            ),
            strip_semicolon=True
        )[0],
        columns=columns,
        table_name=table_name
    )

# Remove table aliases from the SQL query and replace them with fully qualified column names.
def remove_aliases_from_query(query, columns, table_name):
    # Find table aliases in the FROM and JOIN clauses
    table_alias_pattern = re.compile(r'\b(FROM|JOIN)\s+' + table_name + r'\s+(?:AS\s+)?(\w+)\b', re.IGNORECASE)
    table_alias_match = table_alias_pattern.search(query)

    if table_alias_match:
        table_alias = table_alias_match.group(2)
        # Replace table aliases in the query with fully qualified column names
        for col in columns:
            query = re.sub(r'\b' + table_alias + r'\.' + col + r'\b', col, query)
        
        # Remove the table alias definition from the FROM and JOIN clauses
        query = re.sub(table_alias_pattern, r'\1 ' + table_name, query)
    
    return query

# Extract fully qualified column names from the table metadata.
def extract_columns_from_metadata(metadata):
    # Match fully qualified column names
    column_pattern = re.compile(r'\b(\w+\.\w+)\s+\w+', re.IGNORECASE)
    columns = column_pattern.findall(metadata)
    return columns

# Remove 'NULLS LAST' from the ORDER BY clause in the SQL query.
def remove_nulls_last(query):
    parsed = sqlparse.parse(query)
    statement = parsed[0]
    
    new_tokens = []
    order_by_found = False

    for token in statement.tokens:
        if token.ttype is Keyword and token.value.upper() == 'ORDER BY':
            order_by_found = True
            new_tokens.append(token)
            continue

        if order_by_found:
            if token.ttype is None and 'NULLS LAST' in token.value.upper():
                new_value = token.value.upper().replace('NULLS LAST', '').strip()
                new_tokens.append(sqlparse.sql.Token(None, new_value))
                order_by_found = False  # Process the ORDER BY clause only once
            else:
                new_tokens.append(token)
        else:
            new_tokens.append(token)
    
    corrected_query = ''.join(str(token) for token in new_tokens)
    return corrected_query

# Validate and correct SQL query
def validate_correct_sql_query(input_query):
    parsed = sqlparse.parse(input_query)
    statement = parsed[0]
    
    # Find the SELECT and ORDER BY clauses
    select_token_index = None
    order_by_token_index = None
    top_token_index = None
    select_identifiers = None
    order_by_identifiers = None
    
    for i, token in enumerate(statement.tokens):
        if token.ttype is Keyword and token.value.upper() == 'SELECT':
            select_token_index = i
        elif token.ttype is Keyword and token.value.upper() == 'ORDER BY':
            order_by_token_index = i
        elif token.ttype is Keyword and token.value.upper() == 'TOP':
            top_token_index = i

    if select_token_index is None or order_by_token_index is None:
        return input_query

    # Extract columns after SELECT and before FROM
    select_identifiers = statement.tokens[select_token_index + 1]
    if isinstance(select_identifiers, IdentifierList):
        select_columns = select_identifiers.get_identifiers()
    elif isinstance(select_identifiers, Identifier):
        select_columns = [select_identifiers]
    else:
        return input_query
    
    # Extract columns after ORDER BY
    order_by_identifiers = statement.tokens[order_by_token_index + 2]
    if isinstance(order_by_identifiers, IdentifierList):
        order_by_columns = order_by_identifiers.get_identifiers()
    elif isinstance(order_by_identifiers, Identifier):
        order_by_columns = [order_by_identifiers]
    else:
        return input_query

    # Build the corrected query
    new_query = []
    for i, token in enumerate(statement.tokens):
        if i == select_token_index:
            new_query.append('SELECT')
            if top_token_index is not None:
                top_value = statement.tokens[top_token_index + 2]
                new_query.append(f" TOP {top_value}")
            for col in select_columns:
                new_query.append(f" {col},")
            new_query[-1] = new_query[-1][:-1]  # Remove trailing comma
        elif i == order_by_token_index:
            new_query.append(' ORDER BY')
            for col in order_by_columns:
                new_query.append(f" {col},")
            new_query[-1] = new_query[-1][:-1]  # Remove trailing comma
        else:
            new_query.append(str(token).strip())
            
    new_query = ' '.join(new_query).strip()
    
    new_query = remove_nulls_last(new_query)

    return new_query


# Get model and tokenizer based on model type (OpenVINO vs Regular PyTorch/HuggingFace)
def get_model_and_tokenizer(model_name, cache_dir, bnb_config, kv_cache_flag, **kwargs):
    from transformers import AutoTokenizer
    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=model_name, cache_dir=cache_dir, use_fast=True)
    if "ov" in model_name:
        from optimum.intel.openvino import OVModelForCausalLM
        model = OVModelForCausalLM.from_pretrained(
            model_id=model_name, 
            cache_dir=cache_dir,
            use_cache=kv_cache_flag
            )
    else:
        from transformers import AutoModelForCausalLM
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_name_or_path=model_name, 
            cache_dir=cache_dir,
            use_cache=kv_cache_flag,
            quantization_config=bnb_config,
            trust_remote_code=True,
            device_map="auto", **kwargs
            )
    
    return model, tokenizer

# Separate method for getting prompt
def get_prompt_format(file):
    with open(file, "r") as f:
        prompt = f.read()
    return prompt

# Get SQL/OLEDB Table Metadata and Name
def get_table_info():
    if sys.platform == "win32":
        from ..database.constants import WIN_SYSTEMINDEX_TABLE_METADATA
        return WIN_SYSTEMINDEX_TABLE_METADATA, "SystemIndex"
    elif sys.platform == "linux" or sys.platform == "linux2":
        # For Linux DB
        pass
    elif sys.platform == "darwin":
        # For OS X
        pass

# Get File Indexer    
def get_file_indexer(**kwargs):
    if sys.platform == "win32":
        from ..database import WindowsFileIndexer
        return WindowsFileIndexer(**kwargs)
    elif sys.platform == "linux" or sys.platform == "linux2":
        # For Linux DB
        # from ..database import LinuxFileIndexer
        pass
    elif sys.platform == "darwin":
        # For OS X
        pass

# Method to download and save new models in OpenVINO IR Format
def download_and_save_ov_models(model_id, save_dir, fp_gen = "INT4"):
    from optimum.intel.openvino import OVModelForCausalLM
    
    _, model_name = model_id.split("/")
    ov_model = OVModelForCausalLM.from_pretrained(model_id=model_id, export=True, compile=False, load_in_8bit=False)
    
    # Save in FP32
    if fp_gen == "FP32":
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP32")
    # Save in FP16
    if fp_gen == "FP16":
        ov_model.half()
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP16")
    # Save in INT8
    elif fp_gen == "INT8":
        from optimum.intel import OVQuantizer
        ov_quantizer = OVQuantizer.from_pretrained(ov_model)
        ov_quantizer.quantize(save_directory=f"{save_dir}/{model_name}/INT8", weights_only=True)
    # Save in INT4
    elif fp_gen == "INT4":
        import nncf
        import openvino as ov
        ov_model.save_pretrained(f"{save_dir}/{model_name}/FP16")
        compressed_model = nncf.compress_weights(
            ov_model.half()._original_model,
            mode=nncf.CompressWeightsMode.INT4_ASYM,
            group_size=128,
            ratio=0.8
        )
        ov.save_model(compressed_model, f"{save_dir}/{model_name}/INT4/openvino_model.xml")
        shutil.copy(f"{save_dir}/{model_name}/FP16/config.json", f"{save_dir}/{model_name}/INT4/config.json")
        shutil.rmtree(f"{save_dir}/{model_name}")
        
# Get available models from saved directory
def get_available_models(save_dir):
    available_models = defaultdict(list)
    for model_name in os.listdir(save_dir):
        model_dir = os.path.join(save_dir, model_name)
        if os.path.isdir(model_dir):
            for precision in os.listdir(model_dir):
                precision_path = os.path.join(model_dir, precision)
                if os.path.isdir(precision_path):
                    available_models[precision].append(model_name)
    
    return available_models