# from langchain.embeddings.openai import OpenAIEmbeddings
from .llm_manager import EMBEDDINGS
from .n4j_utils import add_docs, add_document_and_chunk_connections
from langchain.document_loaders.csv_loader import CSVLoader
import logging
import os
import tempfile


def upload(file: any) -> bool:

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    # Uncomment to prevent duplicate imports
    # if document_exists(
    #     url=url,
    #     username=username,
    #     password =password,
    #     filename=file.name
    # ) is True:
    #     logging.info(f'File {file} already uploaded')
    #     return False

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
        # Official doc: https://python.langchain.com/docs/integrations/document_loaders/csv
        loader = CSVLoader(
            file_path=tmp_file_path, 
            encoding="utf-8", 
            csv_args={
                    'delimiter': ','}
            )
        
        docs = loader.load()

        # Abstracted Vector call
        add_docs(
            docs, 
            EMBEDDINGS, 
            url, 
            username, 
            password)

        chunks = [d.page_content for d in docs]

        # Simple (Chunk)-[:CHILD_OF]->(Document) relationship
        add_document_and_chunk_connections(
            filename=file.name,
            full_text = "",
            chunks = chunks,
            url=url,
            username=username,
            password = password
        )
        return f"Successfully uploaded {file.name}"
    
    except Exception as e:
        return f"{e}"