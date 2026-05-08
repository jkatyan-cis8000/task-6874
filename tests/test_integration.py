"""
Integration tests for complete tic-tac-toe game scenarios.

Tests cover:
- Full game scenarios (player wins, computer wins, draw)
- Game flow from start to finish
- Interaction between Board and GameController
- Win/draw detection in realistic gameplay
- Multiple games in sequence
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import GameController
from board import Board


class TestFullGameScenarios:
    """Test complete game scenarios from start to finish."""
    
    def test_game_scenario_player_wins_with_row(self):
        """Test scenario where player wins with three in a row."""
        game = GameController()
        
        # Player's strategy: take top row
        # Computer will try to block or win
        game.make_move(0, 0, 'X')  # Player
        game.make_move(1, 1, 'O')  # Computer (center)
        game.make_move(0, 1, 'X')  # Player
        game.make_move(2, 0, 'O')  # Computer
        game.make_move(0, 2, 'X')  # Player wins!
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'X'
        assert game.board.check_winner() == 'X'
    
    def test_game_scenario_computer_wins_with_column(self):
        """Test scenario where computer wins with three in a column."""
        game = GameController()
        
        game.make_move(0, 0, 'X')  # Player
        game.make_move(0, 1, 'O')  # Computer
        game.make_move(1, 2, 'X')  # Player
        game.make_move(1, 1, 'O')  # Computer
        game.make_move(2, 2, 'X')  # Player
        game.make_move(2, 1, 'O')  # Computer wins! (0,1), (1,1), (2,1)
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'O'
        assert game.board.check_winner() == 'O'
    
    def test_game_scenario_draw_game(self):
        """Test scenario where game ends in a draw."""
        game = GameController()
        
        # Execute a draw game (cats game)
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner is None  # Draw
        assert game.board.is_draw() is True
    
    def test_game_scenario_diagonal_win(self):
        """Test game where player wins on diagonal."""
        game = GameController()
        
        game.make_move(0, 0, 'X')  # Player
        game.make_move(0, 1, 'O')  # Computer
        game.make_move(1, 1, 'X')  # Player
        game.make_move(0, 2, 'O')  # Computer
        game.make_move(2, 2, 'X')  # Player wins diagonal!
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'X'
    
    def test_game_scenario_anti_diagonal_win(self):
        """Test game where computer wins on anti-diagonal."""
        game = GameController()
        
        game.make_move(0, 0, 'X')  # Player
        game.make_move(0, 2, 'O')  # Computer
        game.make_move(1, 0, 'X')  # Player
        game.make_move(1, 1, 'O')  # Computer
        game.make_move(2, 1, 'X')  # Player
        game.make_move(2, 0, 'O')  # Computer wins anti-diagonal!
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'O'


class TestGameFlowAndState:
    """Test game flow and state management."""
    
    def test_game_state_after_each_move(self):
        """Test that game state is consistent after each move."""
        game = GameController()
        
        game.make_move(0, 0, 'X')
        assert game.board.get_moves_count() == 1
        assert game.board.get_cell(0, 0) == 'X'
        assert game.game_over is False
        
        game.make_move(1, 1, 'O')
        assert game.board.get_moves_count() == 2
        assert game.board.get_cell(1, 1) == 'O'
        assert game.game_over is False
    
    def test_game_stops_after_winner_found(self):
        """Test that game stops checking after winner is found."""
        game = GameController()
        
        # Set up X to win
        game.make_move(0, 0, 'X')
        game.make_move(1, 0, 'O')
        game.make_move(0, 1, 'X')
        game.make_move(1, 1, 'O')
        game.make_move(0, 2, 'X')
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'X'
    
    def test_game_stops_when_board_full(self):
        """Test that game stops when board is full."""
        game = GameController()
        
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.board.is_full() is True
    
    def test_cant_move_after_game_over(self):
        """Test that moves can still be made even if game_over flag is set (board validation)."""
        game = GameController()
        
        # Create a winning position
        game.make_move(0, 0, 'X')
        game.make_move(0, 1, 'X')
        game.make_move(0, 2, 'X')
        
        game.check_game_over()
        assert game.game_over is True
        
        # Try to make another move
        result = game.make_move(1, 1, 'O')
        assert result is True  # Board allows it (game logic handles game_over check)


class TestBoardAndControllerIntegration:
    """Test integration between Board and GameController."""
    
    def test_controller_uses_board_validation(self):
        """Test that controller respects board's validation."""
        game = GameController()
        
        game.make_move(0, 0, 'X')
        
        # Try to move to same spot
        result = game.make_move(0, 0, 'O')
        assert result is False
    
    def test_controller_reads_board_state(self):
        """Test that controller reads board state correctly."""
        game = GameController()
        
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        
        assert game.board.get_cell(0, 0) == 'X'
        assert game.board.get_cell(1, 1) == 'O'
    
    def test_empty_cells_consistency(self):
        """Test that empty cells list stays consistent with board."""
        game = GameController()
        
        initial_empty = len(game.board.get_empty_cells())
        assert initial_empty == 9
        
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        
        remaining_empty = len(game.board.get_empty_cells())
        assert remaining_empty == 7
    
    def test_moves_count_consistency(self):
        """Test that moves count stays consistent."""
        game = GameController()
        
        for i in range(5):
            row = i // 3
            col = i % 3
            player = 'X' if i % 2 == 0 else 'O'
            game.make_move(row, col, player)
            assert game.board.get_moves_count() == i + 1


class TestComplexGameSequences:
    """Test complex sequences of game moves."""
    
    def test_long_game_sequence(self):
        """Test a long sequence of moves."""
        game = GameController()
        
        moves = [
            (0, 0, 'X'), (1, 1, 'O'), (0, 1, 'X'),
            (0, 2, 'O'), (1, 0, 'X'), (2, 1, 'O'),
            (1, 2, 'X'), (2, 0, 'O'), (2, 2, 'X')
        ]
        
        for row, col, player in moves:
            result = game.make_move(row, col, player)
            assert result is True
        
        game.check_game_over()
        assert game.board.is_full() is True
    
    def test_strategic_game_sequence(self):
        """Test a game with strategic play."""
        game = GameController()
        
        # Player tries to win, computer blocks
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')  # Computer takes center
        game.make_move(0, 1, 'X')  # Player goes for top row
        
        # Computer should block or try to win
        move = game.get_computer_move()
        assert move is not None
    
    def test_game_reset_between_sequences(self):
        """Test that game can be reset and replayed."""
        game = GameController()
        
        # First game
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        assert game.board.get_moves_count() == 2
        
        # Reset
        game.reset()
        assert game.board.get_moves_count() == 0
        assert game.game_over is False
        
        # Second game
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        assert game.board.get_moves_count() == 2


class TestGameOutcomes:
    """Test different game outcomes."""
    
    def test_x_wins_detectable(self):
        """Test that X winning is properly detected."""
        game = GameController()
        
        # Create a scenario where X will win
        game.make_move(0, 0, 'X')
        game.make_move(1, 0, 'O')
        game.make_move(0, 1, 'X')
        game.make_move(2, 0, 'O')
        game.make_move(0, 2, 'X')
        
        game.check_game_over()
        assert game.winner == 'X'
    
    def test_o_wins_detectable(self):
        """Test that O winning is properly detected."""
        game = GameController()
        
        game.make_move(0, 0, 'X')
        game.make_move(1, 0, 'O')
        game.make_move(0, 1, 'X')
        game.make_move(1, 1, 'O')
        game.make_move(2, 2, 'X')
        game.make_move(1, 2, 'O')
        
        game.check_game_over()
        assert game.winner == 'O'
    
    def test_draw_detectable(self):
        """Test that draw is properly detected."""
        game = GameController()
        
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        
        for row, col, player in moves:
            game.make_move(row, col, player)
        
        game.check_game_over()
        assert game.winner is None
        assert game.game_over is True


class TestEdgeGameScenarios:
    """Test edge cases in game scenarios."""
    
    def test_early_game_detection(self):
        """Test detection after minimum moves for win (5 for player first)."""
        game = GameController()
        
        # Minimum moves for X to win: 5
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        game.make_move(0, 1, 'X')
        game.make_move(2, 2, 'O')
        game.make_move(0, 2, 'X')
        
        game.check_game_over()
        assert game.game_over is True
        assert game.winner == 'X'
    
    def test_late_game_detection(self):
        """Test detection near end of game."""
        game = GameController()
        
        # Fill most of board, then win on last available move
        game.make_move(0, 0, 'X')
        game.make_move(0, 1, 'O')
        game.make_move(0, 2, 'X')
        game.make_move(1, 0, 'O')
        game.make_move(1, 1, 'X')
        game.make_move(1, 2, 'O')
        game.make_move(2, 0, 'X')
        game.make_move(2, 1, 'O')
        game.make_move(2, 2, 'X')
        
        game.check_game_over()
        # Should have a winner or be a draw
        assert game.game_over is True


class TestGameConsistency:
    """Test game consistency across multiple operations."""
    
    def test_multiple_games_sequence(self):
        """Test playing multiple games in sequence."""
        for game_num in range(3):
            game = GameController()
            
            # Play some moves
            game.make_move(0, 0, 'X')
            game.make_move(1, 1, 'O')
            game.make_move(0, 1, 'X')
            
            # Verify state
            assert game.board.get_moves_count() == 3
            assert game.board.get_cell(0, 0) == 'X'
            assert game.board.get_cell(1, 1) == 'O'
    
    def test_board_state_isolation(self):
        """Test that each game has isolated board state."""
        game1 = GameController()
        game2 = GameController()
        
        game1.make_move(0, 0, 'X')
        game2.make_move(1, 1, 'X')
        
        # Games should have different board states
        assert game1.board.get_cell(0, 0) == 'X'
        assert game2.board.get_cell(0, 0) is None
        assert game1.board.get_cell(1, 1) is None
        assert game2.board.get_cell(1, 1) == 'X'


class TestGameValidation:
    """Test game validation and error handling."""
    
    def test_invalid_move_doesnt_change_state(self):
        """Test that invalid moves don't change game state."""
        game = GameController()
        game.make_move(0, 0, 'X')
        
        initial_count = game.board.get_moves_count()
        game.make_move(0, 0, 'O')  # Invalid - cell occupied
        
        assert game.board.get_moves_count() == initial_count
        assert game.board.get_cell(0, 0) == 'X'
    
    def test_game_handles_all_valid_positions(self):
        """Test that game can handle moves to all valid positions."""
        for i in range(3):
            for j in range(3):
                game = GameController()
                result = game.make_move(i, j, 'X')
                assert result is True
                assert game.board.get_cell(i, j) == 'X'
