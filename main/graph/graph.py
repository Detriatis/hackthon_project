import numpy as np 
from nodes import SinkNode, SourceNode, Node
from connections import Connection

class Graph:
    def __init__(self, directed: bool = False):
        '''
        Construct a directed or undirected class

        Attributes
        ----------
        nodes : dictionary
            a dictionary of nodes added to the graph, indexed by the nodes name : str 
        connections : list 
            a list of connections between nodes in the graph : Connection
        directed : bool
            Indicate whether to make DAG or UAG 

        Methods  
        ----------
        add_node / nodes: 
            add a node or nodes to the graph 
        
        '''
        self.nodes = {}         # dict: node_id -> Node object
        self.connections = []   # list of Connection objects
        self.directed = directed
        self.adjacency = {} 

    def add_node(self, node: Node):
        self.nodes[node.node_id] = node

    def add_nodes(self, nodes: list[Node]):
        for node in nodes: 
            self.nodes[node.node_id] = node
        
    def add_connection(self, node_a_id, node_b_id, weight=1.0):
        '''
        Here node_a_id: Source Node
        Here node_b_id: Destination Node
        Weight: Parameter for loss over distance between nodes 
        '''
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
        n = len(self.nodes)
        adjacency_matrix = np.zeros((n, n))
        
        # Create an index mapping directly
        node_index = {node_id: i for i, node_id in enumerate(self.nodes.keys())}

        for connection in self.connections:
            a, b = connection.node_a.node_id, connection.node_b.node_id
            i, j = node_index[a], node_index[b]

            if self.directed:
                adjacency_matrix[i, j] = 1 if isinstance(connection.node_a, SourceNode) else 0
                adjacency_matrix[j, i] = 1 if not isinstance(connection.node_a, SourceNode) else 0
            else:
                adjacency_matrix[i, j] = adjacency_matrix[j, i] = 1 

        return adjacency_matrix, node_index
    