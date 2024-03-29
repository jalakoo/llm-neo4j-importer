from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.document_loaders.csv_loader import CSVLoader
import tempfile
from n4j_utils import add_chunk, chunk_exists, add_chunks, add_document_and_chunk_connections, add_tags_to_chunk, document_exists
import os
from tag_generator import get_tags
import logging

def upload(file: any) -> bool:

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USER")
    password = os.getenv("NEO4J_PASSWORD")

    if document_exists(
        url=url,
        username=username,
        password =password,
        filename=file.name
    ) is True:
        logging.info(f'File {file} already uploaded')
        return False

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

    loader = CSVLoader(file_path=tmp_file_path, encoding="utf-8", csv_args={
                'delimiter': ','})
    
    docs = loader.load()
    embeddings = OpenAIEmbeddings()

    logging.debug(f'docs: {docs}')

    add_chunks(
        docs, 
        embeddings, 
        url, 
        username, 
        password)

    add_document_and_chunk_connections(
        filename=file.name,
        full_text = "",
        chunks = [d.page_content for d in docs],
        url=url,
        username=username,
        password = password
    )

    # Adding tags

    for doc in docs:
        tags = get_tags(doc.page_content)
        add_tags_to_chunk(
            doc.page_content,
            tags,
            url,
            username,
            password
        )
    
    return True