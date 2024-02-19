# TODO: Use LangChain Agent to interface with vector + graphCypher options#!/usr/bin/env python

from rag import rag_agent
from rag.llm_manager import CALLBACKS
from gpt4all import GPT4All
import streamlit as st
import logging

# Configure
model = GPT4All("mistral-7b-instruct-v0.1.Q4_0.gguf")
st.set_page_config(layout='wide')
placeholder = st.empty()
emoji_feedback = st.empty()
user_placeholder = st.empty()

# Initialize message history
if "messages" not in st.session_state:
    st.session_state.messages = [
      {"role": "ai", "content": f"This chatbot is powered by GPT4All + Mistral + Neo4j"}, 
    ]

# Display chat messages from history on app rerun
with placeholder.container():
  for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"], unsafe_allow_html=True)

user_input = st.chat_input(placeholder="Ask questions regarding the source data", key="user_input")

if user_input:
  with user_placeholder.container():
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
      st.markdown(user_input)

    with st.chat_message("ai"):

      # Agent response
      with st.spinner('...'):

        message_placeholder = st.empty()
        thought_container = st.container()

        # For displaying chain of thought - this callback handler appears to only works with the deprecated initialize_agent option (see rag_agent.py)
        # st_callback = StreamlitCallbackHandler(
        #   parent_container= thought_container,
        #   expand_new_thoughts=False
        # )
        # StreamlitCcallbackHandler api doc: https://api.python.langchain.com/en/latest/callbacks/langchain_community.callbacks.streamlit.streamlit_callback_handler.StreamlitCallbackHandler.html

        # content = model.generate(user_input)

        content = rag_agent.get_results(
          question=user_input,
          callbacks=CALLBACKS
        )

        new_message = {"role": "ai", "content": content}
        st.session_state.messages.append(new_message)

      message_placeholder.markdown(content)
  
  # Reinsert user chat input if sample quick select was previously used.
#   if "sample" in st.session_state and st.session_state["sample"] is not None:
#     st.session_state["sample"] = None
#     user_input = st.chat_input(placeholder="Ask question on the SEC Filings", key="user_input")

#   emoji_feedback = st.empty()