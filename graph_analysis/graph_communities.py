import networkx as nx
import csv
import community    # package name = python-louvain
import os


# The distribution of the edges weights are heavy tailed so we assume that they are close enough to
# power law distributions and that the top 20% of them are the most significant
# so far tis approach works better with top_threshold = 20
def graph_edge_cleaning(graph, top_threshold=20):
    all_weights = []
    for edge in graph.edges.data():
        all_weights.append(tuple([edge[0], edge[1], edge[2]['weight']]))
    # Sorting based on the third tuple element (weights)
    all_weights.sort(key=lambda tup: tup[2])
    edge_num = len(all_weights)
    # We will keep the top 20% of the edges
    top_twenty = int(edge_num / 5)
    bottom_edges = all_weights[:-top_twenty]
    for edge_tuple in bottom_edges:
        graph.remove_edge(edge_tuple[0], edge_tuple[1])
    # removing nodes with no edges
    # the list is a workaround for a bug:
    # https://stackoverflow.com/questions/48820586/removing-isolated-vertices-in-networkx
    graph.remove_nodes_from(list(nx.isolates(graph)))
    # sig edges exist for removing unimportant edges from the graph
    # sig sig edges exist for overlapping communities splits
    last_sig_edge = all_weights[-top_twenty][2]
    last_sig_sig_edge = all_weights[-int(top_twenty / top_threshold)][2]
    return last_sig_edge, last_sig_sig_edge