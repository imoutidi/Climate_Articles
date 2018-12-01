# Reading from a .csv file, scraped news from difbot
import json


def read_file(filename):
    json_list = list()
    article_list = list()
    with open(filename) as input_file:
        content = input_file.readlines()

    for article in content:
        json_list.append(article.split("\t")[1].strip())

    for json_article in json_list:
        try:
            current_json = json.loads(json_article)
            if "objects" in current_json:
                if len(current_json["objects"]) > 0:
                    if "text" in current_json["objects"][0]:
                        article_list.append(current_json["objects"][0]["text"])
        except ValueError:
            print("Value error")

    # Removing empty articles
    new_article_list = list()
    for text_article in article_list:
        # Number 6 is an arbitrary number to check empty articles
        if len(text_article) > 6:
            new_article_list.append(text_article)

    return new_article_list 


if __name__ == "__main__":
    read_file("/home/iraklis/Desktop/PhDLocal/Datasets/Climate Change/cc1_all_content.csv")