import streamlit as st
import os
import json

SETTINGS_FILE = "user_settings.json"

def render():
    st.header(" LLM Settings")

    # -----------------------------
    # Load previous settings silently
    # -----------------------------
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            saved_settings = json.load(f)
            for key, value in saved_settings.items():
                if key not in st.session_state:
                    st.session_state[key] = value

    # -----------------------------
    # Reset to defaults button
    # -----------------------------
    if st.button("Reset Settings"):
        preserved_hf = st.session_state.get("hf_token", "")  # Preserve token if exists
        st.session_state.update({
            "model_name": "meta-llama/Llama-3.1-8B-Instruct",
            "sql_dialect": "PostgreSQL",
            "temperature": 0.2,
            "hf_token": preserved_hf
        })
        if os.path.exists(SETTINGS_FILE):
            os.remove(SETTINGS_FILE)
        st.success("Settings reset to defaults!")
        st.rerun()

    # -----------------------------
    # HuggingFace Token Input
    # -----------------------------
    st.text_input(
        "HuggingFace Token",
        value=st.session_state.get("hf_token", ""),
        key="hf_token",
        type="password"
    )

    # -----------------------------
    # Model selection
    # -----------------------------
    st.selectbox(
        "Select Model",
        ["meta-llama/Llama-3.1-8B-Instruct",],
        index=["meta-llama/Llama-3.1-8B-Instruct",
               ].index(st.session_state.model_name),
        key="model_name"
    )

    # -----------------------------
    # SQL Dialect selection
    # -----------------------------
    st.selectbox(
        "SQL Dialect",
        ["PostgreSQL", "MySQL", "SQLite"],
        index=["PostgreSQL", "MySQL", "SQLite"].index(st.session_state.sql_dialect),
        key="sql_dialect"
    )

    # -----------------------------
    # Temperature slider
    # -----------------------------
    st.slider(
        "Temperature",
        0.0, 1.0,
        value=st.session_state.get("temperature", 0.2),
        step=0.05,
        key="temperature"
    )

    # -----------------------------
    # Save settings button
    # -----------------------------
    if st.button(" Save Settings"):
        if not st.session_state.hf_token.strip():
            st.warning("Please enter a HuggingFace token before saving!")
        else:
            settings = {
                "hf_token": st.session_state.hf_token,
                "model_name": st.session_state.model_name,
                "sql_dialect": st.session_state.sql_dialect,
                "temperature": st.session_state.temperature
            }
            with open(SETTINGS_FILE, "w") as f:
                json.dump(settings, f)
            st.success(" Settings saved successfully!")
            st.rerun()
