from datetime import date, timedelta
from pivot_files import read_data
from NER_Tools import entity_cleaning, entity_detection
from ToolPack import tools


class KnowledgeGraph:
    # Detecting named entities in the given text
    # Returns a list(articles) of lists(sentences)
    # of dictionaries(named entity kind).
    @staticmethod
    def detect_entities():
        input_path = "/home/iraklis/Desktop/PhDLocal/Datasets/Climate Change/cc1_all_content.csv"
        article_list = read_data.read_file(input_path)

        articles_entity_list = list()
        count = 0
        for article in article_list:
            entity_dict = entity_detection.detection(article)
            print(count)
            count += 1
            if entity_dict != "nan":
                articles_entity_list.append(entity_dict)

        # Cleaning all entities.
        articles_entity_list = entity_cleaning.clean(articles_entity_list)
        tools.save_pickle("/home/iraklis/PycharmProjects/climate_change/IO_files/entity_structure.pickle",
                          articles_entity_list)


if __name__ == "__main__":
    KnowledgeGraph.detect_entities()
