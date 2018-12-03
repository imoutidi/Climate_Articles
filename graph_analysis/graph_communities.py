from graph_analysis import graph_tools
import community


class CommunityTool:

    def __init__(self, path_in, path_out, rel_type, ent_type):
        self.read_p = path_in
        self.write_p = path_out
        self.relation = rel_type
        self.entities = ent_type
        self.graph_toolbox = graph_tools.GraphToolBox()

    # Calculating the percentage of total graph nodes
    # on each community
    @staticmethod
    def calculate_percentages(coms):
        print("Calculating communities percentages")
        com_dict = dict()
        for key, value in coms.items():
            if value in com_dict:
                com_dict[value][0].append(key)
            else:
                com_dict[value] = [[key]]
        total_nodes = len(coms)
        for key in com_dict:
            com_dict[key].append(len(com_dict[key][0]) / total_nodes)
        return com_dict

    @staticmethod
    def create_com_sets(all_coms):
        com_sets = []
        for com_id, com_list in all_coms.items():
            com_sets.append(set(com_list[0]))
        return com_sets

    # Adds nodes that belong to overlapping communities in more than one if the
    # edges connecting it to another community are significant enough
    @staticmethod
    def reshuffle_nodes(sig_coms, graph, sig_sig_e, cmty_sets):
        # print(graph._node[0]['name'])
        new_nodes_dict = dict()
        for sig_n in sig_coms:
            new_nodes_dict[sig_n] = set()

        for com_set in cmty_sets:
            for node in com_set:
                strong_nodes = []
                neighs = graph[node]
                for neigh, weight_dict in neighs.items():
                    if weight_dict['weight'] > sig_sig_e:
                        strong_nodes.append(neigh)
                for s_node in strong_nodes:
                    for s_com in sig_coms:
                        if s_node in cmty_sets[s_com]:
                            new_nodes_dict[s_com].add(node)

        # Adding overlapping nodes int the communities
        # for s_com in sig_coms:
        #     cmty_sets[s_com] = cmty_sets[s_com].union(new_nodes_dict[s_com])
        return cmty_sets

    # Creates one independent graph for each community
    # significant overlapping nodes are split to more
    # than one communities/graphs
    def split_coms(self, coms, graph, s_s_edge):
        print("Working on splitting communities")
        sig_com_graphs = []
        insig_coms_key = []
        sig_coms_key = []
        community_sets = self.create_com_sets(coms)
        for cmnty_num, perc_nodes in coms.items():
            if perc_nodes[1] < 0.05:
                insig_coms_key.append(cmnty_num)
            else:
                sig_coms_key.append(cmnty_num)

        coms_with_overlap = self.reshuffle_nodes(sig_coms_key, graph, s_s_edge, community_sets)
        for sig_key in sig_coms_key:
            sig_com_graphs.append(graph.subgraph(list(coms_with_overlap[sig_key])))

        return sig_com_graphs

    def handle_communities(self, threshold=0):
        key_graph = self.graph_toolbox.form_graph(self.read_p, self.relation, self.entities)
        _, sig_sig_e = self.graph_toolbox.graph_edge_cleaning(key_graph, top_threshold=threshold)
        print("Working on Louvain community detection")
        communities = community.best_partition(key_graph, weight='weight')
        coms_with_perc = self.calculate_percentages(communities)
        sig_graphs = self.split_coms(coms_with_perc, key_graph, sig_sig_e)
        self.graph_toolbox.generate_gephi_graphs(sig_graphs, self.write_p, threshold, self.relation, self.entities)


if __name__ == "__main__":
    input_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Raw_Graphs/"
    output_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Communities/"
    out_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Shrinked_Graphs"
    # community_worker = CommunityTool(input_path, output_path, "Merged", "L")
    # community_worker.handle_communities(threshold=20)
    tool_box = graph_tools.GraphToolBox()
    tool_box.shrink_graph(input_path, out_path, threshold=80, relation="Merged", entities="L")
