"""
Contains the Functionality relating to managing the connections between two nodes.
"""
from graph_elements.nodes import Node, SourceNode, SinkNode
from scipy.spatial.distance import euclidean
import numpy as np 
from typing import Callable

import numpy as np
from scipy.spatial.distance import cdist

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

    def __init__(self, node_a: Node, node_b: Node, 
             power_capacity: float):
         
        self.node_a = node_a
        self.node_b = node_b
        self.power_capacity = power_capacity
        self.power = 0.0

        # Compute the power efficiency factor using the provided weight function (transmission_loss_weight)
        self.weight = self.transmission_loss_weight()

    def transmission_loss_weight(self) -> float:
        """
        Computes the weight based on power transmission losses:
        - Power converter loss at source: 0.7% to 0.8% (randomized)
        - Distance-based loss: 1% per 100 km 
        Ref for both: https://www.nationalgrid.com/sites/default/files/documents/13784-High%20Voltage%20Direct%20Current%20Electricity%20%E2%80%93%20technical%20information.pdf

        Parameters
        ----------
        node_a : Node
            The source or first node.
        node_b : Node
            The destination or second node.

        Returns
        -------
        float
            The weight representing power efficiency factor (0 to 1).
        """
        # Distance-based loss (1% per 100 km)
        distance = euclidean(np.array(self.node_a.cartesian_coordinates), np.array(self.node_b.cartesian_coordinates))  # in meters
        distance_loss_factor = 1 - (0.01 * (distance / 100_000))  # 1% per 100 km

        # Converter efficiency at the source (random between 99.2% and 99.3%)
        converter_efficiency = np.random.uniform(0.992, 0.993)  # Random value between 0.992 and 0.993

        # Final power efficiency factor (apply converter loss first, then distance loss)
        total_efficiency = converter_efficiency * distance_loss_factor

        # Ensure efficiency never goes negative
        return max(total_efficiency, 0)