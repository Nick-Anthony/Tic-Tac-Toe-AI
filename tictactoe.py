# Nick Anthony Tic Tac Toe AI
game_board = []
playerTurn = True
playerChar = ''
aiChar = ''
chars = ['O', 'X']
valid_moves = []
ai_moves = [['0', '1', '2'], ['3', '4', '5'], ['6', '7', '8']]


# prints the current gameboard
def print_board(board):
    print(board[0][0] + ' | ' + board[0][1] + ' | ' + board[0][2])  # prints first row
    print('---------')
    print(board[1][0] + ' | ' + board[1][1] + ' | ' + board[1][2])  # prints second row
    print('---------')
    print(board[2][0] + ' | ' + board[2][1] + ' | ' + board[2][2])  # prints third row


# resets important variables and game board, asks human what character they want
def setup(playerTurn, playerChar, aiChar, chars, board, valid_moves):
    valid_moves = ['0', '1', '2', '3', '4', '5', '6', '7', '8']  # array of the valid moves human can make
    board = [[" "] * 3 for i in range(3)]  # creates 3x3 array with blank spaces

    playerTurn = input("Enter 0 to play as O's or 1 to play as X's: ")
    while playerTurn not in ['0', '1']:  # error trapping
        print("Invalid Input try again")
        playerTurn = input("Enter 0 to play as O's or 1 to play as X's: ")
    playerTurn = int(playerTurn)
    playerChar = chars[playerTurn]  # sets playerCharacter
    if playerTurn == 1:  # sets Ai character
        aiChar = chars[0]
    else:
        aiChar = chars[1]
    return (board, playerTurn, playerChar, aiChar, valid_moves)


# checks if a player has won
def check_win(board, current_char):
    if all(j != " " for i in game_board for j in i):  # checks if there is no more empty spots
        return 0  # return 0 for tie
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == current_char:  # check for horizontal win
            return 1  # return 1 for a win
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == current_char:  # check for vertical win
            return 1
    if board[0][0] == board[1][1] == board[2][2] == current_char:  # diagonal win up-down
        return 1
    if board[2][0] == board[1][1] == board[0][2] == current_char:  # diagonal win down-up
        return 1
    return -1  # returns -1 when no tie or win


# gets user move input
def user_input(valid_moves):
    print()
    print()  # prints two blank lines for formatting
    print('0' + ' | ' + '1' + ' | ' + '2')  # prints what keys the player can press
    print('---------')
    print('3' + ' | ' + '4' + ' | ' + '5')
    print('---------')
    print('6' + ' | ' + '7' + ' | ' + '8')
    move = input("Enter the number where you want to place your piece to place your piece there: ")
    while move not in valid_moves:  # checks if input is a proper move(free space) and a valid number
        print("invalid move")
        move = input("Enter the number where you want to place your piece to place your piece there: ")
    valid_moves.remove(move)
    return int(move), valid_moves


# evaluates a current game_board for the min_max function weighting AI wins more valuable than AI losses
def evaluate(board):
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] == aiChar:  # check for horizontal win
            return 10  # return 10 for an AI win
        if board[i][0] == board[i][1] == board[i][2] == playerChar:
            return -10  # return -10 for a player win
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == aiChar:  # check for vertical win
            return 10
        if board[0][j] == board[1][j] == board[2][j] == playerChar:  # check for vertical win
            return -10
    if board[0][0] == board[1][1] == board[2][2] == aiChar:  # diagonal win up-down
        return 10
    if board[0][0] == board[1][1] == board[2][2] == playerChar:  # diagonal win up-down
        return -10
    if board[2][0] == board[1][1] == board[0][2] == aiChar:  # diagonal win down-up
        return 10
    if board[2][0] == board[1][1] == board[0][2] == playerChar:  # diagonal win down-up
        return -10
    return 0  # returns 0 when neither wins


# uses the min max algorithm to calculate all possible game board from current state returns the score for the given
# position
def min_max(board, isMax):
    score = evaluate(board)  # evaluates current board position

    # if Ai has won return 10
    if score == 10:
        return score
    # if player won return -10
    if score == -10:
        return score
    # if it is a tie return 0
    if all(j != " " for i in game_board for j in i):  # checks if there is no more empty spots
        return 0
    # if it is maximizer's turn
    if isMax:
        best = -1000
        # check all moves
        for i in range(3):
            for j in range(3):
                # check if spot is empty
                if board[i][j] == ' ':
                    # make temporary move
                    board[i][j] = aiChar
                    # recursive call minMax function find the max value of this move
                    best = max(best, min_max(board, not isMax))
                    # undos the temporary move
                    board[i][j] = ' '
        return best
    else:
        # minimizing
        best = 1000
        # check all moves
        for i in range(3):
            for j in range(3):
                # check if spot is empty
                if board[i][j] == ' ':
                    # make temp move
                    board[i][j] = playerChar
                    # recursive call minMax function find the max value of this move
                    best = min(best, min_max(board, not isMax))
                    # undos the temporary move
                    board[i][j] = ' '
        return best


# loops through all possible moves in current game board and calls min_max function on all those position to find best
# move for AI, returns that move to game function
def make_best_move(board):
    bestVal = -1000
    bestMove = (-1, -1)
    # loop through all spots evaluate min max at each empty spot
    for i in range(3):
        for j in range(3):
            # check spot is empty
            if board[i][j] == ' ':
                # make temp move
                board[i][j] = aiChar
                # compute min max for this move
                tempVal = min_max(board, False)
                # undo temp move
                board[i][j] = ' '
                # check if current move minmax value is the best move so far
                # if it is the best move updates bestVal with minmax val and bestMove with i,j
                if tempVal > bestVal:
                    bestMove = (i, j)
                    bestVal = tempVal
    return bestMove


# plays the game switching turns between AI and human calls necessary functions
def game(board, playerChar, aiChar, playerTurn, valid_moves):
    num_moves = 0  # counts number of moves performed
    noWinOrTie = True  # while loop variables keeps looping until someone has won or tied
    while noWinOrTie:
        if playerTurn:
            print_board(board)
            move, valid_moves = user_input(valid_moves)  # gets move and new list of valid moves
            board[move // 3][move % 3] = playerChar  # move // 3 gets row move % 3 gets column
            if num_moves >= 5:  # checks if num_moves >= 5 b/c there will be no win or tie until 5th move or above
                win = check_win(board, playerChar)
                if win == 0:
                    print("you have tied")
                    noWinOrTie = False  # sets loop variable to false
                if win == 1:
                    print("you have won")
                    noWinOrTie = False  # sets loop variable to false
            num_moves += 1
            playerTurn = not playerTurn  # changes which turn it is
        else:
            if num_moves == 0:
                move = (0, 0)  # best opening move stops Ai from having to simulate entire game to make the first move
                valid_moves.remove(ai_moves[move[0]][move[1]])
                board[move[0]][move[1]] = aiChar
                num_moves += 1
                playerTurn = not playerTurn  # changes which turn it is
            else:
                move = make_best_move(board)
                valid_moves.remove(ai_moves[move[0]][move[1]])
                board[move[0]][move[1]] = aiChar
                if num_moves >= 5:
                    win = check_win(board, aiChar)
                    if win == 0:
                        print("you have tied")
                        noWinOrTie = False  # sets loop variable to false
                        print_board(board)
                    if win == 1:
                        print("you have lost")
                        noWinOrTie = False  # sets loop variable to false
                        print_board(board)
                num_moves += 1
                playerTurn = not playerTurn  # changes which turn it is


keepGoing = True  # main loop variable so game can be played multiple times
while keepGoing:
    game_board, playerTurn, playerChar, aiChar, valid_moves = setup(playerTurn, playerChar, aiChar, chars, game_board,
                                                                    valid_moves)
    # calls set_up to reset all important variables and game_board
    game(game_board, playerChar, aiChar, playerTurn, valid_moves)  # calls main game function to play game
    keyPressed = input("press r if you want to restart or e to exit: ")
    while keyPressed not in ['r', 'e']:  # error trapping
        print("input error")
        keyPressed = input("press r if you want to restart or e to exit: ")
    if keyPressed == 'e':  # if player wanted to exit the game loop variable is false
        keepGoing = False
