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

class State:
    """
    Represents the 5x5 game board and rules for Hinger.
    """

    def __init__(self, grid):
        """
        1.1) Sets up the board using a 2D list (5 rows by 5 columns).
        We copy the grid row by row so changing this board doesn't change the original list.
        """
        self.grid = []
        for row in grid:
            new_row = []
            for cell in row:
                new_row.append(cell)
            self.grid.append(new_row)

    def __str__(self):
        """
        1.2) Builds a clean text version of the board to print out.
        """
        output = ""
        for r in range(5):
            row_text = ""
            for c in range(5):
                row_text = row_text + str(self.grid[r][c])
                if c < 4:
                    row_text = row_text + " "
            output = output + row_text
            if r < 4:
                output = output + "\n"
        return output

    def move(self, letter):
        """
        1.3) Takes a letter from 'A' to 'Y', finds the matching cell,
        and removes 1 counter if the cell has counters in it.
        """
        # Make sure the input is a single letter
        if type(letter) != str or len(letter) != 1:
            return False

        letter = letter.upper()
        valid_letters = "ABCDEFGHIJKLMNOPQRSTUVWXY"

        # Check if the letter is between A and Y (Z is not a board cell)
        if letter not in valid_letters:
            return False

        # Find the position (0 to 24) and convert it to row and column
        position = valid_letters.index(letter)
        row = position // 5
        col = position % 5

        # Check if there is at least 1 counter to remove
        if self.grid[row][col] > 0:
            self.grid[row][col] = self.grid[row][col] - 1
            return True
        else:
            return False

    def successors(self):
        """
        1.4) Yields every possible next board state that can be reached
        by removing 1 counter from any active cell.
        """
        for r in range(5):
            for c in range(5):
                # If this cell has counters, create a new board with 1 counter removed
                if self.grid[r][c] > 0:
                    new_state = State(self.grid)
                    new_state.grid[r][c] = new_state.grid[r][c] - 1
                    yield new_state

    def numRegions(self):
        """
        1.5) Counts how many separate groups (regions) of active cells are on the board.
        """
        # Keep track of which cells we have already checked
        visited = []
        for r in range(5):
            visited.append([False, False, False, False, False])

        region_count = 0

        for r in range(5):
            for c in range(5):
                # If we find an active cell we haven't visited yet, it's a new region
                if self.grid[r][c] > 0 and visited[r][c] == False:
                    region_count = region_count + 1

                    # Use a simple list to explore all connected active neighbours
                    to_check = [(r, c)]
                    visited[r][c] = True

                    while len(to_check) > 0:
                        curr_r, curr_c = to_check.pop(0)

                        # Look at all 8 surrounding cells
                        for dr in [-1, 0, 1]:
                            for dc in [-1, 0, 1]:
                                next_r = curr_r + dr
                                next_c = curr_c + dc

                                # Make sure the neighbour is inside the 5x5 board
                                if 0 <= next_r < 5 and 0 <= next_c < 5:
                                    if self.grid[next_r][next_c] > 0 and visited[next_r][next_c] == False:
                                        visited[next_r][next_c] = True
                                        to_check.append((next_r, next_c))

        return region_count

    def numHingers(self):
        """
        1.6) Counts how many cells are 'hingers'.
        A hinger has 1 counter, and removing it splits the board into more regions.
        """
        starting_regions = self.numRegions()
        hinger_count = 0

        for r in range(5):
            for c in range(5):
                # A hinger must have exactly 1 counter
                if self.grid[r][c] == 1:
                    # Temporarily empty the cell to see if regions increase
                    self.grid[r][c] = 0
                    new_regions = self.numRegions()

                    if new_regions > starting_regions:
                        hinger_count = hinger_count + 1

                    # Put the counter back so the board stays the same
                    self.grid[r][c] = 1

        return hinger_count


def tester():
    """
    1.8) Tests the State class using Figure 1.1 from the assignment brief.
    """
    # 1.8a) Create State representing State s1 and print it
    print("--- State s1 ---")
    s1_grid = [
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1],
        [0, 0, 0, 1, 1],
        [0, 0, 0, 0, 1]
    ]
    sa = State(s1_grid)
    print(sa)

    # 1.8b) Additional tests
    print("\n--- Testing Regions and Hingers ---")
    print("Regions in s1 (should be 2):", sa.numRegions())
    print("Hingers in s1 (should be 0):", sa.numHingers())

    # Move 'Y' removes counter at bottom-right (4, 4) -> creates State s2
    print("\nMaking move 'Y':", sa.move('Y'))
    print(sa)
    print("Regions in s2 (should be 2):", sa.numRegions())
    print("Hingers in s2 (should be 1):", sa.numHingers())

    # Move 'M' removes hinger at middle (2, 2) -> creates State s3
    print("\nMaking move 'M':", sa.move('M'))
    print(sa)
    print("Regions in s3 (should be 3):", sa.numRegions())
    print("Hingers in s3 (should be 0):", sa.numHingers())

    # Test invalid moves
    print("\n--- Testing Invalid Moves ---")
    print("Move 'C' on empty cell (should be False):", sa.move('C'))
    print("Move 'Z' end game letter (should be False):", sa.move('Z'))

    # Test successors
    print("\n--- Testing Successors ---")
    next_boards = list(sa.successors())
    print("Possible next moves from s3 (should be 9):", len(next_boards))


if __name__ == "__main__":
    tester()
