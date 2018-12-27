from tool_pack import tools


class ReportGenerator:
    def __init__(self, read_path, write_path):
        self.in_path = read_path
        self.out_path = write_path

    @staticmethod
    def sorting(names, metric):
        # Sorting the names list based on the sorting of the metrics list
        names_metrics_ranking = [[x, y] for x, y in sorted(zip(metric, names), key=lambda pair: pair[0], reverse=True)]
        return names_metrics_ranking

    def print_report(self, metrics_pairs, metric_name):
        with open(self.out_path + metric_name, 'w') as metric_file:
            for pair in metrics_pairs:
                metric_file.write(str(pair) + "\n")

    def make_reports(self, metric_name):
        metric_list = list()
        entity_names = tools.load_pickle(self.in_path + "Entity_Names.pickle")
        entity_metrics = tools.load_pickle(self.in_path + metric_name + ".pickle")
        # d_dict = dict()
        # for node, value in entity_metrics:
        #     d_dict[node] = value
        # entity_metrics = d_dict
        for _, value in entity_metrics.items():
            metric_list.append(value)
        sorted_metrics = self.sorting(entity_names, metric_list)
        self.print_report(sorted_metrics, metric_name)


if __name__ == "__main__":
    input_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graph_Metrics/" \
                 "Merged_All_Days/Merged_PLO_100/"
    output_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graph_Metrics/" \
                  "Merged_All_Days/Merged_PLO_100/Reports/"
    report_gen = ReportGenerator(input_path, output_path)
    report_gen.make_reports("Closeness_Centrality")
