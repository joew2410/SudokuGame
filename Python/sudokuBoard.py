# -*- coding: utf-8 -*-
"""
@filename: sudokuBoard.py
@author: Joe Walker

@description: This file implements the sudoku board

"""

import copy
import csv


class sudokuBoard:
    """
    This class implements the sudoku board
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor class
            Arguments:

            Keyword arguments:

            Outputs:
                None
        """

        boardList = kwargs.get('boardList', [])
        boardCSV = kwargs.get('boardCSV', '')

        if(boardList != []):
            self.startBoard = copy.deepcopy(boardList)
        elif(boardCSV != ''):
            with open(boardCSV) as f:
                reader = csv.reader(f)
                board = [list(map(int, i)) for i in list(reader)]
                self.startBoard = copy.deepcopy(board)
        else:
            # Default board
            self.startBoard = [[0, 8, 0, 0, 0, 0, 2, 0, 0],
                               [0, 0, 0, 0, 8, 4, 0, 9, 0],
                               [0, 0, 6, 3, 2, 0, 0, 1, 0],
                               [0, 9, 7, 0, 0, 0, 0, 8, 0],
                               [8, 0, 0, 9, 0, 3, 0, 0, 2],
                               [0, 1, 0, 0, 0, 0, 9, 5, 0],
                               [0, 7, 0, 0, 4, 5, 8, 0, 0],
                               [0, 3, 0, 7, 1, 0, 0, 0, 0],
                               [0, 0, 8, 0, 0, 0, 0, 4, 0]]

        self.board = copy.deepcopy(self.startBoard)

        self.moveHistory = []

        return

    def print(self):
        """
        This method prints the board in a more readable format

        Inputs:

        Outputs:
        """
        print("-------------------------")
        for rowNum, row in enumerate(self.board, start=1):
            formattedRow = "| "
            for index, value in enumerate(row, start=1):
                formattedRow += (str(value) + " ")

                if((index % 3) == 0):
                    formattedRow += "| "

            print(formattedRow)

            if((rowNum % 3) == 0):
                print("-------------------------")

    def insertNumber(self, x, y, number):
        """
        This method is used to insert a number into the board

        Takes in:
            x - x coordinate of the square to be insert
            y - y coordinate of the square to be insert
            number - the number to be inserted to the square
        """

        # Check the input number is between 0 and 9
        if((0 <= number <= 9) == False):
            print("Invalid input, input must be between 0 and 9")
            return False

        # check the coordinate is valid
        if(((0 <= x <= 8) & (0 <= y <= 8)) == False):
            print("Invalid x or y coordinate")
            return False

        # check the move is valid
        if self.checkValid(x, y, number):

            # record the move in move history
            self.moveHistory.append([x, y, self.board[y][x], number])

            # Insert the value into the grid
            self.board[y][x] = number
            print("valid move")
            return True
        else:
            print("invalid move")
            return False

    def checkValid(self, x, y, number):
        """
        This function checks if a proposed move is valid or not applying classical sudoku rules

        Takes in:
            x - x coordinate
            y - y coordinate
            number - number to be inserted

        Returns:
            bool indicating whether or not the move is valid
        """

        # Check move is valid for non-zero inputs
        if number != 0:

            # check the row
            if number in self.board[y]:
                return False

            # check the column
            for row in self.board:
                if row[x] == number:
                    return False

            # Check the box
            x0 = (x//3)*3
            y0 = (y//3)*3
            for i in range(3):
                for j in range(3):
                    yn = y0 + i
                    xn = x0 + j
                    if self.board[yn][xn] == number:
                        return False

        # If it was one of the given digits, move is deemed invalid
        if((self.board[y][x] != 0) & (self.board[y][x] == self.startBoard[y][x])):
            return False

        return True

    def resetBoard(self):
        """
        Method used to reset the board back to the start board

        Takes in:

        Returns:
        """

        self.board = copy.deepcopy(self.startBoard)
        self.moveHistory = []

    def undoMove(self):
        """
        Method to undo the last move made
        """

        if(self.moveHistory != []):

            # revert previous move
            x, y, prevVal, newVal = self.moveHistory[-1]
            self.board[y][x] = prevVal

            # remove move from move history
            self.moveHistory = self.moveHistory[0:-1]

            return True

        return False    # indicate that there are no moves in the history

    def solve(self):
        """
        This method implements a sudoku solver using recursion
        """

        for y in range(9):
            for x in range(9):
                if self.board[y][x] == 0:
                    for n in range(1, 10):
                        if self.insertNumber(x, y, n):
                            if self.solve():
                                return True
                            self.insertNumber(x, y, 0)
                    return False
        return True


if __name__ == "__main__":

    # Load board from list example
    myBoard = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
               [6, 0, 0, 1, 9, 5, 0, 0, 0],
               [0, 9, 8, 0, 0, 0, 0, 6, 0],
               [8, 0, 0, 0, 6, 0, 0, 0, 3],
               [4, 0, 0, 8, 0, 3, 0, 0, 1],
               [7, 0, 0, 0, 2, 0, 0, 0, 6],
               [0, 6, 0, 0, 0, 0, 2, 8, 0],
               [0, 0, 0, 4, 1, 9, 0, 0, 5],
               [0, 0, 0, 0, 8, 0, 0, 7, 9]]
    testBoard = sudokuBoard(boardList=myBoard)

    # Load default board example
    # testBoard = sudokuBoard()

    # # Load board from csv example
    # import os
    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, '../Boards/CSV/testBoard.csv')
    # testBoard = sudokuBoard(boardCSV=filename)

    testBoard.print()

    testBoard.solve()
    testBoard.print()

    # # Main game loop
    # while(any(0 in row for row in testBoard.board)):
    #     x = int(input('X coordinate: '))
    #     y = int(input('Y coordinate: '))
    #     number = int(input('Number to insert: '))
    #     testBoard.insertNumber(x, y, number)
    #     testBoard.print()

    print("You win!!!")
