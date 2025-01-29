import numpy as np 
from nodes import SinkNode, SourceNode, Node
from connections import Connection

class Graph:
    def __init__(self):
        self.nodes = {}         # dict: node_id -> Node object
        self.connections = []   # list of Connection objects
    
    def add_node(self, node: Node):
        self.nodes[node.node_id] = node

    def add_nodes(self, nodes: list[Node]):
        for node in nodes: 
            self.nodes[node.node_id] = node
        
    def add_connection(self, node_a_id, node_b_id, weight=1.0, directed=False):
        if node_a_id not in self.nodes or node_b_id not in self.nodes:
            raise ValueError("Node not found in graph.")
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]
        
        connection = Connection(node_a, node_b, weight, directed)
        self.connections.append(connection)
        
        # Optionally update adjacency in the node objects themselves
        node_a.connections.append(connection)
        if not directed:
            # Undirected graph might also add same connection to node_b's adjacency
            node_b.connections.append(connection)
    
    def get_node(self, node_id):
        return self.nodes.get(node_id)
    
    def get_neighbors(self, node_id):
        """If you store adjacency in node.connections, just return the connected nodes."""
        return self.nodes.get(node_id).connections
