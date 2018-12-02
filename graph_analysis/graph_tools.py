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
            node_dict[idx] = row[1]
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

        return c_graph

    # The distribution of the edges weights are heavy tailed so we assume that they are close
    # enough to power law distributions and that the top 20% of them are the most significant
    # so far this approach works better with top_threshold = 20
    @staticmethod
    def graph_edge_cleaning(graph, top_threshold=0):
        print("Cleaning insignificant edges and isolated nodes")
        all_weights = []
        for edge in graph.edges.data():
            all_weights.append(tuple([edge[0], edge[1], edge[2]['weight']]))
        # Sorting based on the third tuple element (weights)
        all_weights.sort(key=lambda tup: tup[2])
        edge_num = len(all_weights)

        # We will keep the top threshold% of the edges
        # converting % to fraction
        if top_threshold == 0:
            denominator = 1
        else:
            denominator = 100 / top_threshold

        top_twenty = int(edge_num / denominator)
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

    @staticmethod
    def generate_gephi_graphs(graph_list, path, thresh=0, r_type="", e_type=""):
        print("Generating Gephi graphs.")
        # Checking if the directories exist and if
        # not we create them
        if not os.path.exists(path + "/" + r_type + "_" + str(thresh)):
            os.makedirs(path + "/" + r_type + "_" + str(thresh))
        path = path + "/" + r_type + "_" + str(thresh)
        if not os.path.exists(path + "/" + e_type):
            os.makedirs(path + "/" + e_type)
        path = path + "/" + e_type

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
