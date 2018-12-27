import csv
from datetime import timedelta
import networkx as nx
import os


class GraphToolBox:

    @staticmethod
    def read_edges_csv(filename):
        edge_list = list()
        csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

        next(csv_reader)
        for row in csv_reader:
            edge_list.append((int(row[0]), int(row[1]), float(row[2])))

        return edge_list

    @staticmethod
    def read_nodes_csv(filename):
        node_dict = dict()
        csv_reader = csv.reader(open(filename), delimiter=',', quotechar='"')

        next(csv_reader)
        for idx, row in enumerate(csv_reader):
            node_dict[int(row[0])] = row[1]
            # bug found and corrected keep next line for review
            # node_dict[idx] = row[1]
        return node_dict

    @staticmethod
    def date_range(start_date, end_date):
        for n in range(int((end_date - start_date).days)):
            yield start_date + timedelta(n)

    # All graphs have the same gephi format
    def form_graph(self, path, r_type="", e_type=""):
        print("Creating Graph from .csv")
        nodes_dict = self.read_nodes_csv(path + r_type + "/Nodes" + e_type + ".csv")
        edges_list = self.read_edges_csv(path + r_type + "/Edges" + e_type + ".csv")

        # Adding nodes to graph
        c_graph = nx.Graph()
        for key in nodes_dict:
            c_graph.add_node(key, name=nodes_dict[key])
        c_graph.add_weighted_edges_from(edges_list)

        # TODO debug code delete when you are done
        # with open("/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Debug/nodes", "w") as node_out:
        #     for a, b in c_graph.nodes(data=True):
        #         if 'name' in b:
        #             node_out.write(str(a) + b['name'] + "\n")
        #         else:
        #             node_out.write(str(a) + "found one\n")

        return c_graph

    def only_path_form_graph(self, edge_path, node_path):
        print("Creating Graph from .csv")
        nodes_dict = self.read_nodes_csv(node_path)
        edges_list = self.read_edges_csv(edge_path)

        # Adding nodes to graph
        c_graph = nx.Graph()
        for key in nodes_dict:
            c_graph.add_node(key, name=nodes_dict[key])
        c_graph.add_weighted_edges_from(edges_list)

        return c_graph

    # The distribution of the edges weights are heavy tailed so we assume that they are close
    # enough to power law distributions and that the top 20% of them are the most significant
    # The top_threshold represents the percentage of the graph edge that we are going to keep.
    @staticmethod
    def graph_edge_cleaning(graph, top_threshold=0):
        print("Cleaning insignificant edges and isolated nodes")
        all_weights = []
        for edge in graph.edges.data():
            all_weights.append(tuple([edge[0], edge[1], edge[2]['weight']]))
        # Sorting based on the third tuple element (weights)
        all_weights.sort(key=lambda tup: tup[2])
        edge_num = len(all_weights)

        # We will keep the top threshold % of the edges
        # converting % to fraction. If the threshold is
        # 0 we are keeping the whole graph
        if top_threshold == 0:
            denominator = 1
        else:
            denominator = 100 / top_threshold

        bottom_twenty = int(edge_num / denominator)
        bottom_edges = all_weights[:-bottom_twenty]
        bb = len(bottom_edges)
        for edge_tuple in bottom_edges:
            graph.remove_edge(edge_tuple[0], edge_tuple[1])
        # removing nodes with no edges
        # the list is a workaround for a bug:
        # https://stackoverflow.com/questions/48820586/removing-isolated-vertices-in-networkx
        graph.remove_nodes_from(list(nx.isolates(graph)))
        # lastsig edges exist for removing unimportant edges from the graph
        last_sig_edge = all_weights[-bottom_twenty][2]
        # last_sig_sig_edge exist for overlapping communities splits
        # It will be used to compare edges of overlapping nodes if an edge has a big enough
        # value (>last_sig_sig_edge)the node will be part of both communities that
        # the edge connects
        last_sig_sig_edge = all_weights[-int(bottom_twenty / denominator)][2]
        return last_sig_edge, last_sig_sig_edge

    @staticmethod
    def generate_gephi_graphs(graph_list, path, thresh=0, r_type="", e_type=""):
        print("Generating Gephi graphs.")
        # Checking if the directories exist and if
        # not we create them
        relation_path = path + "/" + r_type + "_" + str(thresh)
        if not os.path.exists(relation_path):
            os.makedirs(relation_path)
        path = relation_path
        entity_path = path + "/" + e_type
        if not os.path.exists(entity_path):
            os.makedirs(entity_path)
        path = entity_path

        for idx, graph in enumerate(graph_list):
            # a = [x for x in graph.nodes.data()]
            # Creating gephi node CSV file
            with open(path + "/Nodes" + "_" + str(idx) + ".csv", 'w') as node_file:
                node_file.write('id,label\n')
                for node in graph.nodes.data():
                    node_file.write(str(node[0]) + "," + node[1]['name'] + "\n")

            with open(path + "/Edges" + "_" + str(idx) + ".csv", 'w') as edge_file:
                edge_file.write('Source,Target,Weight\n')
                for edge in graph.edges.data():
                    edge_file.write(str(edge[0]) + "," + str(edge[1]) + "," + str(edge[2]['weight']) + "\n")

    def shrink_graph(self, read_path, write_path, threshold=0, relation="", entities=""):
        graph = self.form_graph(read_path, relation, entities)
        self.graph_edge_cleaning(graph, top_threshold=threshold)
        self.generate_gephi_graphs([graph], write_path, threshold, relation, entities)
        return graph
