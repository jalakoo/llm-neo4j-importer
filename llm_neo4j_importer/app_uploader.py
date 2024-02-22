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


def on_input_change():
    user_input = st.session_state.user_input
    st.session_state.past.append(user_input)
    st.session_state.generated.append("The messages from Bot\nWith new line")

def on_btn_click():
    del st.session_state.past[:]
    del st.session_state.generated[:]

def main():

    # if "UPLOADED_FILES" not in st.session_state:
    #     st.session_state["UPLOADED_FILES"] = []
    st.set_page_config(layout="wide")
    st.title('Neo4j Data Upload Demo')


    # FILE UPLOADS
    # Allow users to upload multiple files
    files = st.file_uploader("Upload files", accept_multiple_files=True)
    for file in files:
        
        # Dedupe. There is known bug in Streamlit where the same file will be tracked multiple times on. https://github.com/streamlit/streamlit/issues/4877
        # if file.name in st.session_state["UPLOADED_FILES"]:
        #     logging.debug(f'file {file.name} already uploaded. Skipping...')
        #     continue

        if type_supported(file.type) == False:
            st.error(f'File type {file.type} for {file.name} not supported')
            continue

        # TODO: Display visualization of data to import

        success = upload(file)

        if success is False:
            st.error(f"Problem uploading or file with same filename already uploaded")
            continue
    
        # st.session_state["UPLOADED_FILES"].append(file.name)
        st.success(f'File(s) uploaded')

if __name__ == "__main__":
    main()