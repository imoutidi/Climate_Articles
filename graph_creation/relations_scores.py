
class ScoreCalculator:

    def __init__(self):
        self.a = 0

    @staticmethod
    def entity_article_frequency(ent_list):
        all_persons = dict()
        all_locations = dict()
        all_organizations = dict()
        entity_frequencies = dict()

        for sent_dict in ent_list:
            for entity in sent_dict["P"]:
                if entity in all_persons:
                    all_persons[entity] += 1
                else:
                    all_persons[entity] = 1
            for entity in sent_dict["L"]:
                if entity in all_locations:
                    all_locations[entity] += 1
                else:
                    all_locations[entity] = 1
            for entity in sent_dict["O"]:
                if entity in all_organizations:
                    all_organizations[entity] += 1
                else:
                    all_organizations[entity] = 1
        entity_frequencies["P"] = all_persons
        entity_frequencies["L"] = all_locations
        entity_frequencies["O"] = all_organizations

        return entity_frequencies

    def calculate_relations_weights(self, frequencies, rel_type):
        frequency_sum = self.calculate_frequency_sum(frequencies, rel_type)
        weight_dict = dict()
        weight_list = list()
        name_list = list()
        value_list = list()
        for r_t in rel_type:
            name_list += frequencies[r_t]
            value_list += frequencies[r_t].values()
        # we sort the values accordingly the sorted name list and return two sorted tuples
        sorted_values = []
        sorted_names = []
        if len(name_list) != 0:
            #  This comprehension crashes if we give empty lists
            sorted_names, sorted_values = zip(*[(name, value) for name, value in sorted(zip(name_list, value_list))])
            sorted_names = list(sorted_names)
            sorted_values = list(sorted_values)

        for idx, out_value in enumerate(sorted_values[:-1]):
            weight_list.append(list())
            for in_value in sorted_values[idx + 1:]:
                weight_list[idx].append((out_value + in_value) / frequency_sum)

        for out_idx, out_name in enumerate(sorted_names[:-1]):
            for in_idx, in_name in enumerate(sorted_names[out_idx + 1:]):
                weight_dict[out_name + "**" + in_name] = weight_list[out_idx][in_idx]

        return weight_dict

    def calculate_sent_relations_weights(self, ent_list, freqs, rel_type):
        frequency_sum = self.calculate_frequency_sum(freqs, rel_type)
        weight_dict = dict()

        for idx, sent in enumerate(ent_list):
            sent_ent_list = list()
            for r_t in rel_type:
                for ent in sent[r_t]:
                    sent_ent_list.append((ent, freqs[r_t][ent]))
            if len(sent_ent_list) > 1:
                # Calculating sentence weight and add it in weight dict
                sent_ent_list = sorted(list(set(sent_ent_list)))  # I am using set to delete duplicates
                for in_idx, out_name in enumerate(sent_ent_list[:-1]):
                    for in_name in sent_ent_list[in_idx + 1:]:
                        if out_name[0] + "**" + in_name[0] not in weight_dict:
                            weight_dict[out_name[0] + "**" + in_name[0]] = [(out_name[1] + in_name[1]) / frequency_sum]
                        else:
                            weight_dict[out_name[0] + "**" + in_name[0]][0] += (out_name[1] + in_name[
                                1]) / frequency_sum
        return weight_dict

    @staticmethod
    def calculate_frequency_sum(frequencies, r_type):
        values = list()
        for r_t in r_type:
            values += list(frequencies[r_t].values())
        return sum(values)

    def article_level_score(self, all_articles_rel_weights, entity_list, r_type):
        frequencies = self.entity_article_frequency(entity_list)
        single_article_rel_weights = self.calculate_relations_weights(frequencies, r_type)
        for entity_couple in single_article_rel_weights:
            if entity_couple in all_articles_rel_weights:
                all_articles_rel_weights[entity_couple][0] += single_article_rel_weights[entity_couple]
            else:
                all_articles_rel_weights[entity_couple] = [single_article_rel_weights[entity_couple]]

        return all_articles_rel_weights

    def sentence_level_score(self, all_articles_rel_weights, entity_list, r_type):
        frequencies = self.entity_article_frequency(entity_list)
        sentence_rel_weights = self.calculate_sent_relations_weights(entity_list, frequencies, r_type)
        for entity_couple in sentence_rel_weights:
            if entity_couple in all_articles_rel_weights:
                all_articles_rel_weights[entity_couple][0] += sentence_rel_weights[entity_couple][0]
            else:
                all_articles_rel_weights[entity_couple] = [sentence_rel_weights[entity_couple][0]]
                                                           # {art_id: sentence_rel_weights[entity_couple][1]}]

        return all_articles_rel_weights

    @staticmethod
    def merge_scores(article_weights, sentence_weights):
        merged_weights = dict()
        for sent_key in article_weights:
            if sent_key in sentence_weights:
                merged_weights[sent_key] = [sentence_weights[sent_key][0] + article_weights[sent_key][0]]
            else:
                merged_weights[sent_key] = [article_weights[sent_key][0]]
        return merged_weights
