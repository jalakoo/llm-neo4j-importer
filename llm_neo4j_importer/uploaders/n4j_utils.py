from neo4j import GraphDatabase
from langchain_community.vectorstores import Neo4jVector
from langchain_community.graphs import Neo4jGraph
from neo4j.exceptions import ClientError
from pydantic import BaseModel
import logging
import os

# More info at: https://api.python.langchain.com/en/latest/graphs/langchain.graphs.neo4j_graph.Neo4jGraph.html#

def execute_query(url: str,
                  username: str,
                  password: str,
                  query, 
                  params={}, 
                  database: str = "neo4j"):
    logging.debug(f'Using host: {url}, user: {username} to execute query: {query}')
    # Returns a tuple of records, summary, keys
    with GraphDatabase.driver(url, auth=(username, password)) as driver:
        return driver.execute_query(query, params, database=database)

def document_exists(url: str,
                    username: str,
                    password: str,
                    filename: str,
                    database: str = "neo4j",
                    ) -> bool:
    query = """
            MATCH (d:Document) 
            WHERE d.name = $filename
            RETURN d.name AS filename
            """
    params = {
        "filename": filename,
    }
    records, summary, keys = execute_query(url, username, password, query, params, database)
    logging.debug(f'document exists results: records: {records}, summary: {summary}, keys: {keys}')
    return len(records) > 0

def chunk_exists(
        url: str,
        username: str,
        password: str,
        text: str,
        database : str = "neo4j") -> bool:
    query = """
            MATCH (d:Chunck) 
            WHERE d.text = $text
            RETURN d
            """
    params = {
        "text": text
    }
    records, summary, keys = execute_query(url, username, password, query, params, database)
    logging.debug(f'document exists results: records: {records}, summary: {summary}, keys: {keys}')
    return len(records) > 0     

def add_chunk(
        text: str,
        embeddings: any,
        url: str,
        username: str,
        password: str    
    ):
        Neo4jVector.from_documents(
            [text], 
            embeddings, 
            url=url, 
            username=username, 
            password=password)

def add_chunks(
    chunks: list[str],
    embeddings: any,
    url: str,
    username: str,
    password: str    
):
    Neo4jVector.from_documents(
        chunks, 
        embeddings, 
        url=url, 
        username=username, 
        password=password)  

def add_tags_to_chunk(
          chunk: str,
          tags: list[str],
          url: str,
          username: str,
          password: str,
          database: str = "neo4j"):
        graph = Neo4jGraph(
            url=url,
            username=username,
            password=password,
            database=database
        )
        query = """
                MATCH (c:Chunk {text:$text})
                WITH c
                UNWIND $tags AS tag
                MERGE (t:Tag {name:tag})
                MERGE (c)-[:TAGGED]->(t)
                """
        params = {
            "text": chunk,
            "tags": tags
        }
        try:
            graph.query(
                query,
                params
            )
        except ClientError:
            pass
     
def add_tags_to_document(
          filename: str,
          tags: list[str],
          url: str,
          username: str,
          password: str,
          database: str = "neo4j"):
        graph = Neo4jGraph(
            url=url,
            username=username,
            password=password,
            database=database
        )
        query = """
                MATCH (c:Document {name: $filename})
                WITH c
                UNWIND $tags AS tag
                MERGE (t:Tag {name:tag})
                MERGE (c)-[:TAGGED]->(t)
                """
        params = {
            "filename": filename,
            "tags": tags
        }
        try:
            graph.query(
                query,
                params
            )
        except ClientError:
            pass

def add_document(
          filename: str,
          full_text: str,
          neo4j_url: str | None = None,
          neo4j_username: str | None = None,
          neo4j_password: str | None = None,
    ):
        
        # Pull neo4j credentials from .env if available
        if neo4j_url is None:
            neo4j_url = os.getenv("NEO4J_URI", None)
        if neo4j_username is None:
            neo4j_username = os.getenv("NEO4J_USERNAME", None)
        if neo4j_password is None:
            neo4j_password = os.getenv("NEO4J_PASSWORD", None)

        # Raise error otherwise
        if neo4j_url is None:
             raise Exception("Neo4j URI not found")
        

        graph = Neo4jGraph(
            url=neo4j_url,
            username=neo4j_username,
            password=neo4j_password
        )
        query = """
                MERGE (doc:Document {name:$filename, text: $full_text})
                """
        params = {
            "filename": filename,
            "full_text": full_text
        }
        try:
            graph.query(
                query,
                params
            )
        except ClientError:
            pass
     
     
def add_document_and_chunk_connections(
          filename: str,
          full_text: str,
          chunks: list[str],
          url: str,
          username: str,
          password: str,
    ):
        graph = Neo4jGraph(
            url=url,
            username=username,
            password=password
        )
        query = """
                MERGE (doc:Document {name:$filename, text: $full_text})
                WITH doc
                UNWIND $children AS child
                MATCH (c:Chunk {text:child})
                MERGE (c)-[:CHILD_OF]->(doc)
                """
        params = {
            "filename": filename,
            "full_text": full_text,
            "children": chunks
        }
        try:
            graph.query(
                query,
                params
            )
        except ClientError:
            pass