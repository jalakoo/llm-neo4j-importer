from streamlit_agraph import agraph, Node, Edge, Config
# from pydantic import BaseModel
import logging

# class Triples(BaseModel):
#     from_node_label : str
#     relationship_type : str
#     to_node_label : str

# def convert_to_triples_list(list: list[str]) -> list[Triples]:
#     triples_list = []
#     try:
#         for triple_str in list:
#             parts = triple_str.split(',')
#             if len(parts) == 3:
#                 from_node_label, relationship_type, to_node_label = map(str.strip, parts)
#                 triples_list.append(Triples(from_node_label=from_node_label, relationship_type=relationship_type, to_node_label=to_node_label))
#             else:
#                 logging.warning(f"Skipping malformed triple: {triple_str}")
#     except Exception as e:
#         logging.error(f'Error occurred while converting to triples: {e}')
#     return triples_list

def convert_list(list_of_lists: list[list[str]]) -> tuple[list[str],list[str]]:

    nodes = set()
    result_edges = []

    for item in list_of_lists:
        # Each should be a tuple of 3 items, node-edge-node
        n1 = item[0]
        r = item[1]
        n2 = item[2]

        # Standardize casing
        r = r.upper()
        n1 = n1.title()
        n2 = n2.title()

        nodes.add(n1)
        nodes.add(n2) 

        edge = Edge(source=n1, target=n2, label=r)
        result_edges.append(edge)

    result_nodes = []
    for node_label in list(nodes):
        node = Node(id=node_label, label=node_label)
        result_nodes.append(node)

    logging.debug(f'Nodes returning: {result_nodes}')
    logging.debug(f'Edges returning: {result_edges}')

    return result_nodes, result_edges