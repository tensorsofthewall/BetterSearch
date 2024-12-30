import re

def identify_query_type(query: str) -> str:
    # Regex for identifying valid osquery queries (SQL-like)
    osquery_regex = r"^(SELECT\s+.+\s+FROM\s+\w+(\s+WHERE\s+.+)?(\s+(ORDER BY|GROUP BY)\s+\w+(\s+(ASC|DESC))?)?(\s+LIMIT\s+\d+)?;?)$"
    
    if re.match(osquery_regex, query, re.IGNORECASE):
        # SQL Query (osquery compatible)
        return "SQL"
    else:
        return "Unknown"