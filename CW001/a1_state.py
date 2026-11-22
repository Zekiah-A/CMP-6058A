"""
Group Number: [INSERT GROUP NUMBER]
File: a1_state.py
Description: Defines the State class representing the 5x5 Hinger game board,
             along with move validation, successor generation, and graph-based
             region/hinger detection.
"""

"""
Hinger Project
Coursework 001 for: CMP-6058A Artificial Intelligence

Includes a State class for Task 1

@author: A9 (1234, 3456, 5678, and 89123)
@date:   21/10/2026

"""
import copy
from collections import deque


class State:
    """
    Encapsulates the structure and behaviour of a game state in Hinger.
    """

    def __init__(self, grid):
        """
        1.1) Initialises the State with a 2D list grid representing the
        number of counters in each cell of the 5x5 board.
        """
        # Deep copy prevents external list mutations from altering this state
        self.grid = copy.deepcopy(grid)

    def __str__(self):
        """
        1.2) Returns a readable string representation of the board without borders,
        matching the matrix layout in Figure 1.1.
        """
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def move(self, letter):
        """
        1.3) Receives a letter ('A'-'Y') representing a move and removes one counter
        from the corresponding cell, provided the move is legitimate.
        Returns True if successful, False if the move is invalid or cell is empty.
        """
        # Validate that input is a single uppercase/lowercase character between 'A' and 'Y'
        if not isinstance(letter, str) or len(letter) != 1:
            return False

        letter = letter.upper()
        if not ('A' <= letter <= 'Y'):
            return False

        # Convert letter 'A'-'Y' (0-24) into (row, col) coordinates on a 5x5 grid
        index = ord(letter) - ord('A')
        r, c = divmod(index, 5)

        # Check if the cell is active (contains at least 1 counter)
        if self.grid[r][c] <= 0:
            return False

        # Perform the legitimate move by removing one counter
        self.grid[r][c] -= 1
        return True

    def successors(self):
        """
        1.4) Generator method that yields all possible State objects reachable
        in one move (removing one counter from any active cell).
        """
        rows = len(self.grid)
        cols = len(self.grid) if rows > 0 else 0

        for r in range(rows):
            for c in range(cols):
                if self.grid[r][c] > 0:
                    # Create an independent copy of the current state for each valid move
                    next_state = State(self.grid)
                    next_state.grid[r][c] -= 1
                    yield next_state

    def numRegions(self):
        pass

    def numHingers(self):
        pass


def tester():
    pass  # Placeholder for testing the State class functionality


if __name__ == "__main__":
    tester()