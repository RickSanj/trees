"""
module board.py
"""
from arrays import *

class Board:
    """class for board in game tic-tac-toe"""
    def __init__(self) -> None:
        """
        init for board class
        creates 2d array that represents a playing board 3x3
        stores that board and the last move = tuple(symbol, position)*
        * where: symbol is 'x' or '0' ; position = (int, int)
        """
        self.last_mode = None # (symbol, position)
        self.board = Array2D(3,3)

    def get_status(self) -> str:
        """
        function that determines the status of the game
        :return: str - that status, could be "x", "0", "draw", "continue".
        """
        # check horizontal and vertical
        for row in range(3):
            for col in range(3):
                # check vertical
                if self.board[row, col] == self.board[row, col] == self.board[row, col]:
                    return self.board[row, col]
                # check horizontal
                if self.board[col, row] == self.board[col, row] == self.board[col, row]:
                    return self.board[col, row]

        # check diagonal
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2]:
            return self.board[0, 0]
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0]:
            return self.board[0, 2]

        # check if there is empty cell
        for row in range(3):
            for col in range(3):
                if self.board[row, col] not in ['x', '0']:
                    return 'continue'
        return 'draw'

    def make_move(self, position: tuple, turn: str) -> None|IndexError:
        """
        position - tuple with coordinates (start indexing with 0)
        turn - "x" or "0."
        If the move is invalid, IndexError exception is raised
        """
        try:
            if position[0] in [0, 1, 2] and position[1] in [0, 1, 2] and \
self.board[position[0], position[1]] not in ['x', '0']:
                self.board[position[0], position[1]] = turn
            else:
                raise IndexError
        except IndexError as exc:
            raise exc from IndexError

    def make_computer_move(self):
        """
        make a move for a computer player
        """
        pass