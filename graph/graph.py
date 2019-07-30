"""
Implementation of a Graph data structure

"""
from uuid import uuid4


class Vertex:
    """
    Class abstraction representation of a given vertex node

    * Class cotainer to hold any given content value for a given vertex
    * ID set to reflect a DB model or some UUID that is persistable (not used atm)
    """

    def __init__(self, value):
        """

        :param value: Any python object or value to be stored inside the vertex node
        """
        self.id = uuid4()  # intentionally set to a unique value so its not just an in memory reference used
        self.value = value

    def __str__(self):
        """

        :return:
        """
        return str(self.value)


class Graph:
    """

    TODO: Directed vs Undirected (bidirectional direction)
    TODO: Weighted graph

    """

    def __init__(self):
        self.__verticies_dict = {}

    def __str__(self):
        """

        :return:
        """

        result = ''
        edges = self.generate_edges()
        for edge in edges:
            result = ''.join([result, '('])
            for vertex in edge:
                result = ''.join([result, str(vertex), ','])
            result = ''.join([result, ') \n'])
        return result

    def verticies(self) -> list:
        """
        Return a list of verticies in the given Graph

        :return:
        """
        return self.__verticies_dict.keys()

    def add_vertex(self, new_vertex: Vertex) -> None:
        """
        Add the given vertex to the graph object
        TODO: enable population of existing edges for a given vertex

        :param new_vertex:
        :return:
        """

        # edge: each vertex has a unique set of edges
        if str(new_vertex) not in self.__verticies_dict:
            self.__verticies_dict[new_vertex] = {}

        # optional implementation using an ID (ie. unique value in DB row or GUID instead of in memory reference
        # if str(new_vertex.id) not in self.__verticies_dict:
            # self.__verticies_dict[new_vertex.id] = {}

    def add_edge(self, start_vertex: Vertex, end_vertex: Vertex, value: dict = None) -> None:
        """

        :param start_vertex: Starting vertex
        :param end_vertex: Ending vertex (can be the same as starting vertex
        :param value: client data dictionary to be stored

        :return: None
        """

        if start_vertex in self.__verticies_dict:
            self.__verticies_dict[start_vertex][end_vertex] = value
        else:
            self.add_vertex(start_vertex)
            self.add_vertex(end_vertex)  # ensure end_vertex also exists as well
            self.__verticies_dict[start_vertex][end_vertex] = value

    def generate_edges(self) -> [{Vertex, Vertex}]:
        """
        Generate all the edges

        :return: List of set(starting vertex, ending vertex}
        """

        result = []
        for start_vertex in self.__verticies_dict:
            for end_vertex in self.__verticies_dict[start_vertex]:
                edge = {start_vertex, end_vertex}
                if edge not in result:
                    result.append(edge)
        return result


if __name__ == '__main__':
    # TODO: Put into Python unit tests

    def test_simple_graph() -> None:
        """
        Test 2 lineages
        * David -> Sue -> Robert
        * Sam -> Debbie
        * Sue -> Sam

        2 types of islands:
        * Single island (no directional outbound or inbound)
        * Single island (with reference to itself)

        :return: None
        """
        graph = Graph()

        island_vertex = Vertex('island')
        island_vertex2 = Vertex('island points to itself')
        graph.add_vertex(island_vertex)
        graph.add_vertex(island_vertex2)

        david_vertex = Vertex('David')
        sue_vertex = Vertex('Sue')
        robert_vertex = Vertex('Robert')

        # manual vertex addition
        graph.add_vertex(david_vertex)
        graph.add_vertex(sue_vertex)

        graph.add_edge(david_vertex, sue_vertex, {'weight': 100})  # example client data reflecting weight for the edge
        graph.add_edge(sue_vertex, robert_vertex, {'weight': 5})

        # add edge adds the vertex without having an existing vertex / shorthand an edge requires an vertex to existence
        sam_vertex = Vertex('Sam')
        graph.add_edge(sam_vertex, Vertex('Debbie'))
        graph.add_edge(island_vertex2, island_vertex2)

        # have a fork off original lineage
        graph.add_edge(sue_vertex, sam_vertex)

        print('\n*** Graph Edges\n')
        print(graph)  # list of set of verticies
        print('\n*** Graph Verticies')
        verticies = graph.verticies()
        for vertex in verticies:
            print(vertex)

    test_simple_graph()




