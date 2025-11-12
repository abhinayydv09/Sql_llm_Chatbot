import streamlit as st
import requests
from tabs import llm_settings

st.set_page_config(page_title="SQL LLM Chatbot", layout="wide")

# -----------------------------
# Load previous settings if exists
# -----------------------------
import os, json
SETTINGS_FILE = "user_settings.json"

if os.path.exists(SETTINGS_FILE):
    with open(SETTINGS_FILE, "r") as f:
        saved_settings = json.load(f)
        for key, value in saved_settings.items():
            if key not in st.session_state:
                st.session_state[key] = value

# Default values if not in session_state
defaults = {
    "model_name": "meta-llama/Llama-3.1-8B-Instruct",
    "sql_dialect": "PostgreSQL",
    "hf_token": "",
    "temperature": 0.2
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# -----------------------------
# Columns layout
# -----------------------------
left_col, right_col = st.columns([5, 2])

# -----------------------------
# Left column: Main SQL generator
# -----------------------------
with left_col:
    st.title(" SQL LLM Chatbot")

    # Display current settings dynamically
    st.markdown(f"**Model:** `{st.session_state.model_name}`")
    st.markdown(f"**SQL Dialect:** `{st.session_state.sql_dialect}`")

    schema = st.text_area("Database Schema", placeholder="CREATE TABLE ...", height=150)
    user_query = st.text_area("Your Question", placeholder="Get all departments with avg salary > 50000", height=100)

    if st.button("Generate SQL"):
        if not schema.strip() or not user_query.strip():
            st.error("Please provide both schema and query!")
        elif not st.session_state.hf_token.strip():
            st.error("Please set your HuggingFace token in LLM Settings on the right!")
        else:
            try:
                payload = {
                    "schema": schema,
                    "user_query": user_query,
                    "model_name": st.session_state.model_name,
                    "sql_dialect": st.session_state.sql_dialect,
                    "temperature": st.session_state.temperature
                }
                headers = {"Authorization": f"Bearer {st.session_state.hf_token}"}
                response = requests.post("http://127.0.0.1:8000/generate_sql", json=payload, headers=headers)

                if response.status_code == 200:
                    sql_query = response.json().get("sql_query", "")
                    st.success(" Generated SQL Query:")
                    st.code(sql_query, language="sql")
                else:
                    st.error(f"Failed to generate SQL: {response.text}")

            except Exception as e:
                st.error(f"Error calling backend API: {str(e)}")

# -----------------------------
# Right column: LLM Settings
# -----------------------------
with right_col:
    llm_settings.render()
