import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import agraph_utils
import logging

config = Config(height=400, width=1000, directed=True)

test = [["Chickens","eat","seeds"],["people", "eat", "chickens"]]

# Define a callback function to handle node and edge clicks
def handle_click(data):
    if data["type"] == "node":
        node_id = data["id"]
        print("Node clicked:", node_id)
    elif data["type"] == "edge":
        edge_id = data["id"]
        print("Edge clicked:", edge_id)

# Convert response to agraph nodes and edges
try:
    nodes, edges = agraph_utils.convert_list(test)
    agraph(nodes=nodes, 
        edges=edges, 
        config=config) 

except Exception as e:
    logging.error(f'Problem converting response to agraph nodes and edges. Error: {e}')
    st.error(f'Problem converting prompt to graph. Please try again or rephrase the prompt')

# Inject JavaScript for capturing clicks
# js_code = """
# <script type="text/javascript">
#     const graph = document.getElementById("graph1");
#     const nodes = graph.getElementsByClassName("nodes");
#     const edges = graph.getElementsByClassName("edge");

#     for (let node of nodes) {
#         node.addEventListener("click", function(event) {
#             event.stopPropagation(); // Prevent the event from bubbling up
#             const nodeId = node.getAttribute("data-id");
#             console.log("Node clicked:", nodeId);
#         });
#     }

#     for (let edge of edges) {
#         edge.addEventListener("click", function(event) {
#             event.stopPropagation(); // Prevent the event from bubbling up
#             const edgeId = edge.getAttribute("data-id");
#             console.log("Edge clicked:", edgeId);
#         });
#     }

#     document.addEventListener("dblclick", function(event) {
#         event.preventDefault(); // Prevent the default action of double-clicking
#     });
# </script>
# """
# st.write(js_code, unsafe_allow_html=True)
