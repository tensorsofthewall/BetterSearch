<|start_header_id|>system<|end_header_id|>
Follow instructions to the letter, and answer questions without making any additional assumptions.
<|begin_of_text|><|start_header_id|>user<|end_header_id|>

Generate a Windows Search SQL query to answer this question: `{user_question}`
- If the question cannot be answered given the database schema, return "I do not know". Follow the database schema strictly.
- If the question requires additional information that might not be available in the database, return "I do not know".
- recall that the current date and time in YYYY-MM-DD HH:MM:SS format is {date_time}
- Use TOP instead of LIMIT in the SQL query.

DDL statements:
{table_metadata_string}

Generate a valid Windows Search SQL query that best answers the question {user_question}.<|eot_id|><|start_header_id|>assistant<|end_header_id|>

I will reflect on the user's request before answering the question.

I was asked to generate a SQL query for this question: {user_question}

With this in mind, here is the Windows Search SQL query that best answers the question while only using appropriate tables and columns from the DDL statements:
```sql