# File: pa3.py
# Authors: Samuel Cacnio, Christian Gideon
# Date: 14 April 2023
# Description: Solves the stone-grid problem: calculates the most
# optimal spot for a certain amount of stones within a certain distance.

def solve(filename):
    """
    Solves pa3.  Input to problem is in the file named filename.
    Output should be printed to standard output (using print statement).
    """

    #preprocessing first file
    f = open(filename)
    prob_setup = f.readline().split()
    case = 1
    while prob_setup != ["0", "0", "0", "0"]:
        #problem setup
        cols = int(prob_setup[0])
        rows = int(prob_setup[1])
        stone_count = int(prob_setup[2])
        q_count = int(prob_setup[3])
        offset = rows - 1

        grid = [0]*(abs(1-rows-(cols-1))+1) #columns outside ("big"), rows inside ("small")
        #grid conversion/setup
        for col in range(len(grid)):
            grid[col] = [0]*(cols+rows-1)

        for i in range(stone_count):
            coords = f.readline().split()
            new_x = int(coords[0]) - int(coords[1]) #change-var formulas
            new_y = int(coords[0]) + int(coords[1])
            stone = (new_x,new_y)
            grid[stone[0]+offset][stone[1]-2] = 1 #adjust change-var stone coords to fit in python indices
        

        #create matrix to track stones within area originating from origin
        count = count_matrix(grid)

        #go through queries
        print("Case " + str(case) + ":")
        for i in range(q_count):
            distance = int(f.readline())
            x, y, num_stones = most_stones(count, distance, offset)
            print(str(num_stones) + " (" + str(x) + "," + str(y) + ")")

        case += 1
        prob_setup = f.readline().split()



def count_matrix(grid):
    """
    Creates a matrix based on the given grid with stones where an entry contains
    the number of stones in a rectangular area originating from the lower-left
    corner to the current position.

    Args:
        grid (2D grid): the transformed matrix to work with.

    Returns:
        matrix (2D grid): contains amount of stones away from bottom left index for all indices
    """
    
    matrix = [0]*(len(grid))
    rows = range(len(grid[0]))
    row_count = dict.fromkeys(rows,0) #track number of stones in a row
    for col in range(len(grid)):
        matrix[col]=[0]*len(grid[0])
        for row in rows:
            adjacency = 0 #number of stones located in respective area
            if col != 0:
                adjacency += row_count[row]
            if row != 0:
                adjacency += matrix[col][row-1] #since we traverse list by column, adjacency from lower cells sustains
            if grid[col][row] == 1:
                adjacency += 1
                row_count[row] += 1
            matrix[col][row] = adjacency
    return matrix


def most_stones(matrix, distance, offset):
    """
    Finds point in count matrix in proximity (distance) of the most stones

    Args:
        matrix (2D grid): contains amount of stones away from bottom left index for all indices
        distance (int): the distance away from a point stones are allowed to be
        offset (int): used for reverting points back to original graph

    Returns:
        best_point[0] (int): the column value for the best query answer
        best_point[1] (int): the row value for the best query answer
        max_stones (int): the number of stones that are within range of the best_point
    """

    best_point = (1, 1)
    max_stones = 0
    for row in range(len(matrix[0])):
        for col in range(len(matrix)):
            #adding the amount of stones within the specified distance of a point
            stones = matrix[min(col+distance,len(matrix)-1)][min(row+distance,len(matrix[0])-1)]
            if (col-distance-1) >= 0:
                stones -= matrix[max(0,col-distance-1)][min(row+distance,len(matrix[0])-1)]
            if (row-distance-1) >= 0:
                stones -= matrix[min(col+distance,len(matrix)-1)][max(0,row-distance-1)]
            if (max(0,col-distance-1) == 0 and max(0,row-distance-1) == 0) == False:
                stones += matrix[max(0,col-distance-1)][max(0,row-distance-1)]

            #skipping non-existent points by checking them when reverted
            i = (col - offset)
            j = (row + 2)
            revert_x = (i+j)/2
            revert_y = (j-i)/2
            if revert_x.is_integer() == False or revert_y.is_integer == False:
                continue
            else:
                revert_x = int(revert_x)
                revert_y = int(revert_y)
            cand = (revert_x, revert_y)

            #finding new best position to solve the problem
            if stones >= max_stones and cand[0] > 0 and cand[1] > 0:
                if stones > max_stones:
                    max_stones = stones
                    best_point = cand
                elif stones == max_stones:
                    if cand[1] < best_point[1]:
                        max_stones = stones
                        best_point = cand
                    elif cand[1] == best_point[1]:
                        if cand[0] < best_point[0]:
                            max_stones = stones
                            best_point = cand

    return best_point[0], best_point[1], max_stones
            
    
if __name__ == "__main__":
    solve("test1.in")
