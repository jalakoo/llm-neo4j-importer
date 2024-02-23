from upload_utils import upload, upload_url, type_supported
import logging
import os
import re
import streamlit as st
import streamlit.components.v1 as components
import sys

# Logging setup
logging.basicConfig(filename='llm_neo4j_importer.log', encoding='utf-8', level=logging.DEBUG)
root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)

# Streamlit Setup
st.set_page_config(layout="wide")
st.title('Neo4j Data Upload Demo')

# Uploading content from links
url_links = st.text_input("URL link(s)")
links = re.split(', |/n | ', url_links)
for link in links:
    if link is not None and link != "":
        logging.debug(f'url_link: {link}')
        upload_url_result = upload_url(link)
        st.info(upload_url_result)

# Upload local files
files = st.file_uploader("Upload files", accept_multiple_files=True)

for file in files:
    
    # There is known bug in Streamlit where the same file will be tracked multiple times on. https://github.com/streamlit/streamlit/issues/4877 - Dedupe attempts using session state here or switching to a single file upload has NO effect

    if type_supported(file.type) == False:
        st.error(f'File type {file.type} for {file.name} not supported')
        continue

    result_msg = upload(file)
    
    st.info(result_msg)