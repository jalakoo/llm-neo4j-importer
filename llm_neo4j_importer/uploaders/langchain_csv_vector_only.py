# from langchain.embeddings.openai import OpenAIEmbeddings
from .llm_manager import EMBEDDINGS
from langchain_community.vectorstores import Neo4jVector
from langchain.document_loaders.csv_loader import CSVLoader
import os
import tempfile
import logging

def upload(file: any) -> bool:

    # Neo4j credentials
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

    try: 
        # Official doc: https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.csv_loader.CSVLoader.html#langchain_community.document_loaders.csv_loader.CSVLoader
        loader = CSVLoader(
            file_path=tmp_file_path, 
            encoding="utf-8", 
            csv_args={
                    'delimiter': ',',
                    # "fieldnames": ["MLB Team", "Payroll in millions", "Wins"],  # optional target specific column headers
                    }
            )
        
        # Chunk up the document to smaller chunks
        docs = loader.load()

        logging.debug(f'csv docs loaded: {docs}')

        Neo4jVector.from_documents(
            docs, 
            EMBEDDINGS, 
            url=url, 
            username=username, 
            password=password)  
        
        return f"Successfully uploaded {file.name}"
    
    except Exception as e:
        return f"{e}"