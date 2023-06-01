"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
import random
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import time

# from linkedqueue import LinkedQueue


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s_var = ""
            if node is not None:
                s_var += recurse(node.right, level + 1)
                s_var += "| " * level
                s_var += str(node.data) + "\n"
                s_var += recurse(node.left, level + 1)
            return s_var

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def inorder_lst(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []
        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def find_position(node):
            while node:
                # New item is less, go left until spot is found
                if item < node.data:
                    if node.left is None:
                        node.left = BSTNode(item)
                        break
                    else:
                        node = node.left
                # New item is greater or equal,
                # go right until spot is found
                else:
                    if node.right is None:
                        node.right = BSTNode(item)
                        break
                    else:
                        node = node.right

        # Tree is empty, so new item goes at the root
        if self._root is None:
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            find_position(self._root)
        self._size += 1


    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        node = self._root
        while node:
            if item == node.data:
                return node.data
            if item < node.data:
                node = node.left
            else:
                node = node.right

        return None


    # def find(self, item):
    #     """If item matches an item in self, returns the
    #     matched item, or None otherwise."""

    #     def recurse(node):
    #         if node is None:
    #             return None
    #         if item == node.data:
    #             return node.data
    #         if item < node.data:
    #             return recurse(node.left)
    #         return recurse(node.right)

    #     return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    # def add(self, item):
    #     """Adds item to the tree."""

    #     # Helper function to search for item's position
    #     def recurse(node):
    #         # New item is less, go left until spot is found
    #         if item < node.data:
    #             if node.left is None:
    #                 node.left = BSTNode(item)
    #             else:
    #                 recurse(node.left)
    #         # New item is greater or equal,
    #         # go right until spot is found
    #         elif node.right is None:
    #             node.right = BSTNode(item)
    #         else:
    #             recurse(node.right)
    #             # End of recurse

    #     # Tree is empty, so new item goes at the root
    #     if self.isEmpty():
    #         self._root = BSTNode(item)
    #     # Otherwise, search for the item's spot
    #     else:
    #         recurse(self._root)
    #     self._size += 1


    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemremoved = None
        preroot = BSTNode(None)
        preroot.left = self._root
        parent = preroot
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                itemremoved = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if itemremoved is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left is None \
                and not currentnode.right is None:
            liftmaxinleftsubtreetotop(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                newchild = currentnode.right

                # Case 3: The node has no right child
            else:
                newchild = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = newchild
            else:
                parent.right = newchild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preroot.left
        return itemremoved

    def replace(self, item, newitem):
        """
        If item is in self, replaces it with newitem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                olddata = probe.data
                probe.data = newitem
                return olddata
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self, pos=None):
        '''
        Return the height of tree
        :return: int
        '''
        if pos is None:
            pos = self._root
        return self.height1(pos)

    def height1(self, top):
        '''
        Helper function
        :param top:
        :return:
        '''
        if self.is_leaf(top):
            return 0
        return (1 + max(self.height1(i) for i in self.children(top)))

    def is_leaf(self, item):
        """
        Return True is item is a leaf
        :return: bool
        """
        if item is None:
            return False
        if item.left is None and item.right is None:
            return True
        return False

    def children(self, item):
        """
        Return all children of a parent node
        :return: list
        """
        res = []
        if item.left:
            res.append(item.left)
        if item.right:
            res.append(item.right)
        return res

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2*log(1+len(list(self)), 2)
        # if root is None: 
        #     return True
        # return is_balanced(root.right) and \
        # is_balanced(root.left) and \
        # abs(get_height(root.left) - get_height(root.right)) <= 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        lst = []
        for node in self.get_all_nodes():
            if low <= node.data <= high:
                lst.append(node.data)
        if len(lst) == 0:
            lst.append(low)
            lst.append(high)
        return lst


    def rebalance(self):
        """
        Rebalances the tree.
        """
        node_list = self._inorder_traversal(self._root)
        self.clear()
        self._root = self._create_new_tree(sorted(node_list))
        print(self)

    def _inorder_traversal(self, node):
        """
        Performs an inorder traversal and returns a list of nodes in sorted order.
        """
        node_list = []
        stack = []
        current = node

        while True:
            if current is not None:
                stack.append(current)
                current = current.left
            elif stack:
                current = stack.pop()
                node_list.append(current.data)
                current = current.right
            else:
                break

        return node_list

    def _create_new_tree(self, node_list):
        """
        Creates a new tree from the sorted node list.
        """
        if not node_list:
            return None

        mid = len(node_list) // 2
        node = BSTNode(node_list[mid])
        node.left = self._create_new_tree(node_list[:mid])
        node.right = self._create_new_tree(node_list[mid+1:])

        return node

    def get_all_nodes(self) -> list:
        """Returns a list of all nodes in the binary tree."""
        nodes = []
        self._traverse(self._root, nodes)
        return nodes

    def _traverse(self, node, nodes):
        if node:
            nodes.append(node)
            if node.left:
                self._traverse(node.left, nodes)
            if node.right:
                self._traverse(node.right, nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self.get_all_nodes()
        try:
            successor = min([i for i in self if i > item])
            for node in lst:
                if node.data == successor:
                    return node
        except (ValueError, AttributeError, TypeError):
            pass
        return None

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        lst = self.get_all_nodes()
        try:
            successor = max([i for i in self if i < item])
            for node in lst:
                if node.data == successor:
                    return node
        except (ValueError, AttributeError, TypeError):
            pass
        return None

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        with open(path, encoding='UTF-8') as file:
            content = file.readlines()
            content = list(map(lambda x: x[:-2], content))
        random_nodes = random.choices(content, k=10000)

        # linear search
        print('Around 36 sec')
        start = time.time()
        for i in random_nodes:
            for j in content:
                if i == j:
                    continue
        end = time.time()
        print('Linear search =', end-start)

        # binary search alphabet
        print('Around 42 sec')
        tree = LinkedBST()
        for j in content:
            tree.add(j)
        start = time.time()
        for i in random_nodes:
            tree.find(i)
        end = time.time()
        print('Binary search alphabet =', end-start)

        # binary search random
        tree = LinkedBST()
        for j in list(random.choices(content, k=234936)):
            tree.add(j)
        start = time.time()
        for i in random_nodes:
            tree.find(i)
        end = time.time()
        print('Binary search random =', end-start)

        # binary search random after rebalance
        tree = LinkedBST()
        for j in list(random.choices(content, k=234936)):
            tree.add(j)
        tree.rebalance()
        start = time.time()
        for i in random_nodes:
            tree.find(i)
        end = time.time()
        print('Binary search random after rebalance =', end-start)


if __name__ == '__main__':
    a = LinkedBST()
    a.demo_bst('words.txt')
