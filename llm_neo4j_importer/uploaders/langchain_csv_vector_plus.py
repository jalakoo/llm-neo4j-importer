# from langchain.embeddings.openai import OpenAIEmbeddings
from .llm_manager import EMBEDDINGS
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
from .n4j_utils import add_chunk, chunk_exists, add_docs, add_document_and_chunk_connections, add_entities_relationships_to_chunk,add_tags_to_chunk, document_exists
import os
from .openai_entity_relationships_extraction import get_entities
import logging
import csv

def upload(file: any) -> bool:

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

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

    # Official doc: https://python.langchain.com/docs/integrations/document_loaders/csv
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

    # Vector
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

    # TODO: Parse each row separately?

    # for chunk in chunks:
    #     # Extract a list of tuples (entity, relationship, entity)
    #     entities = get_entities(chunk)
    
    #     # Expand around chunks with entity-relationship-entity data
    #     add_entities_relationships_to_chunk(
    #         chunk,
    #         entities,
    #         url,
    #         username,
    #         password
    #     )
    
    return True