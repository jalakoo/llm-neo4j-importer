from langchain_community.document_loaders import YoutubeLoader
from .llm_manager import EMBEDDINGS
from .n4j_utils import add_chunk, chunk_exists, add_chunks, add_document_and_chunk_connections, add_tags_to_chunk, document_exists
import os

def is_youtube_url(url: str) -> bool:
    """
    Checks if a given url is a valid youtube url.
    """
    if url[:23] == "https://www.youtube.com/":
        return True
    return False

def upload_url(url: str):

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    # API doc: https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.youtube.YoutubeLoader.html#langchain_community.document_loaders.youtube.YoutubeLoader
    
    loader = YoutubeLoader.from_youtube_url(
        url, add_video_info=False
    )

    docs = loader.load()

    add_chunks(
        docs, 
        EMBEDDINGS, 
        url, 
        username, 
        password)

    add_document_and_chunk_connections(
        filename=url,
        full_text = "",
        chunks = [d.page_content for d in docs],
        url=url,
        username=username,
        password = password
    )