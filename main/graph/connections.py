class Connection:
    def __init__(self, node_a, node_b, efficiency=1.0, directed=False):
        self.node_a = node_a
        self.node_b = node_b
        self.efficiency = efficiency
        self.directed = directed