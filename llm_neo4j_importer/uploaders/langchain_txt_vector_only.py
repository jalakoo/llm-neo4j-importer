from langchain.docstore.document import Document
# from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.graphs import Neo4jGraph
from langchain_community.vectorstores import Neo4jVector
import os
import logging
from neo4j.exceptions import ClientError
from .llm_manager import EMBEDDINGS
from .tag_generator import get_tags
from .langchain_entity_relationships import get_entities
from .n4j_utils import add_docs, add_tags_to_chunk, add_document_and_chunk_connections,document_exists

def upload(
        file: any) -> bool:
    """
    Uploads a text file to a Neo4j database.

    Args:
        neo4j_credits: Tuple containing the hostname, username, and password of the target Neo4j instance

        nodes: A dictionary of objects to upload. Each key is a unique node label and contains a list of records as dictionary objects.
    
    Raises:
        Exceptions if data is not in the correct format or if the upload fails.
    """
    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    try:
        content = file.read()
    except Exception as _:
        try:
            content = file.content
        except Exception as e:
            logging.error(f'Could not read file {file}')
    
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=100)
    docs = [Document(page_content=x) for x in text_splitter.split_text(content.decode())]

    Neo4jVector.from_documents(
        docs, 
        EMBEDDINGS, 
        url=url, 
        username=username, 
        password=password)  

    return True