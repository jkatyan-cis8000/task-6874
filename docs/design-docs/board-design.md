# Board Class Design Document

## Overview

The `Board` class is the foundation of the tic-tac-toe game implementation. It manages the game state, validates moves, and determines game outcomes.

## Architecture

### Data Structure

The board is implemented using a 3x3 nested list (Python list of lists):
```python
board = [
    [None, None, None],
    [None, None, None],
    [None, None, None]
]
```

**Rationale:**
- Simple and efficient for a 3x3 grid
- Direct indexing via `board[row][col]`
- Easy to iterate and check patterns
- Memory efficient for this small fixed size
- Natural alignment with row/column coordinate system (0-2)

### Cell Values

- `None` represents an empty cell
- `'X'` represents a human player mark
- `'O'` represents a computer/opponent player mark

**Rationale:**
- Using string literals ('X', 'O') makes debugging and display easier
- `None` is Pythonic for "no value" state
- Simple equality checks for winner detection

## Core Methods

### Initialization
- `__init__()`: Creates an empty 3x3 board and initializes move counter

### Move Validation & Execution
- `is_valid_move(row, col)`: Checks if a move is legal (in bounds and empty)
- `make_move(row, col, player)`: Places a mark and updates move counter
- `get_cell(row, col)`: Retrieves the current state of a cell

### Game State Queries
- `check_winner()`: Returns 'X', 'O', or None based on winner status
- `is_full()`: Checks if all 9 cells are filled
- `is_draw()`: Determines if game ended in a draw (full + no winner)
- `is_game_over()`: Checks if game has ended (winner or full)
- `get_empty_cells()`: Returns list of available move positions
- `get_moves_count()`: Returns number of moves made

### Board Management
- `reset()`: Clears the board and move counter for a new game
- `display()`: Prints the board to console
- `__str__()`: Returns formatted string representation

## Winner Detection Algorithm

The `check_winner()` method checks for three matching marks in:
1. **Rows**: 3 cells horizontally
2. **Columns**: 3 cells vertically  
3. **Diagonals**: Two diagonals (top-left to bottom-right, top-right to bottom-left)

**Implementation Details:**
- Uses direct triple equality checks: `a == b == c`
- Verifies the cell is not None (not an empty cell)
- Returns immediately upon finding a match
- Time complexity: O(1) - constant checks regardless of board state

## Design Constraints & Decisions

### Coordinate System
- Rows: 0 (top) to 2 (bottom)
- Columns: 0 (left) to 2 (right)
- This matches typical array indexing and is intuitive for CLI input

### Move Counter
- Tracks total moves made (0-9)
- Used for draw detection (full when `_moves_count == 9`)
- More efficient than scanning the board each time

### Validation Separation
- `is_valid_move()` checks only position validity
- `make_move()` wraps validation with game logic
- Allows queries without side effects

### Error Handling
- `make_move()` raises `ValueError` for invalid player values
- Invalid positions return `False` (graceful failure)
- Out-of-bounds access in `get_cell()` raises `IndexError` (standard Python)

## Interface Contract

### Methods Used by Game Logic (task-2)
- `make_move(row, col, player)` - Execute player moves
- `is_valid_move(row, col)` - Pre-validate before move attempt
- `check_winner()` - Determine game outcome
- `is_full()` - Check for draw condition
- `get_empty_cells()` - Find available positions for AI
- `reset()` - Start new game

### Methods for Display/Testing
- `display()` or `__str__()` - Show board state to user
- `get_cell(row, col)` - Read specific cell state
- `get_moves_count()` - Query game progress

## Extensibility

The class is designed for future enhancement:
- Could add undo/redo by storing move history
- Could add move validation callbacks for rule extensions
- Could implement board hashing for AI algorithms
- Column/row validation helpers could be extracted for board analysis

## Testing Considerations

Key test scenarios:
- Move validation (valid, out of bounds, occupied)
- Winner detection (rows, columns, both diagonals)
- Draw detection (full board, no winner)
- Move counting and state consistency
- Reset functionality
- Display formatting

See task-3 for comprehensive test implementation.
