import torch

# -------------------------------------------------------------------------
# 1) Create a minimal Graph class with a `construct_adjacency` method
#    and some nodes. This is purely illustrative, adapt to your real code.
# -------------------------------------------------------------------------
class Node:
    """
    Represents a node in the graph. Has different attributes depending on
    whether it's a source or a sink node.
    """
    def __init__(self, node_type, total_power=None, lcoe=None,
                 econ_coefficient=None, demand_profile=None):
        self.node_type = node_type
        self.total_power = total_power
        self.lcoe = lcoe
        self.econ_coefficient = econ_coefficient
        self.demand_profile = demand_profile

class SimpleGraph:
    """
    A tiny graph with 2 source nodes, 2 sink nodes.
    construct_adjacency() will return a 2D adjacency matrix of shape (S, D)
    indicating whether source i can supply to sink j.
    """
    def __init__(self):
        # Create four nodes: 2 sources, 2 sinks
        # Source node attributes:
        #   total_power: how much can this source provide (MW)
        #   lcoe: cost coefficient for generating power
        # Sink node attributes:
        #   econ_coefficient: penalty or economic coefficient
        #   demand_profile: how much does this sink need over T time steps
        self.nodes = [
            Node(node_type="source", total_power=50.0, lcoe=10.0),
            Node(node_type="source", total_power=30.0, lcoe=8.0),
            Node(node_type="sink", econ_coefficient=25.0,
                 demand_profile=[20.0, 25.0, 15.0]),  # T=3 steps
            Node(node_type="sink", econ_coefficient=36.0,
                 demand_profile=[15.0, 20.0, 10.0])   # T=3 steps
        ]

    def construct_adjacency(self):
        """
        Return:
          - adjacency matrix of shape (num_sources, num_sinks)
          - optionally some additional info if needed

        For this example, let's assume:
         - Source 0 can supply both sinks (row 0 => [1, 1])
         - Source 1 can supply only the second sink (row 1 => [0, 1])
        """
        import torch
        # We'll treat the "source" nodes as S=2, the "sink" nodes as D=2
        adjacency = torch.tensor([[1.0, 1.0],
                                  [0.0, 1.0]], dtype=torch.float)
        return adjacency, None  # or return any other needed info

import torch

# class Node:
#     """
#     Represents a node in the graph. Has different attributes depending on
#     whether it's a source or a sink node.
#     """
#     def __init__(self, node_type, total_power=None, lcoe=None,
#                  econ_coefficient=None, demand_profile=None):
#         self.node_type = node_type
#         self.total_power = total_power
#         self.lcoe = lcoe
#         self.econ_coefficient = econ_coefficient
#         self.demand_profile = demand_profile


class LargeGraph:
    """
    A more complicated graph with 3 source nodes and 4 sink nodes.

    The adjacency is shape (3,4) indicating where edges exist from each
    of the 3 sources to each of the 4 sinks.
    """
    def __init__(self):
        # ----------------------------------------------------------------------
        # 1) Define Node Data
        #    We have 3 sources (S=3), 4 sinks (D=4)
        # ----------------------------------------------------------------------

        # Source nodes:
        #   total_power = how much power this source can supply
        #   lcoe        = cost coefficient
        source_nodes = [
            Node(node_type="source", total_power=80.0,  lcoe=5.0),
            Node(node_type="source", total_power=60.0,  lcoe=8.0),
            Node(node_type="source", total_power=100.0, lcoe=6.0),
        ]

        # Sink nodes:
        #   econ_coefficient = economic penalty or incentive factor
        #   demand_profile   = needed power each time step
        # We'll have 5 time steps (T=5)
        sink_nodes = [
            Node(node_type="sink", econ_coefficient=24.0,
                 demand_profile=[30, 35, 40, 25, 30]),
            Node(node_type="sink", econ_coefficient=27.0,
                 demand_profile=[20, 20, 20, 20, 20]),
            Node(node_type="sink", econ_coefficient=25.5,
                 demand_profile=[50, 60, 55, 60, 65]),
            Node(node_type="sink", econ_coefficient=26.5,
                 demand_profile=[10, 15, 10, 12, 10])
        ]

        # Combine source + sink in self.nodes
        self.nodes = source_nodes + sink_nodes

    def construct_adjacency(self):
        """
        Return a 3×4 adjacency matrix for the sources→sinks.
        The value 1.0 indicates a valid edge (source can supply that sink).
        The value 0.0 indicates no direct supply possible.
        """
        import torch
        # We have 3 sources, 4 sinks => shape (3,4)
        adjacency = torch.tensor([
            [1.0, 1.0, 1.0, 0.0],  # source 0 can supply sinks 0,1,2
            [0.0, 1.0, 0.0, 1.0],  # source 1 can supply sinks 1,3
            [1.0, 0.0, 1.0, 1.0],  # source 2 can supply sinks 0,2,3
        ], dtype=torch.float)

        # Return adjacency plus possibly None or other info
        return adjacency, None



# -------------------------------------------------------------------------
# 2) Import the graph_solver class code
#    (Paste the runnable solver code you have previously.)
# -------------------------------------------------------------------------
import torch.optim as optim
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
import torch
import torch.optim as optim

class GraphSolver:
    def __init__(self, graph, T=3, epochs=1000, lambda_n=100):
        self.graph = graph
        self.epochs = epochs

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



    def _build_node_tensors(self, graph):
        # for demonstration, collect S sources and D sinks
        self.list_total_power = []
        self.list_lcoe = []
        self.list_econ_coefficient = []
        self.list_demand_profile = []

        for node in graph.nodes:
            if node.node_type == "source":
                self.list_total_power.append(node.total_power)
                self.list_lcoe.append(node.lcoe)
            elif node.node_type == "sink":
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
            cost_term = self.list_lcoe[:, None] * power_allocation_valid.sum(dim=1)  # shape (S, T)
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

# -------------------------------------------------------------------------
# 3) Instantiate the graph and run the solver
# -------------------------------------------------------------------------
if __name__ == "__main__":
    # Create the simple graph
    # test_graph = SimpleGraph()
    test_graph = LargeGraph()
    # Create the solver instance with T=3 (matching demand profiles)
    # solver = GraphSolver(test_graph, T=3, epochs=1000)
    solver = GraphSolver(test_graph, T=5, epochs=10000)
    # Solve the optimization problem
    final_allocation, losses = solver.solve()

    power_allocation_valid = final_allocation * solver.connectivity_mask_3d

    # 1) Received power at each sink over T
    #    distance is shape (S, D), so we expand to (S, D, T)
    dist_3d = solver.matrix_distance.unsqueeze(-1).expand(solver.S, solver.D, solver.T)
    received_power = (power_allocation_valid * dist_3d).sum(dim=0)  # shape (D, T)

    # 2) Unmet demand
    U = solver.list_demand_profile - received_power  # shape (D, T)


    # If you want to see final results directly:
    print("\nFinal allocation:\n", power_allocation_valid.detach().cpu().numpy())
    print(f"Unmet demand: {U}")
    print("\nLoss history (first 10 values):\n", losses[:10])
    plt.plot(losses)
    plt.xlabel("Epoch")
    plt.ylabel("Loss")
    plt.title("Loss History")
    plt.savefig("loss_plot/loss_history.png", dpi=200)
    plt.show()
