# test_llm.py
import os
from dotenv import load_dotenv
from backend.llm_handler import LLMHandler
from backend.sql_utils import clean_sql

# Load environment variables
load_dotenv("backend/.env")

# Get token
hf_token = os.getenv("HF_TOKEN")
model_name = os.getenv("MODEL_NAME")

if not hf_token:
    raise ValueError("❌ HF_TOKEN not found in .env file!")

# Initialize handler
llm = LLMHandler(hf_token=hf_token, model_name=model_name)

# Example schema and user query
schema = """
employees(id INT, name TEXT, department TEXT, salary INT);
departments(id INT, department_name TEXT);
"""

user_query = "List all departments with average salary greater than 50000."

# Generate SQL
sql_query = llm.generate_sql(schema=schema, user_query=user_query, sql_dialect="PostgreSQL", temp = 0.2)
sql_query = clean_sql(sql_query)
print("\n🧠 Generated SQL Query:\n")
print(sql_query)
