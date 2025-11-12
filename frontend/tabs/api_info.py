import streamlit as st

def render():
    st.header("API Connection Info")
    st.write(
        """
        You can connect to the **SQL LLM Chatbot API** to generate SQL queries from natural language questions.

        ### Endpoint
        **POST** `http://localhost:8000/generate_sql`

        ### Required Headers
        The API requires a HuggingFace token passed in the `Authorization` header:

        ```
        Authorization: Bearer YOUR_HF_TOKEN
        ```

        ### Request Body (JSON)
        | Field         | Type    | Description |
        |---------------|---------|-------------|
        | schema        | string  | Database schema (tables & columns) |
        | user_query    | string  | Natural language question about the schema |
        | model_name    | string  | Name of the LLM model to use |
        | sql_dialect   | string  | SQL dialect (e.g., PostgreSQL, MySQL, SQLite) |
        | temperature   | float   | Sampling temperature for LLM (optional, default 0.2) |

        Example JSON payload:

        ```json
        {
            "schema": "CREATE TABLE employees (id INT, name TEXT, salary INT, department INT);",
            "user_query": "Get all departments with average salary > 50000",
            "model_name": "meta-llama/Llama-3.1-8B-Instruct",
            "sql_dialect": "PostgreSQL",
            "temperature": 0.2
        }
        ```

        ### Example Python Usage
        ```python
        import requests

        url = "http://localhost:8000/generate_sql"
        payload = {
            "schema": "CREATE TABLE employees (id INT, name TEXT, salary INT, department INT);",
            "user_query": "Get all departments with average salary > 50000",
            "model_name": "meta-llama/Llama-3.1-8B-Instruct",
            "sql_dialect": "PostgreSQL",
            "temperature": 0.2
        }
        headers = {
            "Authorization": "Bearer YOUR_HF_TOKEN"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Generated SQL:")
            print(response.json()["sql_query"])
        else:
            print("Error:", response.text)
        ```

        This example demonstrates how to:
        1. Pass the HuggingFace token securely.
        2. Send the schema and question to the API.
        3. Receive a cleaned SQL query as output.
        """
    )
