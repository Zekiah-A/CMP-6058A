"""
Hinger Project
Coursework 001 for: CMP-7058A Artificial Intelligence

Includes a State class for Task 1

@author: A9 (1234, 3456, 5678, and 89123)
@date:   21/10/2026

"""
from a1_state import State

def play(state, agentA, agentB):
    """
    3.1 - 3.3) Runs a full game of Hinger between agentA and agentB.
    If an agent is None, it asks a human player to type a move.
    """
    # Set up player names
    if agentA is None:
        nameA = "Human A"
    else:
        nameA = agentA.name

    if agentB is None:
        nameB = "Human B"
    else:
        nameB = agentB.name

    # Both players start with 100 points
    scoreA = 100
    scoreB = 100
    turn = "A"
    valid_letters = "ABCDEFGHIJKLMNOPQRSTUVWXY"

    print("=== Game Start ===")
    print(state)

    # Loop until all counters are gone (or someone plays Z / an illegal move)
    while True:
        # 1. Check if there is at least 1 counter left on the board
        counters_left = False
        for r in range(5):
            for c in range(5):
                if state.grid[r][c] > 0:
                    counters_left = True

        # If no counters are left, stop the game loop
        if counters_left == False:
            break

        print("\n--------------------")
        print(nameA + " Score:", scoreA, "|", nameB + " Score:", scoreB)

        # 2. Get move from Player A or Player B
        if turn == "A":
            print("It is", nameA + "'s turn.")
            if agentA is None:
                move = input("Enter a letter (A-Y) or Z to end game: ")
            else:
                move = agentA.next_move(state)
                print(nameA, "picked:", move)
        else:
            print("It is", nameB + "'s turn.")
            if agentB is None:
                move = input("Enter a letter (A-Y) or Z to end game: ")
            else:
                move = agentB.next_move(state)
                print(nameB, "picked:", move)

        # Clean up input (in case user typed lowercase or spaces)
        if type(move) == str:
            move = move.strip().upper()
        else:
            move = ""

        # 3. Check if player played 'Z' (ends game immediately and loses)
        if move == "Z":
            print(move, "was played! Game ends immediately.")
            if turn == "A":
                print("Winner:", nameB)
                return nameB, scoreB
            else:
                print("Winner:", nameA)
                return nameA, scoreA

        # 4. Check if move is a valid letter from A to Y
        if len(move) != 1 or move not in valid_letters:
            print("Illegal move! Invalid letter.")
            if turn == "A":
                print("Winner:", nameB)
                return nameB, scoreB
            else:
                print("Winner:", nameA)
                return nameA, scoreA

        # Find row and column of the chosen letter
        position = valid_letters.index(move)
        row = position // 5
        col = position % 5

        # 5. Calculate move cost BEFORE making the move (count active neighbours)
        cost = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                next_r = row + dr
                next_c = col + dc
                if 0 <= next_r < 5 and 0 <= next_c < 5:
                    if state.grid[next_r][next_c] > 0:
                        cost = cost + 1

        # 6. Check hinger bonus BEFORE making the move (+100 if cell has 1 counter and splits regions)
        bonus = 0
        if state.grid[row][col] == 1:
            regions_before = state.numRegions()
            state.grid[row][col] = 0
            regions_after = state.numRegions()
            state.grid[row][col] = 1  # Put counter back so state.move() works normally
            if regions_after > regions_before:
                bonus = 100

        # 7. Try to make the move on the board (returns False if cell is empty)
        success = state.move(move)
        if success == False:
            print("Illegal move! That cell is already empty.")
            if turn == "A":
                print("Winner:", nameB)
                return nameB, scoreB
            else:
                print("Winner:", nameA)
                return nameA, scoreA

        # 8. Update the current player's score and switch turns
        if turn == "A":
            scoreA = scoreA + bonus - cost
            turn = "B"
        else:
            scoreB = scoreB + bonus - cost
            turn = "A"

        print("Cost:", cost, "| Bonus:", bonus)
        print(state)

    # All counters are gone - check who has the higher score
    print("\n=== Game Over ===")
    print("Final ->", nameA + ":", scoreA, "|", nameB + ":", scoreB)

    if scoreA > scoreB:
        print("Winner:", nameA)
        return nameA, scoreA
    elif scoreB > scoreA:
        print("Winner:", nameB)
        return nameB, scoreB
    else:
        print("It is a draw!")
        return None


def tester():
    pass


if __name__ == "__main__":
    tester()
