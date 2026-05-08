"""
Tic-Tac-Toe Game Board Module

This module implements the core Board class that manages the game state for tic-tac-toe.
The Board class handles board initialization, move validation, winner detection, and
game state management.
"""


class Board:
    """
    Represents a tic-tac-toe game board and manages game state.
    
    The board is a 3x3 grid where players can place their marks (X or O).
    The board tracks all moves, validates new moves, and determines game outcomes.
    
    Attributes:
        board (list): A 3x3 nested list representing the game board.
                     Empty cells contain None, X cells contain 'X', O cells contain 'O'.
        _moves_count (int): Number of moves made so far on the board.
    """
    
    def __init__(self):
        """Initialize a new empty tic-tac-toe board."""
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self._moves_count = 0
    
    def is_valid_move(self, row, col):
        """
        Validate whether a move can be made at the specified position.
        
        A move is valid if:
        - The row and column are within bounds (0-2)
        - The cell at that position is empty (None)
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
        
        Returns:
            bool: True if the move is valid, False otherwise.
        """
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        return self.board[row][col] is None
    
    def make_move(self, row, col, player):
        """
        Place a player's mark on the board at the specified position.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            player (str): The player marker ('X' or 'O')
        
        Returns:
            bool: True if the move was successfully made, False if the move is invalid.
        
        Raises:
            ValueError: If player is not 'X' or 'O'
        """
        if player not in ('X', 'O'):
            raise ValueError(f"Invalid player: {player}. Must be 'X' or 'O'")
        
        if not self.is_valid_move(row, col):
            return False
        
        self.board[row][col] = player
        self._moves_count += 1
        return True
    
    def get_cell(self, row, col):
        """
        Get the current state of a cell on the board.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
        
        Returns:
            str or None: 'X', 'O', or None if the cell is empty.
        
        Raises:
            IndexError: If row or col are out of bounds.
        """
        return self.board[row][col]
    
    def get_empty_cells(self):
        """
        Get a list of all empty cells on the board.
        
        Returns:
            list: A list of tuples (row, col) representing empty cells.
        """
        empty_cells = []
        for row in range(3):
            for col in range(3):
                if self.board[row][col] is None:
                    empty_cells.append((row, col))
        return empty_cells
    
    def check_winner(self):
        """
        Check if there is a winner on the board.
        
        A winner is determined by three matching marks in a row, column, or diagonal.
        
        Returns:
            str or None: 'X' if X has won, 'O' if O has won, None if no winner.
        """
        # Check rows
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] 
                and self.board[row][0] is not None):
                return self.board[row][0]
        
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] 
                and self.board[0][col] is not None):
                return self.board[0][col]
        
        # Check diagonal (top-left to bottom-right)
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] 
            and self.board[0][0] is not None):
            return self.board[0][0]
        
        # Check diagonal (top-right to bottom-left)
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] 
            and self.board[0][2] is not None):
            return self.board[0][2]
        
        return None
    
    def is_full(self):
        """
        Check if the board is completely full (no empty cells).
        
        Returns:
            bool: True if the board is full, False otherwise.
        """
        return self._moves_count == 9
    
    def is_draw(self):
        """
        Check if the game has ended in a draw.
        
        A draw occurs when the board is full and there is no winner.
        
        Returns:
            bool: True if the game is a draw, False otherwise.
        """
        return self.is_full() and self.check_winner() is None
    
    def is_game_over(self):
        """
        Check if the game has ended (winner found or board is full).
        
        Returns:
            bool: True if the game is over, False otherwise.
        """
        return self.check_winner() is not None or self.is_full()
    
    def reset(self):
        """
        Reset the board to its initial empty state.
        
        Clears all moves and resets the move counter.
        """
        self.board = [[None, None, None], [None, None, None], [None, None, None]]
        self._moves_count = 0
    
    def get_moves_count(self):
        """
        Get the number of moves made so far.
        
        Returns:
            int: The number of moves made on the board.
        """
        return self._moves_count
    
    def __str__(self):
        """
        Return a user-friendly string representation of the board.
        
        Returns:
            str: A formatted string showing the current board state with row and column numbers.
        """
        output = "\n   0   1   2\n"
        output += "  -----------\n"
        
        for row in range(3):
            output += f"{row} |"
            for col in range(3):
                cell = self.board[row][col]
                if cell is None:
                    output += " . |"
                else:
                    output += f" {cell} |"
            output += "\n"
            if row < 2:
                output += "  -----------\n"
            else:
                output += "  -----------\n"
        
        return output
    
    def display(self):
        """
        Print the board to the console.
        
        This is a convenience method that prints the string representation of the board.
        """
        print(self)
