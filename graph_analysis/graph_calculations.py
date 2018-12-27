import time
import networkx as nx

from graph_analysis import graph_tools
from tool_pack import tools


def metrics_calc(entity_type, f_path):
    entity_names = list()
    nodes_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/" \
                 "Shrinked_Graphs/Sentence_10/PLO/Nodes_0.csv"
    edges_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/" \
                 "Shrinked_Graphs/Sentence_10/PLO/Edges_0.csv"
    out_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Shrinked_Graphs/Sentence_10/Metrics/"
    g_tool = graph_tools.GraphToolBox()

    # Loading the graph from CSV files
    # climate_graph = g_tool.form_graph(f_path, "Merged", entity_type)
    climate_graph = g_tool.only_path_form_graph(edges_path, nodes_path)

    for idx, node in climate_graph.nodes.items():
        entity_names.append(node['name'])

    start_time = time.time()
    # Calculating node metrics
    degree = nx.degree(climate_graph, nbunch=None)
    print("---Degree %s seconds ---" % (time.time() - start_time))

    w_degree = nx.degree(climate_graph, nbunch=None, weight='weight')
    print("---Weigheted Degree %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    page_rank = nx.pagerank(climate_graph, alpha=0.85, personalization=None, max_iter=100,
                            tol=1e-06, nstart=None, weight='weight', dangling=None)
    print("---Page Rank %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    betweeness_cen = nx.betweenness_centrality(climate_graph, k=None, normalized=True,
                                               weight='weight', endpoints=False, seed=None)
    print("---Betweeness %s seconds ---" % (time.time() - start_time))
    start_time = time.time()

    closeness_cen = nx.closeness_centrality(climate_graph, u=None, distance=None)
    print("---Closeness %s seconds ---" % (time.time() - start_time))
    # start_time = time.time()
    # TODO replace closeness centrality with Katz centrality
    # issues with max iterations
    # katz_cen = nx.katz_centrality(climate_graph, alpha=0.1, beta=1.0, max_iter=1000, tol=1e-06,
    #                               nstart=None, normalized=True, weight='weight')
    # print("---Katz %s seconds ---" % (time.time() - start_time))
    # for idx, node in climate_graph.nodes.items():
    #     # If the entity exists we simple add the tuple with the metric values
    #     if node['name'] in entity_values:
    #         entity_values[node['name']].append((0, 0, w_degree[idx], 0))
    tools.save_pickle(out_path + "Entity_Names.pickle", entity_names)
    tools.save_pickle(out_path + "Degree.pickle", degree)
    tools.save_pickle(out_path + "Weighted_Degree.pickle", w_degree)
    tools.save_pickle(out_path + "Betweeness_Centrality.pickle", betweeness_cen)
    tools.save_pickle(out_path + "Page_Rank.pickle", page_rank)
    tools.save_pickle(out_path + "Closeness_Centrality.pickle", closeness_cen)
    # tools.save_pickle(out_path + "Katz_Centrality.pickle", katz_cen)


if __name__ == "__main__":
    file_path = "/home/iraklis/PycharmProjects/climate_change/IO_files/Graphs/"

    # start_time = time.time()
    metrics_calc("L", file_path)

    # print("--- %s seconds ---" % (time.time() - start_time))

