"""
Implementation of a Graph data structure

"""
from uuid import uuid4
from typing import Callable


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
        self.__verticies = {}

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
        return self.__verticies.keys()

    def add_vertex(self, new_vertex: Vertex) -> None:
        """
        Add the given vertex to the graph object
        TODO: enable population of existing edges for a given vertex

        :param new_vertex:
        :return:
        """

        # edge: each vertex has a unique set of edges
        if new_vertex not in self.__verticies:
            self.__verticies[new_vertex] = {}

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

        if start_vertex in self.__verticies:
            self.__verticies[start_vertex][end_vertex] = value
        else:
            self.add_vertex(start_vertex)
            self.add_vertex(end_vertex)  # ensure end_vertex also exists as well
            self.__verticies[start_vertex][end_vertex] = value

    def generate_edges(self) -> [{Vertex, Vertex}]:
        """
        Generate all the edges

        :return: List of set(starting vertex, ending vertex}
        """

        result = []  # TODO: inefficient, in an array in this loop results in Big O n^3... consider set
        for start_vertex in self.__verticies:
            for end_vertex in self.__verticies[start_vertex]:
                edge = {start_vertex, end_vertex}
                if edge not in result:
                    result.append(edge)
        return result

    def depth_first_traversal(self, start_vertex: Vertex, callback: Callable) -> None:
        """
        Depth traversal starting with the start_vertex

        :param start_vertex: Starting vertex to start the search
        :param callback: Callback function provided by the caller to be invoked when a vertex node is visited
            Client can use the callback for search criterion and exit the traversal if their condition are meet
            by simply returning False
        :return: None
        """
        visited = []

        def __depth_first_traversal(current_vertex: Vertex) -> None:
            """
            :param current_vertex: Current vertex for processing

            :return:
            """
            queue = self.__verticies[current_vertex].keys()

            for current_queue_vertex in queue:
                if callback:
                    if not callback(current_queue_vertex):
                        return  # TODO: Bug here, throw a exception to be caught at top level to exit deep recursion
                __depth_first_traversal(current_queue_vertex)
            visited.append(current_vertex)

        __depth_first_traversal(start_vertex)
        print('\nVisited verticies:')
        for vertex in visited:
            print(vertex)

    def breath_first_traversal(self, start_vertex: Vertex, callback: Callable) -> None:
        """
        Breadth First Traversal:
        Ensures each level by level (or children are processed

        :param start_vertex: Starting vertex to process
        :param callback: Client provided callback as each node is processed
            Client can use the callback for search criterion and exit the traversal if their condition are meet
            by simply returning False

        :return:
        """
        visited = {}  # Key is the vertex reference, Value is visited boolean flag

        # set operation is much faster than array due to copy operations... also guarantee uniqueness
        # order of processing is hierarchical or level based
        queue = set()

        current_vertex = start_vertex
        queue.add(start_vertex)
        visited[start_vertex] = True

        while queue:
            if self.__verticies[current_vertex]:
                # neighbors exist
                if current_vertex in queue:
                    queue.remove(current_vertex)  # only be valid for initial node/vertex
                else:
                    current_vertex = queue.pop()
            else:
                # no neighbors, dead end
                current_vertex = queue.pop()

            if not callback(current_vertex):
                break

            for neighbor in self.__verticies[current_vertex]:
                if neighbor in visited:
                    continue  # default, this is already set to True as the key would not in visited if not visited
                else:
                    # not visited: ensure we add the neighbor vertex and visit all elements in the queue
                    queue.add(neighbor)
                    visited[neighbor] = True


if __name__ == '__main__':
    # TODO: Put into Python unit tests

    def echo_value(vertex: Vertex):
        """
        Callback used traverse the graph traversal

        :return:
        """
        print(vertex)
        return True

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
        graph.add_edge(island_vertex2, island_vertex2)

        david_vertex = Vertex('David')
        sue_vertex = Vertex('Sue')
        robert_vertex = Vertex('Robert')

        # manual vertex addition
        graph.add_vertex(david_vertex)
        graph.add_vertex(sue_vertex)
        graph.add_vertex(robert_vertex)

        graph.add_edge(david_vertex, sue_vertex, {'weight': 100})  # example client data reflecting weight for the edge
        graph.add_edge(sue_vertex, robert_vertex, {'weight': 5})

        # add edge adds the vertex without having an existing vertex / shorthand an edge requires an vertex to existence
        sam_vertex = Vertex('Sam')
        graph.add_edge(sam_vertex, Vertex('Debbie'))

        # have a fork off original lineage
        graph.add_edge(sue_vertex, sam_vertex)

        print('\n*** Graph Edges\n')
        print(graph)  # list of set of verticies
        print('\n*** Graph Verticies')
        verticies = graph.verticies()
        for vertex in verticies:
            print(vertex)

        print('\n*** Start Breadth Traversal')
        graph.depth_first_traversal(david_vertex, echo_value)

    # test_simple_graph()

    def test_complex_graph():
        """
        More complex graph

        Starting center vertex: David
        David: 2 children
            Sue
            Sally
            Debbie
        Sally:
            Henry
        Henry:
            Alex
        Alex:
            Debbie
        Sue:
            Frank
        Frank:
            Tom
        Tom:
            Hank

        :return:
        """
        all_verticies = {'Sally': None, 'Henry': None, 'David': None, 'Alex': None, 'Sue': None, 'Debbie': None,
                         'Frank': None, 'Tom': None, 'Hank': None}

        graph = Graph()
        for name in all_verticies:
            vertex = Vertex(name)
            graph.add_vertex(vertex)
            all_verticies[name] = vertex  # for testing and book keeping purposes
        # connect parent / child as detailed in docstring
        graph.add_edge(all_verticies['David'], all_verticies['Sally'])
        graph.add_edge(all_verticies['David'], all_verticies['Sue'])
        graph.add_edge(all_verticies['David'], all_verticies['Debbie'])
        graph.add_edge(all_verticies['Sally'], all_verticies['Henry'])
        graph.add_edge(all_verticies['Henry'], all_verticies['Alex'])
        graph.add_edge(all_verticies['Alex'], all_verticies['Debbie'])
        graph.add_edge(all_verticies['Sue'], all_verticies['Frank'])
        graph.add_edge(all_verticies['Frank'], all_verticies['Tom'])
        graph.add_edge(all_verticies['Tom'], all_verticies['Hank'])

        print('\n*** Start Breadth First Traversal')
        graph.breath_first_traversal(all_verticies['David'], echo_value)

        # print('\n*** Start Depth first Traversal')
        # graph.depth_first_traversal(all_verticies['David'], echo_value)


    test_complex_graph()