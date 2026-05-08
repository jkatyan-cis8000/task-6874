# Game Logic and Player Interaction Design

## Overview

The `game.py` module implements the core game controller for the tic-tac-toe application. It orchestrates the gameplay between a human player (X) and an AI computer opponent (O), handling turn management, input validation, AI decision-making, and game flow.

## Architecture

### GameController Class

The main controller class that manages:
- **Game State**: Tracks board state, current player, game over status, and winner
- **Turn Management**: Alternates between player and computer turns
- **User Interaction**: Prompts and validates player input
- **AI Strategy**: Implements intelligent move selection for the computer
- **Game Flow**: Runs the game loop and announces outcomes

### Key Components

#### 1. Player Input Handling

**Method**: `get_player_move()`

The player enters a move as a single digit (0-8) representing positions on the 3x3 grid:
```
0 | 1 | 2
---------
3 | 4 | 5
---------
6 | 7 | 8
```

Input validation includes:
- Checking that input is a valid number
- Verifying the position is in range (0-8)
- Ensuring the target cell is empty via the Board's `is_valid_move()` method
- Converting linear position to (row, col) coordinates: `row = position // 3`, `col = position % 3`

**Error Handling**:
- Invalid characters → prompt for retry
- Out-of-range numbers → prompt for retry
- Occupied positions → prompt for retry
- General exceptions → inform user and retry

#### 2. AI Strategy

**Method**: `get_computer_move()`

The computer uses a priority-based decision strategy to select moves:

1. **Win Move** (Highest Priority)
   - Check all empty cells
   - Simulate placing the computer's mark
   - If it results in a win, take that move
   - Undo the simulation and move on

2. **Block Move** (Second Priority)
   - Check all empty cells
   - Simulate placing the player's mark
   - If it would result in a player win, block by placing computer mark there instead
   - Undo the simulation and move on

3. **Center Move** (Third Priority)
   - If position (1,1) is empty, take it
   - Center control is valuable in tic-tac-toe

4. **Corner Moves** (Fourth Priority)
   - Available corners: (0,0), (0,2), (2,0), (2,2)
   - Randomly select from available corners
   - Corners provide multiple winning opportunities

5. **Side Moves** (Fallback Priority)
   - Available sides: (0,1), (1,0), (1,2), (2,1)
   - Randomly select from available sides
   - Sides are the least valuable positions

**Simulation Pattern**:
For win/block detection, we use a test-and-undo pattern:
```python
self.board.make_move(row, col, piece)  # Test the move
if winning_condition:
    # Found a winning move
    self.board.board[row][col] = None  # Undo
    self.board._moves_count -= 1
    return (row, col)  # Return the actual move to make
```

#### 3. Game Loop

**Method**: `run_game()`

The main game loop follows this flow:
1. Display welcome message with instructions
2. While game is not over:
   - Display the current board
   - Execute current player's turn
   - Check if game is over (win or draw)
3. Display final board and announce result

**Turn Execution**:
- **Player Turn**: Get input via `get_player_move()`, make the move, switch to computer
- **Computer Turn**: Get AI move via `get_computer_move()`, make the move, switch to player

#### 4. Game Outcome Detection

**Method**: `check_game_over()`

Checks game state using the Board's built-in methods:
- `board.check_winner()` → Returns 'X', 'O', or None
- `board.is_draw()` → Returns True if board is full and no winner
- Sets `self.game_over = True` when either condition is met

### Main Function

The `main()` function provides the entry point for the application:
- Creates and runs a GameController instance
- Plays one complete game via `run_game()`
- Prompts user to play again with input validation
- Loops until the user declines to play again
- Displays farewell message

## Design Decisions

### Why Simulation for AI?

The test-and-undo pattern allows the AI to evaluate potential moves without permanently modifying the board. This is simpler than creating board copies and still performant given the 3x3 board size.

### Why Random Selection for Lower Priorities?

Using `random.choice()` for corners and sides adds variety and prevents the AI from being predictable. The game remains challenging while still being beatable with optimal play.

### Position Numbering

Using 0-8 linear indexing (rather than row/col pairs) makes the interface more intuitive for users. Conversion to row/col is straightforward: `row = position // 3`, `col = position % 3`.

### Turn Order

The player always goes first (standard in tic-tac-toe). This is hardcoded as it provides a consistent user experience.

### User Experience Features

- Clear visual board display with position numbers
- Descriptive prompts and feedback
- Input validation with helpful error messages
- Game status announcements (win/loss/draw)
- Ability to play multiple games without restarting the program

## Integration with Board Class

The GameController depends on the Board class from `board.py` for:
- Board state management
- Move validation: `is_valid_move(row, col)`
- Move execution: `make_move(row, col, player)`
- State queries: `get_empty_cells()`, `check_winner()`, `is_full()`, `is_draw()`
- Board display: `__str__()` method

The GameController uses the Board class correctly, never violating its invariants or directly manipulating internal state (except during AI simulation where it undoes changes).

## Testing Considerations

Key behaviors to test:
- Player input validation (invalid numbers, out of range, occupied cells)
- AI move selection under each priority condition
- Win detection (rows, columns, diagonals)
- Draw detection (board full, no winner)
- Complete game scenarios (player win, computer win, draw)
- Multiple games in succession (reset works correctly)

## Future Enhancements

Potential improvements for future iterations:
- Difficulty levels (easy, medium, hard) with different AI strategies
- Move history and undo functionality
- Game statistics tracking (wins/losses/draws)
- Configurable player names
- Network multiplayer support
