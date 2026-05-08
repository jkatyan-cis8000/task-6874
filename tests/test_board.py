"""
Comprehensive unit tests for the Board class.

Tests cover:
- Board initialization
- Move validation (valid/invalid positions, occupied cells, out of bounds)
- Making moves and tracking state
- Cell access
- Empty cells retrieval
- Winner detection (rows, columns, diagonals)
- Draw detection
- Game over status
- Board reset functionality
- Move counting
- String representation
"""

import pytest
import sys
import os

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from board import Board


class TestBoardInitialization:
    """Test board initialization and initial state."""
    
    def test_board_creates_empty_3x3_grid(self):
        """Test that board initializes as a 3x3 grid with all None values."""
        board = Board()
        assert len(board.board) == 3
        assert all(len(row) == 3 for row in board.board)
        assert all(cell is None for row in board.board for cell in row)
    
    def test_board_starts_with_zero_moves(self):
        """Test that move counter starts at zero."""
        board = Board()
        assert board.get_moves_count() == 0
    
    def test_board_is_empty_initially(self):
        """Test that board starts with all 9 cells empty."""
        board = Board()
        empty_cells = board.get_empty_cells()
        assert len(empty_cells) == 9
        assert set(empty_cells) == {(i, j) for i in range(3) for j in range(3)}


class TestMoveValidation:
    """Test move validation logic."""
    
    def test_valid_move_on_empty_cell(self):
        """Test that moves on empty cells are valid."""
        board = Board()
        assert board.is_valid_move(0, 0) is True
        assert board.is_valid_move(1, 1) is True
        assert board.is_valid_move(2, 2) is True
    
    def test_invalid_move_out_of_bounds_negative(self):
        """Test that negative row/col indices are invalid."""
        board = Board()
        assert board.is_valid_move(-1, 0) is False
        assert board.is_valid_move(0, -1) is False
        assert board.is_valid_move(-1, -1) is False
    
    def test_invalid_move_out_of_bounds_positive(self):
        """Test that indices >= 3 are invalid."""
        board = Board()
        assert board.is_valid_move(3, 0) is False
        assert board.is_valid_move(0, 3) is False
        assert board.is_valid_move(3, 3) is False
    
    def test_invalid_move_on_occupied_cell(self):
        """Test that moves on occupied cells are invalid."""
        board = Board()
        board.make_move(1, 1, 'X')
        assert board.is_valid_move(1, 1) is False
    
    def test_all_boundary_valid_positions(self):
        """Test that all valid boundary positions are accepted."""
        board = Board()
        valid_positions = [(0, 0), (0, 2), (2, 0), (2, 2), (1, 1)]
        for row, col in valid_positions:
            assert board.is_valid_move(row, col) is True


class TestMakingMoves:
    """Test making moves on the board."""
    
    def test_make_valid_move_returns_true(self):
        """Test that valid moves return True."""
        board = Board()
        result = board.make_move(0, 0, 'X')
        assert result is True
    
    def test_make_invalid_move_returns_false(self):
        """Test that invalid moves return False."""
        board = Board()
        board.make_move(0, 0, 'X')
        result = board.make_move(0, 0, 'O')  # Cell already occupied
        assert result is False
    
    def test_make_move_out_of_bounds_returns_false(self):
        """Test that out-of-bounds moves return False."""
        board = Board()
        assert board.make_move(3, 3, 'X') is False
        assert board.make_move(-1, 0, 'X') is False
    
    def test_make_move_places_mark_correctly(self):
        """Test that moves place the correct mark on the board."""
        board = Board()
        board.make_move(0, 0, 'X')
        assert board.get_cell(0, 0) == 'X'
        
        board.make_move(1, 1, 'O')
        assert board.get_cell(1, 1) == 'O'
    
    def test_make_move_increments_counter(self):
        """Test that move counter increments with each move."""
        board = Board()
        assert board.get_moves_count() == 0
        
        board.make_move(0, 0, 'X')
        assert board.get_moves_count() == 1
        
        board.make_move(1, 1, 'O')
        assert board.get_moves_count() == 2
    
    def test_invalid_player_raises_value_error(self):
        """Test that invalid player markers raise ValueError."""
        board = Board()
        with pytest.raises(ValueError):
            board.make_move(0, 0, 'Z')
        
        with pytest.raises(ValueError):
            board.make_move(0, 0, 'x')  # Lowercase
        
        with pytest.raises(ValueError):
            board.make_move(0, 0, '')
    
    def test_alternating_moves_x_and_o(self):
        """Test alternating X and O moves."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'O')
        board.make_move(0, 2, 'X')
        
        assert board.get_cell(0, 0) == 'X'
        assert board.get_cell(0, 1) == 'O'
        assert board.get_cell(0, 2) == 'X'


class TestCellAccess:
    """Test getting cell values."""
    
    def test_get_empty_cell_returns_none(self):
        """Test that empty cells return None."""
        board = Board()
        assert board.get_cell(0, 0) is None
    
    def test_get_cell_after_move(self):
        """Test getting cell value after move."""
        board = Board()
        board.make_move(1, 2, 'X')
        assert board.get_cell(1, 2) == 'X'
    
    def test_get_cell_out_of_bounds_raises_error(self):
        """Test that out-of-bounds cell access raises IndexError."""
        board = Board()
        with pytest.raises(IndexError):
            board.get_cell(3, 0)
        
        with pytest.raises(IndexError):
            board.get_cell(0, 3)


class TestEmptyCells:
    """Test getting empty cells."""
    
    def test_get_empty_cells_on_fresh_board(self):
        """Test that fresh board returns all 9 empty cells."""
        board = Board()
        empty = board.get_empty_cells()
        assert len(empty) == 9
        assert set(empty) == {(i, j) for i in range(3) for j in range(3)}
    
    def test_get_empty_cells_after_moves(self):
        """Test that empty cells list updates after moves."""
        board = Board()
        board.make_move(0, 0, 'X')
        empty = board.get_empty_cells()
        assert len(empty) == 8
        assert (0, 0) not in empty
    
    def test_get_empty_cells_full_board(self):
        """Test that full board returns no empty cells."""
        board = Board()
        # Fill entire board
        for i in range(3):
            for j in range(3):
                board.make_move(i, j, 'X' if (i + j) % 2 == 0 else 'O')
        
        empty = board.get_empty_cells()
        assert len(empty) == 0


class TestWinnerDetection:
    """Test winner detection for all winning conditions."""
    
    def test_no_winner_on_empty_board(self):
        """Test that empty board has no winner."""
        board = Board()
        assert board.check_winner() is None
    
    def test_winner_first_row(self):
        """Test detection of three X's in first row."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'X')
        board.make_move(0, 2, 'X')
        assert board.check_winner() == 'X'
    
    def test_winner_second_row(self):
        """Test detection of three O's in second row."""
        board = Board()
        board.make_move(1, 0, 'O')
        board.make_move(1, 1, 'O')
        board.make_move(1, 2, 'O')
        assert board.check_winner() == 'O'
    
    def test_winner_third_row(self):
        """Test detection of three X's in third row."""
        board = Board()
        board.make_move(2, 0, 'X')
        board.make_move(2, 1, 'X')
        board.make_move(2, 2, 'X')
        assert board.check_winner() == 'X'
    
    def test_winner_first_column(self):
        """Test detection of three O's in first column."""
        board = Board()
        board.make_move(0, 0, 'O')
        board.make_move(1, 0, 'O')
        board.make_move(2, 0, 'O')
        assert board.check_winner() == 'O'
    
    def test_winner_second_column(self):
        """Test detection of three X's in second column."""
        board = Board()
        board.make_move(0, 1, 'X')
        board.make_move(1, 1, 'X')
        board.make_move(2, 1, 'X')
        assert board.check_winner() == 'X'
    
    def test_winner_third_column(self):
        """Test detection of three O's in third column."""
        board = Board()
        board.make_move(0, 2, 'O')
        board.make_move(1, 2, 'O')
        board.make_move(2, 2, 'O')
        assert board.check_winner() == 'O'
    
    def test_winner_diagonal_top_left_to_bottom_right(self):
        """Test detection of diagonal win (0,0 -> 2,2)."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'X')
        board.make_move(2, 2, 'X')
        assert board.check_winner() == 'X'
    
    def test_winner_diagonal_top_right_to_bottom_left(self):
        """Test detection of diagonal win (0,2 -> 2,0)."""
        board = Board()
        board.make_move(0, 2, 'O')
        board.make_move(1, 1, 'O')
        board.make_move(2, 0, 'O')
        assert board.check_winner() == 'O'
    
    def test_no_winner_incomplete_row(self):
        """Test no winner with incomplete row."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'X')
        assert board.check_winner() is None
    
    def test_no_winner_mixed_marks(self):
        """Test no winner with mixed marks in row."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'O')
        board.make_move(0, 2, 'X')
        assert board.check_winner() is None
    
    def test_winner_returns_correct_player(self):
        """Test that check_winner returns the correct player."""
        board = Board()
        # Set up X to win
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'X')
        board.make_move(0, 2, 'X')
        winner = board.check_winner()
        assert winner == 'X'
        assert winner != 'O'


class TestDrawDetection:
    """Test draw detection."""
    
    def test_draw_full_board_no_winner(self):
        """Test draw detection on a full board with no winner."""
        board = Board()
        # Create a draw game:
        # X | O | X
        # X | O | O
        # O | X | X
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        for row, col, player in moves:
            board.make_move(row, col, player)
        
        assert board.is_draw() is True
        assert board.is_full() is True
        assert board.check_winner() is None
    
    def test_not_draw_board_not_full(self):
        """Test that incomplete board is not a draw."""
        board = Board()
        board.make_move(0, 0, 'X')
        assert board.is_draw() is False
    
    def test_not_draw_board_with_winner(self):
        """Test that board with winner is not a draw."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'X')
        board.make_move(0, 2, 'X')
        board.make_move(1, 0, 'O')
        board.make_move(1, 1, 'O')
        
        assert board.is_draw() is False
        assert board.check_winner() == 'X'


class TestGameOverStatus:
    """Test game over detection."""
    
    def test_game_not_over_empty_board(self):
        """Test that empty board is not game over."""
        board = Board()
        assert board.is_game_over() is False
    
    def test_game_over_with_winner(self):
        """Test that game is over when there's a winner."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(0, 1, 'X')
        board.make_move(0, 2, 'X')
        assert board.is_game_over() is True
    
    def test_game_over_when_board_full(self):
        """Test that game is over when board is full."""
        board = Board()
        # Fill board to create a draw
        moves = [
            (0, 0, 'X'), (0, 1, 'O'), (0, 2, 'X'),
            (1, 0, 'X'), (1, 1, 'O'), (1, 2, 'O'),
            (2, 0, 'O'), (2, 1, 'X'), (2, 2, 'X')
        ]
        for row, col, player in moves:
            board.make_move(row, col, player)
        
        assert board.is_game_over() is True
    
    def test_game_not_over_partial_board(self):
        """Test that game is not over with partial board and no winner."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'O')
        board.make_move(2, 2, 'X')
        assert board.is_game_over() is False


class TestBoardReset:
    """Test board reset functionality."""
    
    def test_reset_clears_all_moves(self):
        """Test that reset clears all moves from the board."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'O')
        board.make_move(2, 2, 'X')
        
        board.reset()
        
        for i in range(3):
            for j in range(3):
                assert board.get_cell(i, j) is None
    
    def test_reset_resets_move_counter(self):
        """Test that reset resets the move counter to zero."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'O')
        
        assert board.get_moves_count() == 2
        
        board.reset()
        
        assert board.get_moves_count() == 0
    
    def test_reset_allows_new_moves(self):
        """Test that board can be played on after reset."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.reset()
        
        result = board.make_move(0, 0, 'O')
        assert result is True
        assert board.get_cell(0, 0) == 'O'
    
    def test_multiple_resets(self):
        """Test that board can be reset multiple times."""
        board = Board()
        
        for _ in range(3):
            board.make_move(0, 0, 'X')
            board.make_move(1, 1, 'O')
            assert board.get_moves_count() == 2
            
            board.reset()
            assert board.get_moves_count() == 0
            assert board.get_cell(0, 0) is None


class TestBoardStringRepresentation:
    """Test board string representation."""
    
    def test_str_method_returns_string(self):
        """Test that __str__ returns a string."""
        board = Board()
        result = str(board)
        assert isinstance(result, str)
    
    def test_str_shows_board_state(self):
        """Test that string representation shows board state."""
        board = Board()
        board.make_move(0, 0, 'X')
        board.make_move(1, 1, 'O')
        
        result = str(board)
        assert 'X' in result
        assert 'O' in result
    
    def test_str_shows_empty_cells_as_dots(self):
        """Test that empty cells are shown as dots."""
        board = Board()
        result = str(board)
        assert '.' in result
    
    def test_display_method_exists(self):
        """Test that display method exists and doesn't raise errors."""
        board = Board()
        # This should not raise an exception
        try:
            board.display()
        except Exception as e:
            pytest.fail(f"display() raised {type(e).__name__}: {e}")


class TestEdgeCases:
    """Test edge cases and boundary conditions."""
    
    def test_full_board_is_full(self):
        """Test is_full returns True for completely filled board."""
        board = Board()
        for i in range(3):
            for j in range(3):
                board.make_move(i, j, 'X' if (i + j) % 2 == 0 else 'O')
        
        assert board.is_full() is True
    
    def test_board_with_8_moves_not_full(self):
        """Test is_full returns False for 8 moves."""
        board = Board()
        for i in range(3):
            for j in range(3):
                if board.get_moves_count() < 8:
                    board.make_move(i, j, 'X')
        
        assert board.is_full() is False
    
    def test_sequential_moves_different_positions(self):
        """Test making moves in sequence on different positions."""
        board = Board()
        positions = [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1), (2, 2)]
        
        for idx, (row, col) in enumerate(positions):
            player = 'X' if idx % 2 == 0 else 'O'
            result = board.make_move(row, col, player)
            assert result is True
        
        assert board.is_full() is True
