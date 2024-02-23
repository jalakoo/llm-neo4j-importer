from langchain_community.document_loaders import YoutubeLoader
from .llm_manager import EMBEDDINGS
from .n4j_utils import add_chunk, chunk_exists, add_docs, add_document_and_chunk_connections, add_tags_to_chunk, document_exists
import os

def is_youtube_url(url: str) -> bool:
    """
    Checks if a given url is a valid youtube url.
    """
    if url.startswith("https://www.youtube.com/"):
        return True
    return False

def upload_url_link(url: str):

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    # API doc: https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.youtube.YoutubeLoader.html#langchain_community.document_loaders.youtube.YoutubeLoader
    
    try: 
        loader = YoutubeLoader.from_youtube_url(
            url, add_video_info=False
        )

        docs = loader.load()

        add_docs(
            docs, 
            EMBEDDINGS, 
            url, 
            username, 
            password)
        return "Success"
    except Exception as e:
        return e