"""
Tic-Tac-Toe Game Module

This module implements the game controller that orchestrates the tic-tac-toe gameplay.
It handles turn management, player input, AI strategy, and game flow.
"""

import sys
import random
from board import Board


class GameController:
    """
    Controls the flow of a tic-tac-toe game.
    
    Manages:
    - Game state and turns (X for player, O for computer)
    - User input handling and move validation
    - AI player with strategic decision-making
    - Game loop execution
    - Win/draw detection and game outcomes
    """
    
    def __init__(self):
        """Initialize a new game controller with a fresh board."""
        self.board = Board()
        self.player = 'X'  # Human player
        self.computer = 'O'  # AI player
        self.current_player = self.player  # Player always goes first
        self.game_over = False
        self.winner = None
    
    def display_board(self):
        """Display the current board state."""
        print("\n" + str(self.board))
    
    def get_player_move(self):
        """
        Get a valid move from the player via user input.
        
        Prompts the user to enter a position (0-8) on the board.
        Validates the input and ensures the move is legal.
        
        Returns:
            tuple: (row, col) representing the valid move
        """
        while True:
            try:
                position = input("Your move (0-8): ").strip()
                
                # Validate input is a number
                if not position.isdigit():
                    print("Invalid input. Please enter a number between 0 and 8.")
                    continue
                
                position = int(position)
                
                # Validate position is in range
                if position < 0 or position > 8:
                    print("Invalid position. Please enter a number between 0 and 8.")
                    continue
                
                # Convert linear position (0-8) to row, col
                row = position // 3
                col = position % 3
                
                # Check if the move is valid on the board
                if not self.board.is_valid_move(row, col):
                    print("That position is already occupied. Choose another.")
                    continue
                
                return (row, col)
            
            except Exception as e:
                print(f"Error: {e}. Please try again.")
    
    def get_computer_move(self):
        """
        Determine the computer's next move using strategic AI.
        
        Strategy priority:
        1. Win: If computer can win in one move, take it
        2. Block: If player can win in one move, block them
        3. Center: If center (1,1) is empty, take it
        4. Corners: Take a random corner if available
        5. Sides: Take a random side if available
        
        Returns:
            tuple: (row, col) representing the computer's move
        """
        empty_cells = self.board.get_empty_cells()
        
        if not empty_cells:
            return None
        
        # Priority 1: Check if computer can win
        for row, col in empty_cells:
            self.board.make_move(row, col, self.computer)
            if self.board.check_winner() == self.computer:
                self.board.board[row][col] = None  # Undo the move
                self.board._moves_count -= 1
                return (row, col)
            self.board.board[row][col] = None  # Undo the move
            self.board._moves_count -= 1
        
        # Priority 2: Check if player can win and block them
        for row, col in empty_cells:
            self.board.make_move(row, col, self.player)
            if self.board.check_winner() == self.player:
                self.board.board[row][col] = None  # Undo the move
                self.board._moves_count -= 1
                return (row, col)
            self.board.board[row][col] = None  # Undo the move
            self.board._moves_count -= 1
        
        # Priority 3: Take the center if available
        if (1, 1) in empty_cells:
            return (1, 1)
        
        # Priority 4: Take a corner if available
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        available_corners = [corner for corner in corners if corner in empty_cells]
        if available_corners:
            return random.choice(available_corners)
        
        # Priority 5: Take any available side
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        available_sides = [side for side in sides if side in empty_cells]
        if available_sides:
            return random.choice(available_sides)
        
        # Fallback: return any available cell
        return empty_cells[0] if empty_cells else None
    
    def make_move(self, row, col, player):
        """
        Execute a move on the board and update game state.
        
        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)
            player (str): The player making the move ('X' or 'O')
        
        Returns:
            bool: True if the move was successful, False otherwise
        """
        return self.board.make_move(row, col, player)
    
    def check_game_over(self):
        """
        Check if the game has ended and determine the outcome.
        
        Updates game_over and winner attributes.
        """
        winner = self.board.check_winner()
        
        if winner:
            self.game_over = True
            self.winner = winner
        elif self.board.is_draw():
            self.game_over = True
            self.winner = None  # Draw
    
    def play_turn(self):
        """
        Execute one complete turn of the game.
        
        Handles getting input, making a move, and switching players.
        """
        if self.current_player == self.player:
            # Player's turn
            print("\n--- Your Turn (X) ---")
            row, col = self.get_player_move()
            self.make_move(row, col, self.player)
            self.current_player = self.computer
        else:
            # Computer's turn
            print("\n--- Computer's Turn (O) ---")
            move = self.get_computer_move()
            if move:
                row, col = move
                self.make_move(row, col, self.computer)
                print(f"Computer plays position {row * 3 + col}")
            self.current_player = self.player
    
    def run_game(self):
        """
        Run a complete game loop until a winner or draw is determined.
        
        Displays the board, handles turns, and announces the outcome.
        """
        print("\n" + "=" * 40)
        print("     WELCOME TO TIC-TAC-TOE!")
        print("=" * 40)
        print("You are X, Computer is O")
        print("Positions are numbered 0-8:")
        print("  0 | 1 | 2")
        print("  ---------")
        print("  3 | 4 | 5")
        print("  ---------")
        print("  6 | 7 | 8")
        print("=" * 40)
        
        # Game loop
        while not self.game_over:
            self.display_board()
            self.play_turn()
            self.check_game_over()
        
        # Game over - announce result
        self.display_board()
        print("\n" + "=" * 40)
        if self.winner == self.player:
            print("🎉 You won! Congratulations!")
        elif self.winner == self.computer:
            print("💻 Computer won! Better luck next time.")
        else:
            print("🤝 It's a draw!")
        print("=" * 40)
    
    def reset(self):
        """Reset the game controller for a new game."""
        self.board.reset()
        self.game_over = False
        self.winner = None
        self.current_player = self.player


def main():
    """
    Main entry point for the tic-tac-toe game.
    
    Runs the game loop and prompts the user to play again after each game.
    """
    play_again = True
    
    while play_again:
        game = GameController()
        game.run_game()
        
        # Ask if user wants to play again
        while True:
            response = input("\nDo you want to play again? (yes/no): ").strip().lower()
            if response in ('yes', 'y'):
                play_again = True
                break
            elif response in ('no', 'n'):
                play_again = False
                break
            else:
                print("Please enter 'yes' or 'no'.")
    
    print("\nThanks for playing! Goodbye!")


if __name__ == "__main__":
    main()
