import pickle
import networkx as nx

from ToolPack import tools
from Graph_Analysis import graph_tools


def write_dict(out_dict, name):
    with open("/home/iraklis/PycharmProjects/AllTheNews/Pivot_Files/Debug_Files/"
              + name + ".txt", 'w') as out_file:
        for key, value in out_dict.items():
            # if len(value) != 51:
            #     print("The " + key + "Entity has not 51 list elements")
            out_file.write(str(key) + " " + str(len(value)) + " " + str(value) + '\n')



# def write_list(out_list, name):



def pickle_to_file(path, struct_type, file_name):
    # loading file
    load_day_dict_list = open(path, "rb")
    pickle_file = pickle.load(load_day_dict_list)
    load_day_dict_list.close()
    if struct_type == "Dict":
        write_dict(pickle_file, file_name)
    elif struct_type == "List":
        print("TODO implement a list writer")


def check_nodes(entity_type, f_path):
    entity_values = dict()

    for week_num in range(1, 52):   # Date loop
        # In ISO calendar: Year, Number of years week(1-52/53), Number of weeks day(1=Monday, 7=Sunday
        c_date = tools.iso_to_gregorian(2016, week_num, 7)
        # Loading the graph from CSV files
        a_graph = graph_tools.form_graph(c_date, "Article_Sentence", entity_type, f_path + "Week_Graphs/")
        alpha_dict = nx.get_node_attributes(a_graph, 'name')

        alpha_entities = set(alpha_dict.values())


if __name__ == "__main__":
    pickle_to_file("/home/iraklis/PycharmProjects/AllTheNews/Graph_Analysis/Similarity_Timeseries/"
                   "P_sim_series_dict.pickle", "Dict", "P_simeseries_dict")
    # file_path = "/home/iraklis/PycharmProjects/AllTheNews/"
    # check_nodes("P", file_path)