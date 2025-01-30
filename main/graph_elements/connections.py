"""
Contains the Functionality relating to managing the connections between two nodes.
"""
from .nodes import Node, SourceNode, SinkNode

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
    power_capacity: float, optional
        A power limit for this connection. Defaults to 0.0

    Attributes
    ----------
    node_a : Node
        The source or first node of this connection.
    node_b : Node
        The destination or second node of this connection.
    weight : float
        Weight or capacity assigned to this connection.
    power_capacity: float
        Power capacity of this connection.
    power: float
        Current power being channeled by connection.
    """

    def __init__(self, node_a: Node, node_b: Node, weight: float = 1.0, power_capacity: float = 0.0):
        self.node_a = node_a
        self.node_b = node_b
        self.weight = weight
        self.power_capacity = power_capacity
        self.power = 0.0

    def transmit_power(self, node: Node):
        if self.node_a.node_id == node.node_id:
            source_node = self.node_a 
            sink_node = self.node_b
        
        elif self.node_b.node_id == node.node_id: 
            source_node = self.node_b
            sink_node = self.node_a 

        else: 
            raise TypeError('Node is not in the connection')
        
        P = source_node.query_power(sink_node)
        sink_node.transmit_power(P)
        self.power += P 

        return P, sink_node        
