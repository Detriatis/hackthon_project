import numpy as np 
from nodes import SinkNode, SourceNode, Node
from connections import Connection

class Graph:
    def __init__(self, directed = False):
        self.nodes = {}         # dict: node_id -> Node object
        self.connections = []   # list of Connection objects
        self.directed = directed

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node

    def add_nodes(self, nodes: list[Node]):
        for node in nodes: 
            self.nodes[node.node_id] = node
        
    def add_connection(self, node_a_id, node_b_id, weight=1.0):
        if node_a_id not in self.nodes or node_b_id not in self.nodes:
            raise ValueError("Node not found in graph.")
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]
        
        connection = Connection(node_a, node_b, weight)
        self.connections.append(connection)
        # Optionally update adjacency in the node objects themselves
        node_a.connections.append(connection)
        if not self.directed:
            # Undirected graph might also add same connection to node_b's adjacency
            node_b.connections.append(connection)
    
    def get_node(self, node_id):
        return self.nodes.get(node_id)
    
    def get_neighbors(self, node_id):
        """If you store adjacency in node.connections, just return the connected nodes."""
        return self.nodes.get(node_id).connections
    
    def construct_adjacency(self):
        adjacency_matrix = np.zeros((len(self.nodes), len(self.nodes)))
        node_index = {} 
        for i, (node_id, node) in enumerate(self.nodes.items()):
            node_index[node_id] = i 

        for connection in self.connections:
            node_a_id = connection.node_a.node_id
            node_b_id = connection.node_b.node_id
            
            node_a_idx = node_index[node_a_id]
            node_b_idx = node_index[node_b_id]

            if self.directed: 
                if isinstance(connection.node_a, SourceNode):
                    adjacency_matrix[node_a_idx, node_b_idx] = 1
                else: 
                    adjacency_matrix[node_b_idx, node_a_idx] = 1
            
            if not self.directed:
                adjacency_matrix[node_b_idx, node_a_idx] = 1 
                adjacency_matrix[node_a_idx, node_b_idx] = 1 

        return adjacency_matrix, node_index

            
         
