from upload_utils import upload, type_supported
import logging
import os
import streamlit as st
import streamlit.components.v1 as components
import sys

logging.basicConfig(filename='llm_neo4j_importer.log', encoding='utf-8', level=logging.DEBUG)

root = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
root.addHandler(handler)

st.set_page_config(layout="wide")
st.title('Neo4j Data Upload Demo')

# Allow users to upload multiple files
files = st.file_uploader("Upload files", accept_multiple_files=True)

for file in files:
    
    # There is known bug in Streamlit where the same file will be tracked multiple times on. https://github.com/streamlit/streamlit/issues/4877 - Dedupe attempts using session state here or switching to a single file upload has NO effect

    if type_supported(file.type) == False:
        st.error(f'File type {file.type} for {file.name} not supported')
        continue

    success = upload(file)

    if success is False:
        st.error(f"Problem uploading or file with same filename already uploaded")
        continue

    st.success(f'File(s) uploaded')