import streamlit as st
import os
import json
import requests

SETTINGS_FILE = "user_settings.json"

def render():
    st.header(" LLM Settings")

    # -----------------------------
    # Initialize session_state defaults if not already set
    # -----------------------------
    defaults = {
        "hf_token": "",
        "model_name": "meta-llama/Llama-3.1-8B-Instruct",
        "sql_dialect": "PostgreSQL",
        "temperature": 0.2
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

    # -----------------------------
    # Load previous settings silently
    # -----------------------------
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            saved_settings = json.load(f)
            for key, value in saved_settings.items():
                if key not in st.session_state or not st.session_state[key]:
                    st.session_state[key] = value

    # -----------------------------
    # Reset Settings button
    # -----------------------------
    if st.button("Reset Settings"):
        preserved_hf = st.session_state.get("hf_token", "")  # optionally preserve token
        st.session_state.update(defaults)
        st.session_state["hf_token"] = preserved_hf
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        st.success("Settings reset to defaults!")
        st.rerun()

    # -----------------------------
    # HuggingFace Token Input
    # -----------------------------
    st.text_input("HuggingFace Token", key="hf_token", type="password")

    # Placeholder for HF token status / warning below the input
    token_warning_placeholder = st.empty()

    # -----------------------------
    # HF token validity check
    # -----------------------------
    hf_token = st.session_state.get("hf_token", "")
    if hf_token:
        try:
            resp = requests.get(
                "https://api-inference.huggingface.co/models/meta-llama/Llama-3.1-8B-Instruct",
                headers={"Authorization": f"Bearer {hf_token}"},
                timeout=5
            )
            if resp.status_code == 401:
                token_warning_placeholder.warning(" Your HuggingFace token has expired or is invalid. Please update it.")
            else:
                token_warning_placeholder.success(" HuggingFace token is valid.")
        except Exception as e:
            token_warning_placeholder.warning(f" Unable to verify token: {e}")
    else:
        token_warning_placeholder.info("Please enter your HuggingFace token above.")

    # -----------------------------
    # Model selection
    # -----------------------------
    st.selectbox(
        "Select Model",
        ["meta-llama/Llama-3.1-8B-Instruct"],
        key="model_name"
    )

    # -----------------------------
    # SQL Dialect selection
    # -----------------------------
    st.selectbox(
        "SQL Dialect",
        ["PostgreSQL", "MySQL", "SQLite"],
        key="sql_dialect"
    )

    # -----------------------------
    # Temperature slider
    # -----------------------------
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        step=0.05,
        key="temperature"
    )

    # -----------------------------
    # Save Settings button
    # -----------------------------
    if st.button("Save Settings"):
        if not st.session_state.hf_token.strip():
            token_warning_placeholder.warning(" Please enter a HuggingFace token before saving!")
        else:
            settings = {
                "hf_token": st.session_state.hf_token,
                "model_name": st.session_state.model_name,
                "sql_dialect": st.session_state.sql_dialect,
                "temperature": st.session_state.temperature
            }
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)
            token_warning_placeholder.success("Settings saved successfully!")
            st.rerun()
