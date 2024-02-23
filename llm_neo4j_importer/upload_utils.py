from uploaders.langchain_pdf import upload as load_pdf
from uploaders.langchain_txt import upload as load_txt
from uploaders.langchain_csv_vector_plus import upload as load_csv_vector_plus
from uploaders.langchain_csv_vector_only import upload as load_csv_vector_only
from uploaders.langchain_csv_graph import upload as load_csv_graph
from uploaders.langchain_image import upload as load_image
import requests
import logging

def type_supported(type:str) -> bool:
    if type in ["application/pdf", "text/csv", "text/plain", "image/jpeg", "image/png"]:
        return True
    return False

def upload(file:any) -> bool:

    # file maybe None, UploadFile or list of UploadFile.
    # See streamlit's doc for more info: https://docs.streamlit.io/library/api-reference/widgets/st.file_uploader

    # More info on acceptable mime types: https://www.iana.org/assignments/media-types/media-types.xhtml#text
    if file.type == "application/pdf":
        return load_pdf(file)
    elif file.type == "text/csv":
        load_csv_graph(file)
        load_csv_vector_plus(file)
        return True
    
    elif file.type == "text/plain":
        return load_txt(file)
    elif file.type == "image/jpeg" or file.type == "image/png":
        return load_image(file)
    else:
        logging.error(f'file type not supported')
        return False

def process_url(url:str) -> bool:
    response = requests.get(url)
    type = response.headers['Content-Type']
    if type == "application/pdf":
        load_pdf(response.content)
    else:
        return False
    return True