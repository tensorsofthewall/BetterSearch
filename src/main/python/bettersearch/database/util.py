import os, re, requests
import platform
from collections import defaultdict
from .constants import parsable_exts, WIN_SYSINDEX_TO_COLS
from pathlib import Path
from typing import List

def convert_gps_info_to_lat_lon_alt(gpsInfo):
    def convert_to_degrees(value):
        degrees, minutes, seconds = value
        return degrees + (minutes / 60.0) + (seconds / 3600.0)
    
    lat_direction = gpsInfo[1]
    lat_value = gpsInfo[2]
    lon_direction = gpsInfo[3]
    lon_value = gpsInfo[4]
    altitude = gpsInfo[5]
    
    latitude = convert_to_degrees(lat_value)
    if lat_direction == 'S':
        latitude = -latitude
    
    longitude = convert_to_degrees(lon_value)
    if lon_direction == 'W':
        longitude = -longitude
    
    return f"Latitude: {latitude}, Longitude: {longitude}, Altitude: {altitude}m"


def get_all_exts(exts):
    all_exts = []
    for key in exts.keys():
        if any(isinstance(sub, list) for sub in exts[key]):
            for sublist in exts[key]:
                all_exts.extend(sublist)
        else:
            all_exts.extend(exts[key])
    return all_exts


def find_files_recursively(folders):
        files = []
        for dir in folders:
            dir_path = Path(dir)
            if dir_path.exists() and dir_path.is_dir():
                files.extend([p for p in dir_path.rglob('*') if p.suffix in get_all_exts(parsable_exts)])
        
        return files


def create_init_config():
    config = defaultdict(str)
    config['index_folders'] = os.path.expanduser("~")
    if platform.system() == "Windows":
        config['index_folder_exceptions'] = os.path.join(os.path.expanduser("~"), "AppData")
    return config


def is_sql_query(query):
    """
    Check if given query is SQL or NL query
    """
    
    sql_keywords = [
        'SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER',
        'OUTER', 'GROUP BY', 'ORDER BY', 'HAVING', 'LIMIT', 'OFFSET','TABLE', 'AND', 'OR', 'NOT', 'BETWEEN', 'LIKE', 'IN', 'AS','DISTINCT'
    ]
    
    query_upper = query.upper()
    
    for keyword in sql_keywords:
        if keyword in query_upper:
            return True
    
    # Regex Checking of SQL-like syntax for osquery
    sql_patterns = [
        r'\bSELECT\b.*\bFROM\b',
        r'^SELECT\s+.+\s+FROM\s+\w+(\s+WHERE\s+.+)?(\s+(ORDER BY|GROUP BY)\s+\w+(\s+(ASC\|DESC))?)?(\s+LIMIT\s+\d+)?;?$',
        r'^SELECT\s+(\*\|[\w, ]+)\s+FROM\s+\w+',
        r'WHERE\s+\w+\s+(=\|LIKE\|IN\|BETWEEN\|>\|<\|>=\|<=)\s+(\'.+\'\|\d+\|\(.+\))',
        r'JOIN\s+\w+\s+(ON\|USING)\s+\(.+\)',
        r'regex_match\(\w+,\s*\'.*\',\s*\d+\)',
    ]
    
    for pattern in sql_patterns:
        if re.search(pattern, query_upper):
            return True
    
    return False

def format_sqlrows_to_text(rows, description):
    """
    Convert SQLrows to text input for LLM
    """
    if not rows:
        return ""
    
    column_names = [desc[0] for desc in description]
    formatted_text = ""
    for row in rows:
        row_text = ", ".join(f"{column_names[i]}: {row[i]}" for i in range(len(row)))
        formatted_text += f"{row_text}\n"
    
    return formatted_text.strip()

def format_sqlrows_to_dict(rows, description):
    if not rows:
        return {}
    
    column_names = [desc[0] for desc in description]
    formatted_dict = {}
    for row in rows:
        item = {}
        item.update({WIN_SYSINDEX_TO_COLS.get(column_names[i]): row[i] for i in range(len(row))})
        formatted_dict[item["path"]] = item
    
    return formatted_dict

def flatten(query_list):
    return [subitem for item in query_list for subitem in item]



def get_compat_osquery_schemas(version: str = "5.14.1", is_cross_platform: bool = False):
    url = f"https://raw.githubusercontent.com/osquery/osquery-site/source/src/data/osquery_schema_versions/{version}.json"
    json_response = requests.get(url).json()
    
    if is_cross_platform:
        return [x for x in json_response if all(p in x.get('platforms') for p in ['windows','darwin','linux'])]
    
    return [x for x in json_response if platform.system().lower() in x.get('platforms')]