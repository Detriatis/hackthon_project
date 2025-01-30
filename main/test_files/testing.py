from graph_elements.connections import Connection 
from graph_elements.nodes import SourceNode, SinkNode, Solar, Wind, Gas, Node
from graph_elements.graph import Graph


def main():
    source_solar = Solar('solar1', 24, [0, 1]) 
    source_wind = Wind('wind1', 24, [1, 0], offshore=True)
    sink = SinkNode('city1', 24, [0, 0]) 
    graph = Graph(directed=True)
    
    # Adding a node to the graph, nodes are stored as key value pairs, where the
    # key is the node id and the value is the Node object
    graph.add_node(sink)
    graph.add_node(source_solar)
    graph.add_node(source_wind)
    # When you add a connection you create a connection object, the method takes 
    # the node id you specified for each node. The connection object contains node_a - source node
    # and node_b - sink node. You also specify a weight which defines the coefficient for the power transmission
    graph.add_connection(source_solar.node_id, sink.node_id, weight=0.25)
    graph.add_connection(source_wind.node_id, sink.node_id, weight=1)
    # Calling construct adjacency will iterate all connections to return an adjacency array 
    # the array [i, j] is formatted so [i] is the source, and [j] is the sink
    # this function also returns a node index of key value pairs, where the key is the node id
    # and the index indicates its index in the array
    adjaceny, node_index = graph.construct_adjacency()
    # Any node can be retrieved by calling get node, with the node id, on the graph object 
    node = graph.get_node(list(node_index.keys())[1])
    # nodes also store all their connections as an attribute, if directed connections are only stored
    # as outgoing connections i.e. source nodes store connections but sink nodes generally wont
    id = node.connections[0].node_b.node_id

if __name__ == '__main__': 
    main() 