import math
import random

AI = "X"
HUMAN = "O"

template = [["","",""],
            ["","",""],
            ["","",""]]

testGrid = [["X","X","O"],
            ["O","X",""],
            ["O","","O"]]

# Check if AI or Human Won:
def whoWon(grid, row, column):
    if grid[row][column] == AI:
        return 1
    elif grid[row][column] == HUMAN:
        return -1
    
# Check for win
def winCheck(grid):
    # win (1), lose (-1), draw (0), still in progress = None

    # check columns (iterate 3 times)
    # return 1 or -1
    for column in range(0,3):
        if grid[0][column] == grid[1][column] == grid[2][column] != "":
            return whoWon(grid, 0, column)
            
    # check rows (iterate 3 times)
    # return 1 or -1
    for row in range(0,3):
        if grid[row][0] == grid[row][1] == grid[row][2] != "":
            return whoWon(grid, row, 0)
        
    # check diagonals (twice)
    # return 1 or -1
    # left corner:
    if grid[0][0] == grid[1][1] == grid[2][2] != "":
        return whoWon(grid, 1, 1)
    if grid[0][2] == grid[1][1] == grid[2][0] != "":
        return whoWon(grid, 1, 1)

    # draw if all spaces are full
    if "" not in grid[0] and "" not in grid[1] and "" not in grid[2]:
        return 0
    
    return None

# Find best move
def findBestMove(grid):
    # best score = -infinity
    bestScore = -math.inf
    # best spaces = []
    bestMoves = []
    # iterate through empty spaces
    for row in range(len(grid)):
        for column in range(len(grid[row])):
            if grid[row][column] == "":
                grid[row][column] = AI
                # call minimax, if greater than best score, best spaces = [move]. if == best score, bestspaces.append(move)
                result = minimax(grid, False)
                if result > bestScore:
                    bestScore = result
                    bestMoves = [(row,column)]
                elif result == bestScore:
                    bestMoves.append((row,column))
                grid[row][column] = ""
    
    # pick random space from list of possible spaces
    return random.choice(bestMoves)

# Minimax
def minimax(grid, isMaximising): #later add depth
    # ismaximising means it's the ai turn, else simulate the player
    # check for win state, return if there is one
    winState = winCheck(grid)
    if winState != None:
        # do something later when someone wins
        return winState
    # if currently nothing, continue and... 

    # if maximising, 
    if isMaximising:
        bestScore = -math.inf
        # best score = -infinity    
        # iterate through empty squares
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if grid[row][column] == "":
                    grid[row][column] = AI
                    # call minimaxing(ismaximising = false) 
                    result = minimax(grid, False)
                    if result > bestScore:
                        # if higher than best score, update var
                        bestScore = result
                    grid[row][column] = ""
        # when finished, return best score
        return bestScore
    else:
        bestScore = math.inf
        # best score = infinity    
        # iterate through empty squares
        for row in range(len(grid)):
            for column in range(len(grid[row])):
                if grid[row][column] == "":
                    grid[row][column] = HUMAN
                    # call minimaxing(ismaximising = false) 
                    result = minimax(grid, True)
                    if result < bestScore:
                        # if lower than best score, update var
                        bestScore = result
                    grid[row][column] = ""
        # when finished, return best score
        return bestScore

# later add alpha beta pruning

def game():
    grid = template
    playerTurn = True
    print("Naughts and Crosses:")
    print("You are playing naughts (O)")
    while True:
        while playerTurn:
            print()
            for i in range(3):
                print(grid[i])
            userRow = input("Enter row (0, 1, 2): ")
            userColumn = input("Enter column (0, 1 ,2): ")
            # check for int later
            
            if grid[int(userRow)][int(userColumn)] == "":
                grid[int(userRow)][int(userColumn)] = HUMAN
                playerTurn = False
            else:
                print("That space is taken, choose another.")

        winState = winCheck(grid)
        if winState == 1:
            print("You win!")
            return
        elif winState == -1:
            print("You lose...")
            return
        elif winState == 0:
            print("You draw!")
            return

        cpuRow, cpuColumn = findBestMove(grid)
        print("Computer makes a move...")
        grid[cpuRow][cpuColumn] = AI

        winState = winCheck(grid)
        if winState == 1:
            print("You win!")
            return
        elif winState == -1:
            print("You lose...")
            return
        elif winState == 0:
            print("You draw!")
            return
        playerTurn = True



if __name__ == '__main__':
    game()