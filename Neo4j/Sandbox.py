from neo4j.v1 import GraphDatabase
from py2neo import Graph, Node
import csv


class HelloWorldExample(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def print_greeting(self, message):
        with self._driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, message)
            print(greeting)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]

def graph_to_neodb():
    nodes = "file:/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Raw_Graphs/Merged/NodesPLO.csv"
    edges = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Raw_Graphs/Merged/EdgesPLO.csv"

    driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "2113"))
    session = driver.session()
    # a = session.run("RETURN 1 AS a, true AS b, 3.14 AS c").data()
    # Create a node
    # session.run("CREATE (al:Person {name:'John', born:1986})")
    # a = session.run("MATCH (a:Person) WHERE a.name='John' RETURN a.born")
    session.run("LOAD CSV WITH HEADERS FROM $nodes AS node_row "
                "CREATE (n:Node) "
                "SET n = node_row,"
                "n.id = toInteger(node_row.id),"
                "n.label = node_row.label", nodes=nodes)
    with open(edges) as edge_file:
        next(edge_file)
        count = 0
        for edge in edge_file:
            print(count)
            count += 1
            edge_info = edge.strip().split(",")
            session.run("MATCH (n1: Node {id:$source}), (n2: Node {id:$target})"
                        "CREATE (n1)-[r:Co_Occured {weight:$weight}]->(n2)"
                        , source=float(edge_info[0]), target=float(edge_info[1]), weight=float(edge_info[2]))


def insert_nodes_to_neodb(neo_graph):
    # node_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Raw_Graphs/Merged/NodesPLO.csv"
    test_node_path = "/home/iraklis/PycharmProjects/Climate_Articles/Neo4j/Test_Files/test_graph_1/nodes.csv"
    graph = Graph("bolt://localhost:7687", user="neo4j", password="2113")

    trans_action = graph.begin()

    with open(test_node_path) as csvfile:
        next(csvfile)   # labels of the columns
        node_csv = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(node_csv):
            # statement = "Create(n{id:{A} ,label:{B}})"
            # trans_action.append(statement, {"A": row[0], "B": row[1]})
            trans_action.create(Node("Entity", id=row[0], label=row[1]))

            # if idx % 1000 == 0:
        trans_action.commit()
            # trans_action = graph.begin()


def insert_edges_to_neodb(neo_graph):
    edge_path = "/home/iraklis/PycharmProjects/Climate_Articles/IO_files/Graphs/Raw_Graphs/Merged/EdgesPLO.csv"
    test_edge_path = "/home/iraklis/PycharmProjects/Climate_Articles/Neo4j/Test_Files/test_graph_1/edges.csv"
    graph = Graph("bolt://localhost:7687", user="neo4j", password="2113")

    trans_action = graph.begin()

    with open(test_edge_path) as csvfile:
        next(csvfile)   # labels of the columns
        edge_csv = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(edge_csv):



if __name__ == "__main__":
    insert_nodes_to_neodb()


