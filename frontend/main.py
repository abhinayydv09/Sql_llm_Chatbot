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
# Custom CSS for smaller font in text areas
# -----------------------------
st.markdown("""
    <style>
    textarea {
        font-size: 13px !important;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# Columns layout
# -----------------------------
left_col, right_col = st.columns([5, 2])

# -----------------------------
# Left column: Main SQL generator
# -----------------------------
with left_col:
    st.title("SQL LLM Chatbot")

    # Display current settings dynamically
    st.markdown(f"**Model:** `{st.session_state.model_name}`")
    st.markdown(f"**SQL Dialect:** `{st.session_state.sql_dialect}`")

    # Database Schema input (larger)
    schema = st.text_area(
        "Database Schema",
        placeholder="Enter Database Schema ...",
        height=250,
        max_chars=2000
    )

    # User Question(s) input (larger)
    user_query = st.text_area(
        "Your Question(s)",
        placeholder="Questions ...",
        height=180,
        max_chars=1500
    )

    # Placeholder for token warning below inputs
    hf_warning_placeholder = st.empty()

    # Generate SQL button
    if st.button("Generate SQL"):
        if not schema.strip() or not user_query.strip():
            st.error("Please provide both schema and query!")
        elif not st.session_state.hf_token.strip():
            hf_warning_placeholder.warning("⚠️ Please enter your HuggingFace token above to generate SQL!")
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

                    if sql_query.strip():
                        st.success("Generated SQL Queries:")
                        # Split multiple queries by semicolon
                        raw_queries = sql_query.split(";")
                        queries = []
                        for q in raw_queries:
                            cleaned_q = q.replace("```sql", "").replace("```", "").strip()
                            if cleaned_q:
                                if not cleaned_q.endswith(";"):
                                    cleaned_q += ";"
                                queries.append(cleaned_q)

                        for i, q in enumerate(queries, 1):
                            st.markdown(f"**Query {i}:**")
                            st.code(q, language="sql")
                    else:
                        st.info("No SQL generated.")
                elif response.status_code == 401:
                    hf_warning_placeholder.warning("⚠️ HuggingFace token expired or invalid! Please update it.")
                else:
                    st.error(f"Failed to generate SQL: {response.text}")

            except Exception as e:
                st.error(f"Error calling backend API: {str(e)}")

# -----------------------------
# Right column: LLM Settings
# -----------------------------
with right_col:
    llm_settings.render()
