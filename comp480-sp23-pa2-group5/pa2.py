# File: pa2.py
# Authors: Samuel Cacnio and Christian Gideon  
# Date: 24 March 2023
# Description: Program containing a function
# to solve the problem described in pa2 for comp 480,
# spring 2023.

from rbtree import RBTree

def create_trees(tuples):
    """
    Takes a sorted list of tuples and creates a tree for each
    kind of first element and then fills each tree
    by the second elements
    Returns a list of rbtrees
    """
    trees = []
    last_tree = -1 #last type of first element encountered
    curr_tree = -1 #current tree to add to (by index in trees)
    for i in tuples:
        if i[0] > last_tree: #new encounter --> start new tree
            trees.append(RBTree(lambda x: x[1]))
            curr_tree += 1
            trees[curr_tree].insert(i)
            last_tree = i[0]
        else:
            trees[curr_tree].insert(i)
    return trees

def pa2(filename):
    """
    Solves problem described in pa2 problem statement.
    filename is the name of the file containing the input.
    Should return the result: either None
    if the problem has no solution, or a tuple containing two orders:
    the order of the first set up numbers, and the order of the second
    set of numbers.
    """
    #preprocessing file to create lists of tuples
    f = open(filename)
    size = int(f.readline())
    a0_lst = [int(i) for i in f.readline().split()]
    a1_lst = [int(i) for i in f.readline().split()]
    b0_lst = [int(i) for i in f.readline().split()]
    b1_lst = [int(i) for i in f.readline().split()]
    f.close()
    a = [] #temp storage for tuples
    b = []
    for i in range(size):
        a.append((a0_lst[i],a1_lst[i],i+1)) #tuple of first and second elements according to file format and index (starting at 1)
        b.append((b0_lst[i],b1_lst[i],i+1))
    a = sorted(a)
    b = sorted(b)
    a_forest = create_trees(a) #lists of trees
    b_forest = create_trees(b)
    sol_A = [] #to store original indices of our paired/ordered tuples
    sol_B = []

    #begin algorithm
    a_order = 0 #index of tree in respective list
    b_order = 0
    curr_ATree = a_forest[a_order] #select starting trees
    curr_BTree = b_forest[b_order]
    curr_ANode = ()
    curr_BNode = ()
    while (len(sol_A)<size): #run until solution has 'size' tuples --> complete
        try:
            #if tree is empty, move to next tree --> avoid handling KeyError due to empty tree
            if (len(curr_ATree)==0):
                a_order += 1
            if (len(curr_BTree)==0):
                b_order += 1
            curr_ATree = a_forest[a_order]
            curr_BTree = b_forest[b_order]

            #avoid emptying one list too far before the other
            if (len(curr_ATree) > len(curr_BTree)):
                #if biggest B cannot find match in ATree, fail
                curr_BNode = curr_BTree.delete_max()
                curr_ANode = curr_ATree.delete_smallest_greater_than(curr_BNode)
            else:
                #if smallest A cannot find match in BTree, fail
                curr_ANode = curr_ATree.delete_min()
                curr_BNode = curr_BTree.delete_largest_less_than(curr_ANode)
            
            #append original indices in solutions
            sol_A.append(curr_ANode[2])
            sol_B.append(curr_BNode[2])
        except KeyError:
            return None
    return (sol_A, sol_B)

if __name__ == '__main__':
    """
    Can run this file directly when testing your code.
    """
    ans = pa2("input8.txt")
