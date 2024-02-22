# Retrieve from streamlit secrets or .env
import streamlit as st

NEO4J_DATABASE = st.secrets["NEO4J_DATABASE"]
NEO4J_URI = st.secrets["NEO4J_URI"]
NEO4J_USERNAME = st.secrets["NEO4J_USERNAME"]
NEO4J_PASSWORD = st.secrets["NEO4J_PASSWORD"]
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
