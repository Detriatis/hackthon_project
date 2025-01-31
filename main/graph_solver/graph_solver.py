import torch.optim as optim
import matplotlib.pyplot as plt
import torch
from graph_elements.nodes import Node, SourceNode, SinkNode
from graph_elements.graph import Graph 

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class GraphSolver:
    def __init__(self, graph: Graph, T=3, epochs=1000, lambda_n=100):
        self.graph: Graph = graph
        self.epochs = epochs

        #### TODO this is incorrect: The shape is actually (S + D, S + D) as we made the assumption
        #### That all nodes could, in theory, connect to any other node. So either we need to change
        #### the construct adjacency function or the shape this code expects
        # 1) Construct adjacency
        adj, _ = self.graph.construct_adjacency()  # shape (S, D)
        self.matrix_distance = adj

        # 2) Prepare shapes
        self.S, self.D = self.matrix_distance.shape
        self.T = T

        # 3) Instead of masked_select, create a full matrix_power_allocation as a leaf Parameter
        #    The entire (S, D, T) becomes trainable
        self.matrix_power_allocation = torch.nn.Parameter(
            torch.rand((self.S, self.D, self.T), dtype=torch.float)
        )

        # 4) Build connectivity mask
        self.connectivity_mask = (self.matrix_distance != 0).float()  # shape (S, D)
        # Expand to (S, D, T)
        self.connectivity_mask_3d = self.connectivity_mask.unsqueeze(-1).expand(self.S, self.D, self.T)

        # 5) Read node data from the graph (example)
        self._build_node_tensors(graph)

        # 6) Define optimizer *directly on matrix_power_allocation*
        self.optimizer = optim.Adam([self.matrix_power_allocation], lr=0.02)
        self.losses = []

        # 7) define hyperparameters
        self.lambda_n = lambda_n



    def _build_node_tensors(self):
        # for demonstration, collect S sources and D sinks
        self.list_total_power = []
        self.list_lcoe = []
        self.list_econ_coefficient = []
        self.list_demand_profile = []
        
        for node in self.graph.nodes.values():
            if isinstance(node, SourceNode):
                self.list_total_power.append(node.total_power)
                self.list_lcoe.append(node.lcoe)
            elif isinstance(node, SinkNode):
                self.list_econ_coefficient.append(node.econ_coefficient)
                self.list_demand_profile.append(node.demand_profile)

        self.list_total_power = torch.tensor(self.list_total_power, dtype=torch.float)
        self.list_lcoe       = torch.tensor(self.list_lcoe,       dtype=torch.float)
        self.list_econ_coefficient = torch.tensor(self.list_econ_coefficient, dtype=torch.float)
        self.list_demand_profile   = torch.tensor(self.list_demand_profile,   dtype=torch.float)
        # Expect shapes: 
        #   list_total_power: (S,)
        #   list_lcoe: (S,)
        #   list_econ_coefficient: (D,)
        #   list_demand_profile: (D, T)

    def solve(self):
        for epoch in range(self.epochs):
            self.optimizer.zero_grad()

            # ----- Mask out invalid edges -----
            # Option A) Force them to zero so they don't contribute to cost
            # Option B) Multiply in the forward pass
            power_allocation_valid = self.matrix_power_allocation * self.connectivity_mask_3d

            # 1) Received power at each sink over T
            #    distance is shape (S, D), so we expand to (S, D, T)
            dist_3d = self.matrix_distance.unsqueeze(-1).expand(self.S, self.D, self.T)
            received_power = (power_allocation_valid * dist_3d).sum(dim=0)  # shape (D, T)

            # 2) Unmet demand
            U = self.list_demand_profile - received_power  # shape (D, T)

            # 3) Objective J
            # cost_term for sources
            cost_term = (self.list_lcoe * power_allocation_valid.sum(dim=1)).sum()
            # econ_term for sinks
            econ_term = self.list_econ_coefficient[:, None] * torch.nn.ReLU()(U)                     # shape (D, T)
            J = torch.sum(econ_term) + torch.sum(cost_term)

            # 4) Constraint penalties
            # supply violation: sum across D, T for each source -> compare to total_power
            supply_violations = power_allocation_valid.sum(dim=1) - self.list_total_power[:, None]  
            L_supply = self.lambda_n * torch.sum(torch.relu(supply_violations)**2)

            # non-negativity penalty (on power_allocation + on U if we don't want negative U)
            L_neg = self.lambda_n * torch.sum(torch.relu(-power_allocation_valid)**2 + torch.relu(-U)**2)

            L_total = J + L_supply + L_neg
            L_total.backward()

            self.optimizer.step()
            self.losses.append(L_total.item())

            if epoch % 200 == 0:
                print(f"Epoch {epoch}, Loss: {L_total.item():.4f}")

        return self.matrix_power_allocation.detach(), self.losses