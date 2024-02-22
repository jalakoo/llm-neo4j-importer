import streamlit as st
import streamlit.components.v1 as components
from upload_utils_vector_only import upload, type_supported
import logging

logging.basicConfig(filename='llm_neo4j_importer.log', encoding='utf-8', level=logging.DEBUG)

def main():

    st.set_page_config(layout="wide")
    st.title('Neo4j Data Upload Demo')

    # Allow users to upload multiple files
    files = st.file_uploader("Upload files", accept_multiple_files=True)
    for file in files:

        if type_supported(file.type) == False:
            st.error(f'File type {file.type} for {file.name} not supported')
            continue
    
        success = upload(file)

        if success is False:
            st.error(f"Problem uploading or file with same filename already uploaded")
            continue
    
        st.success(f'File(s) uploaded')

if __name__ == "__main__":
    main()