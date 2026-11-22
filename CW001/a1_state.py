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
        1.1) Initialises the State with a 5x5 2D list representing the board.
        Each element represents the number of counters in that cell.
        """
        # Deep copy ensures external modifications to the input list don't mutate internal state
        self.grid = copy.deepcopy(grid)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0]) if self.rows > 0 else 0

    def __str__(self):
        """
        1.2) Returns a readable string representation of the board without borders,
        matching the matrix style shown in Figure 1.1.
        """
        return "\n".join(" ".join(str(cell) for cell in row) for row in self.grid)

    def _letter_to_coords(self, letter):
        """
        1.7) Utility method: Converts a move letter ('A'-'Y') into (row, col) coordinates.
        Returns None if the letter is invalid or reserved ('Z').
        """
        if not isinstance(letter, str) or len(letter) != 1:
            return None
        
        letter = letter.upper()
        if 'A' <= letter <= 'Y':
            index = ord(letter) - ord('A')
            return divmod(index, 5)  # Returns (row, col) for a 5x5 grid
        return None

    def _coords_to_letter(self, r, c):
        """
        1.7) Utility method: Converts (row, col) coordinates into a move letter ('A'-'Y').
        """
        return chr(ord('A') + (r * 5 + c))

    def _get_adjacent_coords(self, r, c):
        """
        1.7) Utility method: Yields all valid adjacent coordinates (horizontally,
        vertically, or diagonally) where max{|r-r'|, |c-c'|} == 1.
        """
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    yield nr, nc

    