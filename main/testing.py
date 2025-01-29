'''
Test Docstring
'''


from .graph_elements.connections import Connection
from .graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from .graph_elements.graph import Graph

def main():
    source_solar = Solar('solar1', '10', '10', '10') 
    source_wind = Wind('wind1', '10', '10', '10')
    sink = SinkNode('city1', '10', '10') 
    graph = Graph(directed=False)

    graph.add_node(sink)
    graph.add_node(source_solar)
    graph.add_node(source_wind)
    graph.add_connection(source_solar.node_id, sink.node_id, weight=0.25)
    graph.add_connection(source_wind.node_id, sink.node_id, weight=1)
    graph, node_index = graph.construct_adjacency()
    print(graph) 
    print(node_index) 
if __name__ == '__main__': 
    main() 