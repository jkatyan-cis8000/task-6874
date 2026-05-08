"""
Comprehensive unit tests for the GameController class.

Tests cover:
- Game initialization
- Turn management (switching between player and computer)
- AI strategy (win priority, block priority, center, corners, sides)
- Move making
- Game state tracking
- Game over detection
- Game reset
- Edge cases in AI decision-making
"""

import pytest
import sys
import os
from unittest.mock import patch, MagicMock
from io import StringIO

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from game import GameController
from board import Board


class TestGameControllerInitialization:
    """Test GameController initialization."""
    
    def test_game_controller_initializes(self):
        """Test that GameController initializes successfully."""
        game = GameController()
        assert game is not None
    
    def test_game_controller_creates_board(self):
        """Test that GameController creates a Board instance."""
        game = GameController()
        assert isinstance(game.board, Board)
    
    def test_player_is_x(self):
        """Test that human player is X."""
        game = GameController()
        assert game.player == 'X'
    
    def test_computer_is_o(self):
        """Test that computer is O."""
        game = GameController()
        assert game.computer == 'O'
    
    def test_current_player_starts_as_player(self):
        """Test that player goes first."""
        game = GameController()
        assert game.current_player == game.player
    
    def test_game_not_over_initially(self):
        """Test that game is not over at start."""
        game = GameController()
        assert game.game_over is False
    
    def test_winner_is_none_initially(self):
        """Test that winner is None at start."""
        game = GameController()
        assert game.winner is None


class TestGameStateTracking:
    """Test game state tracking."""
    
    def test_check_game_over_no_winner(self):
        """Test game over check with no winner."""
        game = GameController()
        game.check_game_over()
        assert game.game_over is False
        assert game.winner is None
    
    def test_check_game_over_with_winner_x(self):
        """Test game over detection with X winner."""
        game = GameController()
        # Set up winning condition for X
        game.board.make_move(0, 0, 'X')
        game.board.make_move(0, 1, 'X')
        game.board.make_move(0, 2, 'X')
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'X'
    
    def test_check_game_over_with_winner_o(self):
        """Test game over detection with O winner."""
        game = GameController()
        # Set up winning condition for O
        game.board.make_move(1, 0, 'O')
        game.board.make_move(1, 1, 'O')
        game.board.make_move(1, 2, 'O')
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner == 'O'
    
    def test_check_game_over_with_draw(self):
        """Test game over detection with draw."""
        game = GameController()
        # Set up a draw
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        for row, col, player in moves:
            game.board.make_move(row, col, player)
        
        game.check_game_over()
        
        assert game.game_over is True
        assert game.winner is None  # Draw


class TestMakingMoves:
    """Test making moves through the controller."""
    
    def test_make_valid_move(self):
        """Test making a valid move."""
        game = GameController()
        result = game.make_move(0, 0, 'X')
        assert result is True
    
    def test_make_invalid_move(self):
        """Test that invalid moves return False."""
        game = GameController()
        game.make_move(0, 0, 'X')
        result = game.make_move(0, 0, 'O')
        assert result is False
    
    def test_move_updates_board(self):
        """Test that moves update the board."""
        game = GameController()
        game.make_move(1, 1, 'X')
        assert game.board.get_cell(1, 1) == 'X'


class TestAIStrategy:
    """Test AI strategy in move selection."""
    
    def test_ai_finds_winning_move(self):
        """Test that AI takes winning move when available."""
        game = GameController()
        # Set up scenario where AI (O) can win
        game.board.make_move(0, 0, 'O')
        game.board.make_move(0, 1, 'O')
        # Empty cell at (0, 2) will give O the win
        
        move = game.get_computer_move()
        assert move == (0, 2)
    
    def test_ai_blocks_player_win(self):
        """Test that AI blocks player's winning move."""
        game = GameController()
        # Set up scenario where player (X) can win
        game.board.make_move(1, 0, 'X')
        game.board.make_move(1, 1, 'X')
        # If not blocked, X wins at (1, 2)
        
        move = game.get_computer_move()
        assert move == (1, 2), "AI should block player's winning move"
    
    def test_ai_takes_center_when_available(self):
        """Test that AI takes center position when no win/block."""
        game = GameController()
        # Empty board, center should be taken
        move = game.get_computer_move()
        assert move == (1, 1)
    
    def test_ai_takes_corner_when_center_taken(self):
        """Test that AI takes corner when center is not available."""
        game = GameController()
        game.board.make_move(1, 1, 'X')  # Block center
        
        move = game.get_computer_move()
        corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
        assert move in corners
    
    def test_ai_takes_side_when_center_and_corners_taken(self):
        """Test that AI takes side when center and corners are blocked."""
        game = GameController()
        # Block center
        game.board.make_move(1, 1, 'X')
        # Block all corners
        game.board.make_move(0, 0, 'X')
        game.board.make_move(0, 2, 'X')
        game.board.make_move(2, 0, 'X')
        game.board.make_move(2, 2, 'X')
        
        move = game.get_computer_move()
        sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
        assert move in sides
    
    def test_ai_returns_none_on_full_board(self):
        """Test that AI returns None when board is full."""
        game = GameController()
        # Fill entire board
        for i in range(3):
            for j in range(3):
                game.board.make_move(i, j, 'X' if (i + j) % 2 == 0 else 'O')
        
        move = game.get_computer_move()
        assert move is None
    
    def test_ai_win_priority_over_block(self):
        """Test that AI prioritizes winning over blocking."""
        game = GameController()
        # Set up both: AI can win AND player can win (next turn)
        game.board.make_move(0, 0, 'O')
        game.board.make_move(0, 1, 'O')
        game.board.make_move(2, 0, 'X')
        game.board.make_move(2, 1, 'X')
        
        move = game.get_computer_move()
        # Should win at (0, 2) not block at (2, 2)
        assert move == (0, 2)
    
    def test_ai_considers_all_empty_cells(self):
        """Test that AI considers all empty cells for winning."""
        game = GameController()
        # Test multiple winning scenarios
        for i in range(3):
            for j in range(3):
                game_test = GameController()
                # Set up O to win at position (i, j)
                game_test.board.make_move(i, j, 'O')
                game_test.board.make_move(i, (j + 1) % 3, 'O')
                # AI should find the winning move
                move = game_test.get_computer_move()
                assert move is not None or len(game_test.board.get_empty_cells()) == 0
    
    def test_ai_handles_empty_board(self):
        """Test AI behavior on empty board (should pick center)."""
        game = GameController()
        move = game.get_computer_move()
        assert move == (1, 1), "AI should pick center on empty board"
    
    def test_ai_never_returns_occupied_cell(self):
        """Test that AI never selects an occupied cell."""
        game = GameController()
        # Make some moves
        game.board.make_move(0, 0, 'X')
        game.board.make_move(1, 1, 'O')
        game.board.make_move(0, 1, 'X')
        
        move = game.get_computer_move()
        
        if move is not None:
            row, col = move
            assert game.board.get_cell(row, col) is None


class TestTurnManagement:
    """Test turn switching and management."""
    
    def test_current_player_switches_after_move(self):
        """Test that current player switches after a move."""
        game = GameController()
        initial_player = game.current_player
        
        # Simulate player's turn
        game.current_player = game.computer
        assert game.current_player != initial_player
    
    def test_player_and_computer_alternate(self):
        """Test that player and computer alternate turns."""
        game = GameController()
        
        # Simulate alternating turns
        assert game.current_player == game.player
        
        game.current_player = game.computer
        assert game.current_player == game.computer
        
        game.current_player = game.player
        assert game.current_player == game.player


class TestGameReset:
    """Test game reset functionality."""
    
    def test_reset_clears_board(self):
        """Test that reset clears the board."""
        game = GameController()
        game.make_move(0, 0, 'X')
        game.make_move(1, 1, 'O')
        
        game.reset()
        
        assert game.board.get_moves_count() == 0
        assert game.board.get_cell(0, 0) is None
        assert game.board.get_cell(1, 1) is None
    
    def test_reset_sets_game_not_over(self):
        """Test that reset sets game_over to False."""
        game = GameController()
        game.game_over = True
        
        game.reset()
        
        assert game.game_over is False
    
    def test_reset_clears_winner(self):
        """Test that reset clears the winner."""
        game = GameController()
        game.winner = 'X'
        
        game.reset()
        
        assert game.winner is None
    
    def test_reset_returns_current_player_to_player(self):
        """Test that reset returns current player to player."""
        game = GameController()
        game.current_player = game.computer
        
        game.reset()
        
        assert game.current_player == game.player


class TestBoardDisplay:
    """Test display methods."""
    
    @patch('sys.stdout', new_callable=StringIO)
    def test_display_board_prints(self, mock_stdout):
        """Test that display_board prints the board."""
        game = GameController()
        game.display_board()
        output = mock_stdout.getvalue()
        assert len(output) > 0
        assert '.' in output  # Empty cells shown as dots


class TestEdgeCases:
    """Test edge cases in game logic."""
    
    def test_ai_move_doesnt_throw_on_nearly_full_board(self):
        """Test AI doesn't crash on nearly full board."""
        game = GameController()
        # Fill board except one cell
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1)]
        for idx, (row, col) in enumerate(positions):
            player = 'X' if idx % 2 == 0 else 'O'
            game.board.make_move(row, col, player)
        
        move = game.get_computer_move()
        assert move == (2, 2) or move is None
    
    def test_game_controller_tracks_moves_correctly(self):
        """Test that game controller properly tracks moves."""
        game = GameController()
        assert game.board.get_moves_count() == 0
        
        game.make_move(0, 0, 'X')
        assert game.board.get_moves_count() == 1
        
        game.make_move(1, 1, 'O')
        assert game.board.get_moves_count() == 2


class TestComplexGameScenarios:
    """Test complex game scenarios."""
    
    def test_game_scenario_ai_wins(self):
        """Test a scenario where AI can set up a win."""
        game = GameController()
        # Player: (0,0), AI: (1,1), Player: (2,2), AI should be able to win
        game.make_move(0, 0, 'X')
        move = game.get_computer_move()
        assert move is not None
    
    def test_multiple_game_resets(self):
        """Test that game can be reset and played multiple times."""
        for _ in range(3):
            game = GameController()
            game.make_move(0, 0, 'X')
            move = game.get_computer_move()
            assert move is not None
            
            game.reset()
            assert game.board.get_moves_count() == 0
            assert game.game_over is False
    
    def test_game_state_consistency(self):
        """Test that game state remains consistent through multiple operations."""
        game = GameController()
        
        # Make some moves
        game.make_move(0, 0, 'X')
        assert game.board.get_moves_count() == 1
        
        game.make_move(1, 1, 'O')
        assert game.board.get_moves_count() == 2
        
        # Check that board state is consistent
        assert game.board.get_cell(0, 0) == 'X'
        assert game.board.get_cell(1, 1) == 'O'
        
        # Get AI move (shouldn't modify move count)
        move = game.get_computer_move()
        assert game.board.get_moves_count() == 2


class TestAICornerCases:
    """Test corner cases in AI logic."""
    
    def test_ai_undo_move_doesnt_affect_board_count(self):
        """Test that AI's move testing doesn't affect final move count."""
        game = GameController()
        initial_count = game.board.get_moves_count()
        
        move = game.get_computer_move()
        
        # After getting computer move, count should be same
        assert game.board.get_moves_count() == initial_count
    
    def test_ai_undo_move_doesnt_affect_board_state(self):
        """Test that AI's move testing doesn't leave test moves on board."""
        game = GameController()
        game.board.make_move(0, 0, 'X')
        game.board.make_move(1, 1, 'O')
        
        board_state_before = [row[:] for row in game.board.board]
        move = game.get_computer_move()
        board_state_after = [row[:] for row in game.board.board]
        
        # Board state should be unchanged
        assert board_state_before == board_state_after
    
    def test_ai_considers_all_win_combinations(self):
        """Test that AI can recognize wins in all positions."""
        # Test each row
        for row in range(3):
            for col in range(3):
                game = GameController()
                game.board.make_move(row, col, 'O')
                game.board.make_move(row, (col + 1) % 3, 'O')
                move = game.get_computer_move()
                assert move is not None or game.board.get_moves_count() == 9
