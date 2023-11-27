# File: pa4.py
# Authors: Samuel Cacnio and Christian Gideon
# Date: 5/12/23
# Description: Helper file for PA4 sudoku solver

import math

class Node:
    """
    Stores an assignment of numbers to cells for a game of Sudoku
    """
    def __init__(self, size, cells, filled):
        """
        size (int) - stores base size of Sudoku game (3 if 3x3, 4 if 4x4, etc.)
        cells (list[Cell]) - 2D list of all Sudoku cells by row and column
        filled (int) - stores number of cells currently filled
        """
        self.size = size
        self.cells = cells
        self.filled = filled

    def __str__(self) -> str:
        """
        Returns string representation of the Sudoku game state
        """
        string = ""
        for row in self.cells:
            for cell in row:
                if cell.value is None:
                    string += "_ "
                else:
                    string += str(cell.value) + " "
            string += "\n"
        return string
    
    def find_row(self, curr_cell):
        """
        Returns a list of Cells that are in the same row as curr_cell
        """
        row = []
        for cell in self.cells[curr_cell.row]:
            if cell is not curr_cell:
                row.append(cell)
        return row
    
    def find_column(self, curr_cell):
        """
        Returns a list of Cells that are in the same column as curr_cell
        """
        column = []
        for i in range(self.size): # Size of the grid
            cell = self.cells[i][curr_cell.column]
            if cell is not curr_cell:
                column.append(cell)
        return column
    
    def find_subgrid(self, curr_cell):
        """
        Returns a list of Cells that are in the same subgrid as curr_cell
        """
        square = []
        subsize = int(math.sqrt(self.size))
        subgrid_row = (curr_cell.row // subsize) * subsize
        subgrid_column = (curr_cell.column // subsize) * subsize
        for row in range(subgrid_row, subgrid_row + subsize):
            for column in range(subgrid_column, subgrid_column + subsize):
                cell = self.cells[row][column]
                if cell is not curr_cell:
                    square.append(cell)
        return square

    def set_cell(self, row, col, val):
        """
        Places a value in a cell and makes cutoffs based on the assignment

        Parameters:
        row (int) - row of cell object in Sudoku game to access
        col (int) - columnn of cell object in Sudoku game to access
        val (str) - value to place in the cell object

        Returns:
        False if the assignment leads to an impossible Sudoku state
        True if the assignment is legal
        """
        cell = self.cells[row][col]
        if cell.value == None:
            self.filled += 1
            cell.set_val(val)
            valid_by_option = self.elimOptions(cell)
            if valid_by_option == False:
                return False
            valid_by_elim = self.set_by_viable(cell)
            if valid_by_elim == False:
                return False
        return True
        

    def elimOptions(self, curr_cell):
        """
        Checks and eliminates possibilities after updating a cell
        
        Parameters:
            curr_cell (Cell) - the cell to be used in reference to the eliminations being made
        
        Returns:
            new_singles (Queue) - the queue of cells with only one option remaining.
            False when an impossible combination was found - a cutoff
            True if eliminating options does not find a cutoff
        """
        new_singles = []
        
        #Eliminate possibilities for each empty cell in the same row, column, and subgrid as the current cell
        row = self.find_row(curr_cell)
        col = self.find_column(curr_cell)
        subgrid = self.find_subgrid(curr_cell)
        candidates = list(set().union(row,col,subgrid))
        for cell in candidates:
            if cell.value is None:
                if len(cell.options) == 0: #if cell isn't filled but has no options, we have an impossible game
                    return False
                if curr_cell.value in cell.options:
                    cell.options.remove(curr_cell.value)
                    #When deleting options, if only one value left add the cell to queue for later
                    if len(cell.options) == 1:
                        new_singles.append(cell)

        #If any basic eliminations resulted in a single option remaining, take care of the option now as another cutoff
        if len(new_singles)>0:
            for single in new_singles:
                if single.value == None: #Cutting out singles that had their last option eliminated before this step
                    if len(single.options) == 0:
                        return False
                    #If this isn't the case (this is a real single), then set this cell to the only remaining option
                    valid = self.set_cell(single.row, single.column, single.options[0])
                    if valid == False:
                        return False
                new_singles.remove(single)
        return True
    

    def set_by_viable(self, curr_cell):
        """
        Looks through 'neighborhood' of curr_cell and fills cells if they are the only candidate in their neighborhood
        to be a given value per Sudoku rules

        Parameters:
        curr_cell (Cell) - current cell to perform eliminations from

        Returns:
        False if a dead end or cutoff is encountered
        True if assignments are legal
        """
        if self.filled == self.size ** 2:
            return True
        if self.size == 9: # size is 9 x 9 grid
            options = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        elif self.size == 16: # size is 16 x 16 grid
            options = ["1", "2", "3", "4", "5", "6", "7", "8", "9",
                    "A", "B", "C", "D", "E", "F", "G"]
        else: # size is 25 x 25 grid
            options = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J",
                    "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
                    "U", "V", "W", "X", "Y"]
        row = self.find_row(curr_cell)
        col = self.find_column(curr_cell)
        sub = self.find_subgrid(curr_cell)
        #for each possible value, check if row/column/subgrid has only one cell able to take that value
        for val in options:
            for group in [row, col, sub]:
                group_ops = []
                for cell in group:
                    group_ops += cell.options
                    if val in cell.options:
                        candidate = cell
                if group_ops.count(val)==1:
                    group_valid = self.set_cell(candidate.row, candidate.column, val)
                    if group_valid == False:
                        return False
        return True
        

class Cell:
    """
    An instance of an individual cell in a game of Sudoku with key attributes attached
    """

    def __init__(self, row, column, value, options):
        """
        row (int) - y coordinate of cell in relation to Sudoku game
        col (int) - x coordinate of cell in relation to Sudoku game
        value (str) - current value stored in cell per Sudoku rules
        options (list[str]) - list of values that the cell could possibly hold per Sudoku rules
        """
        self.row = row
        self.column = column
        self.value = value
        self.options = options
    
    def __str__(self) -> str:
        """
        Returns string representation fo cell.value
        or '_' if no value in self.value
        """
        if self.value == None:
            return "_"
        return str(self.value)
    
    def set_val(self, val):
        """
        Sets self.value to val and erases remaining options
        """
        self.value = str(val)
        self.options = []

    #compare cells by length of options list for sorting
    def __le__(self, other):
        return len(self.options) <= len(other.options)

    def __gt__(self, other):
        return len(self.options) > len(other.options)