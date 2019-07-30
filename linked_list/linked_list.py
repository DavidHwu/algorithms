"""
Implements performant linked list

"""
from random import randint


class LinkedListNode:
    """
    Doubly linked list Node for the given linked list
    """
    def __init__(self, value) -> None:
        self.next = None
        self.previous = None
        self.value = value

    def __str__(self) -> str:
        return 'value: {}'.format(self.value)

    def attach(self, prior_node) -> None:
        """

        :param prior_node:
        :return:
        """
        next_node = prior_node.next
        prior_node.next = self
        self.next = next_node
        self.previous = prior_node
        if next_node:
            next_node.previous = self


class LinkedList:
    """
    Linked List Implementation
    Cache the first and last node internally
    """
    def __init__(self) -> None:
        self.first_node = None
        self.last_node = None

    def __str__(self) -> str:
        header = 'First Node: {0}\n' \
                 'Last Node: {1}\n'.format(self.first_node, self.last_node)

        node_str = ''
        current_node = self.first_node
        while current_node:
            node_str = ''.join([node_str, str(current_node), '\n'])
            current_node = current_node.next
        return header + node_str

    def append_node(self,
                    new_node: LinkedListNode,
                    prior_node: LinkedListNode = None) -> None:
        """
        Attach the given node to anywhere in the list

        :param new_node: New node for appending
        :param prior_node: Prior node to attach to... defaults to None to attach the the head of the list
        :return: None
        """

        if self.first_node is None and self.last_node is None:
            # only 1 in the list
            self.first_node = new_node
            self.last_node = new_node
            new_node.previous = None
            new_node.previous = None
            return

        if prior_node:
            if self.last_node is prior_node:
                # tail of linked list
                self.last_node = new_node
            next_node = prior_node.next
            if next_node:
                next_node.previous = new_node
                new_node.previous = prior_node
            prior_node.next = new_node
            new_node.previous = prior_node
            new_node.next = next_node
        else:
            # attach to the head of the list
            next_node = self.first_node
            next_node.previous = new_node
            new_node.next = next_node

            self.first_node = new_node

    def remove_node(self, node: LinkedListNode) -> None:
        """
        Remove the given node from the linked list and ensure linking order are preserved
        Ensures the LinkedList class sets the first and last node pointers properly if head/tail is removed

        :param node: Node for removal
        :return: None
        """
        previous_node = node.previous
        next_node = node.next

        if previous_node and next_node:
            previous_node.next = next_node
            next_node.previous = previous_node
            return

        if previous_node is None:
            # head
            self.first_node = next_node
            if next_node:
                next_node.previous = None

        if next_node is None:
            # tail
            self.last_node = previous_node
            if previous_node:
                previous_node.next = None


def test_linkedlist_node():
    """

    :return:
    """
    nodes = []
    for i in range(10):
        nodes.append(LinkedListNode(randint(1, 1000)))
        if i >= 1:
            nodes[i-1].attach(nodes[i])

    for i in range(10):
        print(nodes[i])


if __name__ == '__main__':

    def test_linkedlist():
        """
        Test the LinkedList class
        :return:
        """
        print('*** Test LinkedList')

    def generate_test(linked_list: LinkedList) -> list:
        """
        Generate random set of nodes in a list format for testing purposes
        :return:
        """
        result = []
        for i in range(10):
            new_node = LinkedListNode(randint(1, 1000))
            result.append(new_node)
            if i == 0:
                linked_list.append_node(new_node)
            else:
                linked_list.append_node(new_node, result[i-1])
        return result

    linked_list = LinkedList()
    nodes = generate_test(linked_list)
    print('--> Original Content\n')
    print(linked_list)
    # remove the middle element
    element_number = 5
    print('--> Remove middle node: {}\n'.format(nodes[element_number]))
    linked_list.remove_node(nodes[element_number])
    print(linked_list)
    # remove the head node
    print('--> Remove head node\n')
    linked_list.remove_node(nodes[0])
    print(linked_list)
    # remove the tail node
    print('--> Remove the tail node')
    linked_list.remove_node(nodes[len(nodes)-1])
    print(linked_list)

    # test_linkedlist_node()
    test_linkedlist()



