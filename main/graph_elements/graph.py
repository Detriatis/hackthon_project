"""
This module provides the Graph class for constructing and managing
directed or undirected graphs of Node objects and their Connections.
"""

import numpy as np
from .nodes import SinkNode, SourceNode, Node
from .connections import Connection

class Graph:
    """
    A directed or undirected graph of nodes and connections.

    Parameters
    ----------
    directed : bool, optional
        If True, construct a directed graph; otherwise undirected.
        Defaults to False.

    Attributes
    ----------
    nodes : dict of str -> Node
        A dictionary of node objects, keyed by their node_id.
    connections : list of Connection
        A list of Connection objects between nodes.
    directed : bool
        Indicates whether the graph is directed.
    adjacency : dict
        (Optional) Dictionary for any adjacency structures or custom tracking.
    """

    def __init__(self, directed: bool = False):
        self.nodes = {}
        self.connections = []
        self.directed = directed
        self.adjacency = {}

    def add_node(self, node: Node):
        """
        Add a single node to the graph.

        Parameters
        ----------
        node : Node
            A node object to be added.

        Returns
        -------
        None
        """
        self.nodes[node.node_id] = node

    def add_nodes(self, nodes: list[Node]):
        """
        Add multiple nodes to the graph.

        Parameters
        ----------
        nodes : list of Node
            A list of node objects to be added.

        Returns
        -------
        None
        """
        for node in nodes:
            self.nodes[node.node_id] = node

    def add_connection(self, node_a_id, node_b_id, weight=1.0):
        """
        Add a connection between two existing nodes in the graph.

        Parameters
        ----------
        node_a_id : str
            The source node's ID.
        node_b_id : str
            The destination node's ID.
        weight : float, optional
            A parameter indicating, for instance, the "cost" or "capacity"
            of the connection. Defaults to 1.0.

        Raises
        ------
        ValueError
            If either node_a_id or node_b_id is not found in the graph.

        Returns
        -------
        None
        """
        if node_a_id not in self.nodes or node_b_id not in self.nodes:
            raise ValueError("Node not found in the graph.")
        node_a = self.nodes[node_a_id]
        node_b = self.nodes[node_b_id]

        connection = Connection(node_a, node_b, weight)
        self.connections.append(connection)

        # Update adjacency in each node
        node_a.connections.append(connection)
        if not self.directed:
            # In undirected graphs, we also record the connection on node_b
            node_b.connections.append(connection)

    def get_node(self, node_id: str) -> Node:
        """
        Retrieve a node object by its ID.

        Parameters
        ----------
        node_id : str
            The ID of the node to retrieve.

        Returns
        -------
        Node or None
            The node object if found, otherwise None.
        """
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id: str) -> list[Connection]:
        """
        Retrieve all connections for a given node.

        Parameters
        ----------
        node_id : str
            The ID of the node whose neighbors to retrieve.

        Returns
        -------
        list of Connection
            A list of connections from the specified node.

        Raises
        ------
        KeyError
            If the node_id does not exist in the graph.
        """
        node = self.nodes[node_id]  # Will raise KeyError if missing
        return node.connections

    def construct_adjacency(self):
        """
        Construct an adjacency matrix representing the graph.

        For each connection, the matrix entry [i, j] is set to the weight
        if the graph is directed or to the weight in both [i, j] and [j, i]
        if undirected.

        Returns
        -------
        adjacency_matrix : np.ndarray
            A 2D NumPy array where rows and columns are indexed by nodes.
        node_index : dict of str -> int
            A mapping from node IDs to their row/column index in the matrix.
        """
        n = len(self.nodes)
        adjacency_matrix = np.zeros((n, n))

        # Create an index mapping
        node_index = {node_id: i for i, node_id in enumerate(self.nodes.keys())}

        for connection in self.connections:
            w = connection.weight
            a_id = connection.node_a.node_id
            b_id = connection.node_b.node_id
            i, j = node_index[a_id], node_index[b_id]

            if self.directed:
                # Optional logic for directed weighting
                adjacency_matrix[i, j] = w if isinstance(connection.node_a, SourceNode) else 0
                adjacency_matrix[j, i] = w if not isinstance(connection.node_a, SourceNode) else 0
            else:
                adjacency_matrix[i, j] = w
                adjacency_matrix[j, i] = w

        return adjacency_matrix, node_index

    def power_dispersion_matrices(self): 
        adjacency_matrix, node_index = self.construct_adjacency()
        power_matrix = np.zeros_like(adjacency_matrix)
        for node_id, i in node_index.values():
            node = self.get_node(node_id) 
            if isinstance(node, SourceNode): 
                connections = node.connections
            else: 
                pass 

            for connection in connections: 
                p, sink_node = connection.transmit_power(node)
                j = node_index[sink_node.node_id]
                
                power_matrix[i, j] = p

        return power_matrix 