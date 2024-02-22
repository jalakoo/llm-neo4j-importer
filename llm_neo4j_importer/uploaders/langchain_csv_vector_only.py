# from langchain.embeddings.openai import OpenAIEmbeddings
from .llm_manager import EMBEDDINGS
from langchain_community.vectorstores import Neo4jVector
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
import os
import logging

def upload(file: any) -> bool:

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    #use tempfile because CSVLoader only accepts a file_path
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        try:
            tmp_file.write(file.read())
        except Exception as _:
            try:
                tmp_file.write(file.content)
            except Exception as e:
                logging.error(f'Unable to read file {file}')
        tmp_file_path = tmp_file.name

    # Official doc: https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.csv_loader.CSVLoader.html#langchain_community.document_loaders.csv_loader.CSVLoader
    loader = CSVLoader(
        file_path=tmp_file_path, 
        encoding="utf-8", 
        csv_args={
                'delimiter': ','}
        )
    
    # For targeting particular column headers
    # csv_args={
    #     "delimiter": ",",
    #     "quotechar": '"',
    #     "fieldnames": ["MLB Team", "Payroll in millions", "Wins"],
    # },
    
    docs = loader.load()

    logging.debug(f'docs: {docs}')

    Neo4jVector.from_documents(
        docs, 
        EMBEDDINGS, 
        url=url, 
        username=username, 
        password=password)  
    
    return True