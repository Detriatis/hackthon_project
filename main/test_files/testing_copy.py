from graph_elements.connections import Connection 
from graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph_elements.graph import Graph
from graph_solver.graph_solver import GraphSolver
from graph_elements.node_generator import generate_nodes

def main():
    T = 24
    num_solar, num_wind, num_gas, num_sinks = 10, 10, 10, 5  # Setting number of each node type

    # Create the graph
    graph = Graph(directed=True)

    # Generate and add nodes dynamically
    source_nodes, sink_nodes = generate_nodes(graph, num_solar, num_wind, num_gas, num_sinks,24)

    # Print adjacency matrix
    adjacency, node_index = graph.construct_adjacency()
    print("Adjacency Matrix:\n", adjacency)

    # Iterate over nodes and print relevant data
    for node_id, node in graph.nodes.items():
        if isinstance(node, SourceNode):
            power_series = node.get_power_output_series()
            print(f"Source {node_id}: Power Series {power_series}")
        if isinstance(node, SinkNode):
            demand_series = node.demand_profile
            print(f"Sink {node_id}: Demand Series {demand_series}")

    # Initialize and run the solver
    solver = GraphSolver(graph, T=T)
    power_allocations, _ = solver.solve()
    print(f"Power allocations: {power_allocations}")

if __name__ == '__main__': 
    main()
