# File: rbtree.py
# Author: John Glick    
# Date: February 20, 2023
# Description: Red-Black tree.  Red-black trees
# are balanced binary search trees.
#      
from enum import Enum

class Color(Enum):
    RED = 1
    BLACK = 2

class RBTreeNode:
    def __init__(self, item, color, left, right, parent,
                 key):
        """
        Initializes red-black tree node with item and other
        fields.
        """
        self.item = item
        self.color = color
        self.left = left
        self.right = right
        self.parent = parent
        self.key = key

    def __lt__(self, node):
        """
        Returns if self node is < node
        """

        # First test handles case of node being the
        # dummy node, with no item in it.
        if self.item == None or node.item == None:
            return False
        
        return self.key(self.item) < self.key(node.item)
    
    def __le__(self, node):
        """
        Returns if self node is <= node
        """

        # First test handles case of node being the
        # dummy node, with no item in it.

        if self.item == None or node.item == None:
            return False
        
        return self.key(self.item) <= self.key(node.item)
    
    def __eq__(self, node):
        """
        Returns if self node is == node
        """

        # First test handles case of node being the
        # dummy node, with no item in it.

        if self.item == None or node.item == None:
            return False
        
        return self.key(self.item) == self.key(node.item)

class RBTree:
    def __init__(self, key = lambda x: x):
        """
        Initializes empty tree.
        """
        self.key = key   # key for comparing items stored in nodes.
        self.size = 0
        self.null_node = RBTreeNode(None, Color.BLACK, None, 
                                    None, None, self.key)
        # Dummy node makes coding some parts of the algorithm simpler.
        self.null_node.left = self.null_node.right = self.null_node.parent = self.null_node
        self.root = self.null_node  

    def __len__(self):
        """
        Returns size of tree.
        """
        return self.size
    
    def insert(self, item):
        """
        Inserts parameter item into the tree.
        Duplicates allowed.
        """
        z = RBTreeNode(item, Color.RED, self.null_node, 
                            self.null_node, self.null_node,
                            self.key)
        y = self.null_node
        x = self.root
        while x is not self.null_node:
            y = x
            if z < x:
                x = x.left
            else:
                x = x.right
        z.parent = y
        if y is self.null_node:
            self.root = z
        else:
            if z < y:
                y.left = z
            else:
                y.right = z
        self.insert_fixup(z)
        self.size += 1
    
    def delete(self, item):
        """
        Deletes the parameter item from the tree (only one
        instance of it) if item is in the tree.  Raises KeyError
        exception if not in the tree.
        """
        # Find item
        z = self.root
        while z is not self.null_node and z.item != item:
            if self.key(item) < self.key(z.item):
                z = z.left
            else:
                z = z.right
        if z is self.null_node:
            raise KeyError
        self.delete_node(z)

    def delete_max(self):
        """
        Deletes and returns the largest item in the tree.
        Raises KeyError if the tree is empty.
        """
        if self.root is self.null_node:
            raise KeyError
        
        x = self.root
        while x.right is not self.null_node:
            x = x.right
        largest_item = x.item
        self.delete_node(x)
        return largest_item

    def delete_min(self):
        """
        Deletes and returns the smallest item in the tree.
        Raises KeyError if the tree is empty.
        """
        if self.root is self.null_node:
            raise KeyError
        
        x = self.root
        while x.left is not self.null_node:
            x = x.left
        smallest_item = x.item
        self.delete_node(x)
        return smallest_item
    
    def delete_smallest_greater_than(self, item):
        """
        Deletes and returns the smallest item in the tree that 
        is greater than the parameter item.
        Raises KeyError if there is no such item.
        """
        if self.root is self.null_node:
            raise KeyError
        
        x = self.root
        last_greater_than = self.null_node
        while True:
            if self.key(item) >= self.key(x.item):
                if x.right is self.null_node:
                    if last_greater_than is self.null_node:
                        raise KeyError
                    else:
                        break
                else:
                    x = x.right
            else:
                last_greater_than = x
                if x.left is self.null_node:
                    break
                else:
                    x = x.left

        return_item = last_greater_than.item
        self.delete_node(last_greater_than)
        return return_item

    def delete_largest_less_than(self, item):
        """
        Deletes and returns the largest item in the tree that 
        is less than the parameter item.
        Raises KeyError if there is no such item.
        """
        if self.root is self.null_node:
            raise KeyError
        
        x = self.root
        last_less_than = self.null_node
        while True:
            if self.key(item) <= self.key(x.item):
                if x.left is self.null_node:
                    if last_less_than is self.null_node:
                        raise KeyError
                    else:
                        break
                else:
                    x = x.left
            else:
                last_less_than = x
                if x.right is self.null_node:
                    break
                else:
                    x = x.right

        return_item = last_less_than.item
        self.delete_node(last_less_than)
        return return_item
    
    # **********************************
    # Helper methods.
    # **********************************
    
    def insert_fixup(self, z):
        """
        Restores the red-black tree properties
        after an insertion.
        """
        while z.parent.color == Color.RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self.left_rotate(z.parent.parent)
        self.root.color = Color.BLACK

    def delete_node(self, z):
        """
        Deletes the node z from the tree.  z should exist in the tree.
        """
        if z.left is self.null_node or z.right is self.null_node:
            y = z
        else:
            y = self.tree_successor(z)
        if y.left is not self.null_node:
            x = y.left
        else:
            x = y.right
        x.parent = y.parent
        if y.parent is self.null_node:
            self.root = x
        else:
            if y is y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        if y is not z:
            z.item = y.item
        if y.color == Color.BLACK:
            self.delete_fixup(x)
        self.size -= 1

    def delete_fixup(self, x):
        """
        Restores the red-black tree property after a deletion.
        """
        while x is not self.root and x.color == Color.BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = Color.BLACK  
        self.root.parent = self.null_node
           
    def left_rotate(self, x):
        """
        Performs left rotation rooted at the node x.
        """
        y = x.right
        x.right = y.left
        if y.left is not self.null_node:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self.null_node:
            self.root = y
        else:
            if x is x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self, y):
        """
        Performs a right rotation rooted at the node y.
        """
        x = y.left
        y.left = x.right
        if x.right is not self.null_node:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self.null_node:
            self.root = x
        else:
            if y is y.parent.left:
                y.parent.left = x
            else:
                y.parent.right = x
        x.right = y
        y.parent = x

    def tree_successor(self, x):
        """
        Return the node that contains the next largest
        value in the tree after x.  Returns the null node
        if there is no next largest.
        """
        if x.right is not self.null_node:
            return self.tree_minimum(x.right)
        y = x.parent
        while y is not self.null_node and x is y.right:
            x = y
            y = y.parent
        return y
    
    def tree_minimum(self, x):
        """
        Returns the node in the subtree rooted
        at x containing the minimum item.
        """
        while x.left is not self.null_node:
            x = x.left
        return x