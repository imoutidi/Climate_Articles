from ToolPack import tools
from graph_creation import relations_scores


class GraphCreator:

    def __init__(self, s_path):
        self.s_calculator = relations_scores.ScoreCalculator()
        self.structure_path = s_path
        self.relation_types = ["PLO", "PL", "PO", "LO", "P", "L", "O"]

    def assign_ids(self, art_ent_list, rel_type):
        index_dict = dict()
        entry_id = 0
        for ent_list in art_ent_list:
            frequencies = self.s_calculator.entity_article_frequency(ent_list)
            for r_t in rel_type:
                for ent_key in frequencies[r_t]:
                    if ent_key not in index_dict:
                        index_dict[ent_key] = entry_id
                        entry_id += 1
        return index_dict

    @staticmethod
    def assign_sentence_ids(sent_rel_weights):
        index_dict = dict()
        entry_id = 0
        for entity_pair in sent_rel_weights:
            splited_pair = entity_pair.split("**")
            for entity in splited_pair:
                if entity not in index_dict:
                    index_dict[entity] = entry_id
                    entry_id += 1
        return index_dict

    @staticmethod
    def article_graph(art_rel_weights, ids, r_type, path):
        # Creating gephi node CSV file
        with open(path + '/Nodes' + r_type + '.csv', 'w') as node_file:
            node_file.write('id,label\n')
            for i_d in ids:
                node_file.write(str(ids[i_d]) + "," + i_d + "\n")

        # Creating gephi edge CSV file
        with open(path + '/Edges' + r_type + '.csv', 'w') as edge_file:
            edge_file.write('Source,Target,Weight\n')
            for rel_weight in art_rel_weights:
                splited_pair = rel_weight.split("**")
                edge_file.write(str(ids[splited_pair[0]]) + ","
                                + str(ids[splited_pair[1]]) + ","
                                + str(art_rel_weights[rel_weight][0]) + "\n")

    @staticmethod
    def sentence_graph(sent_rel_weights, ids, r_type, path):

        # Creating gephi node CSV file
        with open(path + '/Nodes' + r_type + '.csv', 'w') as node_file:
            node_file.write('id,label\n')
            for i_d in ids:
                node_file.write(str(ids[i_d]) + "," + i_d + "\n")

        # Creating gephi edge CSV file
        with open(path + '/Edges' + r_type + '.csv', 'w') as edge_file:
            edge_file.write('Source,Target,Weight\n')
            for rel_weight in sent_rel_weights:
                splited_pair = rel_weight.split("**")
                edge_file.write(str(ids[splited_pair[0]]) + ","
                                + str(ids[splited_pair[1]]) + ","
                                + str(sent_rel_weights[rel_weight][0]) + "\n")

    @staticmethod
    def merged_graph(merged_rel_weights, ids, r_type, path):

        # Creating gephi node CSV file
        with open(path + '/Nodes' + r_type + '.csv', 'w') as node_file:
            node_file.write('id,label\n')
            for i_d in ids:
                node_file.write(str(ids[i_d]) + "," + i_d + "\n")

        # Creating gephi edge CSV file
        with open(path + '/Edges' + r_type + '.csv', 'w') as edge_file:
            edge_file.write('Source,Target,Weight\n')

            for rel_weight in merged_rel_weights:
                splited_pair = rel_weight.split("**")
                edge_file.write(str(ids[splited_pair[0]]) + ","
                                + str(ids[splited_pair[1]]) + ","
                                + str(merged_rel_weights[rel_weight][0]) + "\n")

    def create_article_graph(self, project_path):
        ent_struct = tools.load_pickle(self.structure_path)

        for rel_type in self.relation_types:
            articles_rel_weights = dict()

            for ent_list in ent_struct:
                articles_rel_weights = self.s_calculator.article_level_score(articles_rel_weights, ent_list, rel_type)
            node_ids = self.assign_ids(ent_struct, rel_type)

            # Creating gephi CSV files
            self.article_graph(articles_rel_weights, node_ids, rel_type, project_path)

    def create_sentence_graph(self, project_path):
        ent_struct = tools.load_pickle(self.structure_path)
        for rel_type in self.relation_types:
            sentences_rel_weights = dict()

            # Calculating the weight for all entities for all sentences of all articles
            # In this dictionary we will keep the score regarding
            # the occurrences of two entities in a sentence
            # The score will be accumulated for each pair.
            for ent_list in ent_struct:
                sentences_rel_weights = self.s_calculator.sentence_level_score(sentences_rel_weights,
                                                                               ent_list, rel_type)
            # Only for sentence level graphs
            sent_entry_ids = self.assign_sentence_ids(sentences_rel_weights)

            # Creating gephi CSV file
            self.sentence_graph(sentences_rel_weights, sent_entry_ids, rel_type, project_path)

    def create_merged_graph(self, project_path):
        ent_struct = tools.load_pickle(self.structure_path)
        for rel_type in self.relation_types:
            articles_rel_weights = dict()
            sentences_rel_weights = dict()

            for ent_list in ent_struct:
                articles_rel_weights = self.s_calculator.article_level_score(articles_rel_weights, ent_list, rel_type)
            for ent_list in ent_struct:
                sentences_rel_weights = self.s_calculator.sentence_level_score(sentences_rel_weights,
                                                                               ent_list, rel_type)
            merged_ids = self.assign_ids(ent_struct, rel_type)
            merged_rel_weights = self.s_calculator.merge_scores(articles_rel_weights, sentences_rel_weights)
            # Creating gephi CSV file
            self.merged_graph(merged_rel_weights, merged_ids, rel_type, project_path)
            print()


if __name__ == "__main__":
    file_path = "/home/iraklis/PycharmProjects/climate_change/IO_files/entity_structure.pickle"
    g_c = GraphCreator(file_path)
    article_graph_path = "/home/iraklis/PycharmProjects/climate_change/IO_files/Graphs/Article"
    sentence_graph_path = "/home/iraklis/PycharmProjects/climate_change/IO_files/Graphs/Sentence"
    merged_graph_path = "/home/iraklis/PycharmProjects/climate_change/IO_files/Graphs/Merged"
    # g_c.create_article_graph(article_graph_path)
    # g_c.create_sentence_graph(sentence_graph_path)
    g_c.create_merged_graph(merged_graph_path)
