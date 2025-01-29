"""
Contains the Functionality relating to managing the connections between two nodes.
"""

class Connection:
    """
    A connection (edge) between two nodes in a graph.

    Parameters
    ----------
    node_a : Node
        The source or first node.
    node_b : Node
        The destination or second node.
    weight : float, optional
        A weight or capacity for this connection. Defaults to 1.0.

    Attributes
    ----------
    node_a : Node
        The source or first node of this connection.
    node_b : Node
        The destination or second node of this connection.
    weight : float
        Weight or capacity assigned to this connection.
    """
    def __init__(self, node_a, node_b, weight: float = 1.0):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight
