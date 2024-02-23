from neo4j import GraphDatabase
from langchain_community.vectorstores import Neo4jVector
from langchain_community.graphs import Neo4jGraph
from neo4j.exceptions import ClientError
from pydantic import BaseModel
import logging
import os

neo4j_log = logging.getLogger("neo4j")
neo4j_log.setLevel(logging.ERROR)

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

def add_docs(
    docs: list[any], # list[Documents]
    embeddings: any,
    url: str,
    username: str,
    password: str    
):
    
    # Official API Doc: https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.neo4j_vector.Neo4jVector.html#langchain_community.vectorstores.neo4j_vector.Neo4jVector

    # Target Neo4j DB requires APOC (included in Aura, needs to be enabled on desktop)

    Neo4jVector.from_documents(
        docs, 
        embeddings, 
        url=url, 
        username=username, 
        password=password)  
     
def add_entities_relationships_to_chunk(
          chunk: str,
          triples: list[list],
          url: str,
          username: str,
          password: str,
          database : str = "neo4j"
):

    if len(triples) == 0:
         logging.info(f'Skipping chunk with no triples: {chunk}, triples: {triples}')
         return
    
    # UNWIND will not work because we need to dynamically assign a relationship type. Types and Node labels can not be set within an unwind context or via params!

    # query = """
    #         MATCH (c:Chunk {text:$text})
    #         WITH c
    #         UNWIND $triples AS triple
    #         MERGE (f:Entity {name:triple[0]})
    #         MERGE (t:Entity {name:triple[2]})
    #         MERGE (f)-[:`{triple[1]}`]->(t)
    #         """

    query = """MATCH (c:Chunk {text:$text})"""

    # NOTE: Double quotes for string property values, back-tick for enclosing node label or relationship type names!
    for i, triple in enumerate(triples):
            if len(triple) != 3:
                 logging.warning(f"Skipping invalid triple: {triple}")
                 continue
            query += f"""
            MERGE (f{i}:Entity {{name:"{triple[0]}"}})
            MERGE (t{i}:Entity {{name:"{triple[2]}"}})
            MERGE (f{i})-[:`{triple[1]}`]->(t{i})
            MERGE (c)-[:MENTIONS]->(f{i})
            """
    params = {
        "text": chunk
    } 
    
    logging.debug(f'Final query:\n{query}')

    try:
        graph = Neo4jGraph(
            url=url,
            username=username,
            password=password,
            database=database
        )
        graph.query(
            query,
            params
        )
    except Exception as e:
        logging.error(f'Problem adding triple entity-relationships to chuck: {e}')

# As labels instead of node name properties
# def add_entities_relationships_to_chunk(
#           chunk: str,
#           triples: list[list],
#           url: str,
#           username: str,
#           password: str,
#           database : str = "neo4j"
# ):

#     # Unwind will not work for generating labels dynamically
#     query = """
#             MATCH (c:Chunk {text:$text})
#             """
#     for i, triple in enumerate(triples):
#             if len(triple) != 3:
#                  logging.warning(f"Skipping invalid triple: {triple}")
#                  continue
#             query += f"""
#             MERGE (f{i}:`{triple[0]}`)
#             MERGE (t{i}: `{triple[2]}`)
#             MERGE (f{i})-[:`{triple[1]}`]->(t{i})
#             """
#     params = {
#         "text": chunk
#     } 
#     try:
#         graph = Neo4jGraph(
#             url=url,
#             username=username,
#             password=password,
#             database=database
#         )
#         graph.query(
#             query,
#             params
#         )
#     except Exception as e:
#         logging.error(f'Problem adding triple entity-relationships to chuck: {e}')

def add_nodes_to_doc(
          filename: str,
          nodes: list[list[(str, str)]],
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

        query = """MERGE (d:Document {name:$filename})"""

        # NOTE: Double quotes for string property values, back-tick for enclosing node label or relationship type names!
        for i, row in enumerate(nodes):
            query += f"""MERGE (r{i}:Row {{name:"{filename}_{i}"}})"""
            for rpi, tuple in enumerate(row):
                if len(tuple) != 2:
                    logging.warning(f"Skipping invalid node: {tuple}")
                    continue
                query += f"""
                MERGE (n{i}_{rpi}:`{tuple[0]}` {{name:"{tuple[1]}"}})
                MERGE (n{i}_{rpi})-[:FROM]->(r{i})
                """
            # Connect each row to the document
            query += f"""MERGE (r{i})-[:IN]-(d)"""
        params = {
            "filename": filename
        } 
        try:
            graph.query(
                query,
                params
            )
        except ClientError:
            pass

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