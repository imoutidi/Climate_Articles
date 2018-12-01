import csv
from datetime import timedelta
import networkx as nx


class GraphTool:
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
    def form_graph(self, r_type, e_type, path):

        nodes_dict = self.read_nodes_csv(path + r_type + "/Nodes" + e_type + ".csv")
        edges_list = self.read_edges_csv(path + r_type + "/Edges" + e_type + ".csv")

        # Adding nodes to graph
        c_graph = nx.Graph()
        for key in nodes_dict:
            c_graph.add_node(key, name=nodes_dict[key])
        c_graph.add_weighted_edges_from(edges_list)

        return c_graph
