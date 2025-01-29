from connections import Connection
from nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph import Graph

def main():
    source_solar = Solar('solar1', '10', '10', '10') 
    source_wind = Wind('wind1', '10', '10', '10')
    sink = SinkNode('city1', '10', '10') 
    graph = Graph(directed=False)

    graph.add_node(sink)
    graph.add_node(source_solar)
    graph.add_node(source_wind)
    graph.add_connection(source_solar.node_id, sink.node_id, weight=1)
    graph.add_connection(source_wind.node_id, sink.node_id, weight=1)

    adjacency, node_idx = graph.construct_adjacency()
    
if __name__ == '__main__': 
    main() 