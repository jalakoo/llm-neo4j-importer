from langchain_community.document_loaders import YoutubeLoader
from langchain.text_splitter import CharacterTextSplitter
from .llm_manager import EMBEDDINGS
from .n4j_utils import add_chunk, chunk_exists, add_docs, add_document_and_chunk_connections, add_tags_to_chunk, document_exists, add_video_and_chunk_connections
import os

def is_youtube_url(url: str) -> bool:
    """
    Checks if a given url is a valid youtube url.
    """
    if url.startswith("https://www.youtube.com/"):
        return True
    return False

def upload_url_link(url_link: str):

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    if document_exists(
        url=url,
        username=username,
        password=password,
        filename = url_link
        ) is True:
        return "Ignoring duplicate upload"
    
    # API doc: https://api.python.langchain.com/en/latest/document_loaders/langchain_community.document_loaders.youtube.YoutubeLoader.html#langchain_community.document_loaders.youtube.YoutubeLoader
    
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=100)
    
    try: 
        loader = YoutubeLoader.from_youtube_url(
            url_link, 
            add_video_info=False
        )

        docs = loader.load_and_split(text_splitter)

        add_docs(
            docs, 
            EMBEDDINGS, 
            url, 
            username, 
            password)

        add_video_and_chunk_connections(
            filename=url_link,
            full_text = "",
            chunks = [d.page_content for d in docs],
            url=url,
            username=username,
            password = password
        )
        return f"Successfully processed {url_link}"
    
    except Exception as e:
        return e