import numpy as np

turn = 0
board = np.zeros((3, 3))
dimens = 3
heights = np.zeros(10)
mv = (0, 0)

def winningStateHelper(token, r, c, dr, dc):
    if(r < 0 or c < 0 or r > dimens - 1 or c > dimens - 1):
        return 0
    if(not int(board[r][c]) == token):
        return 0
    return 1 + winningStateHelper(token, r + dr, c + dc, dr, dc)

def inWinningState():
    win = False
    token = int(board[mv[0]][mv[1]])
    if(token == 0):
        return 0
    if(winningStateHelper(token, mv[0], mv[1], -1, 0) + winningStateHelper(token, mv[0], mv[1], 1, 0) - 1 >= 2):
        win = True
    if(winningStateHelper(token, mv[0], mv[1], 0, 1) + winningStateHelper(token, mv[0], mv[1], 0, -1) - 1 >= 2):
        win = True
    if(winningStateHelper(token, mv[0], mv[1], -1, -1) + winningStateHelper(token, mv[0], mv[1], 1, 1) - 1 >= 2):
        win = True
    if(winningStateHelper(token, mv[0], mv[1], -1, 1) + winningStateHelper(token, mv[0], mv[1], 1, -1) - 1 >= 2):
        win = True

    if(win):
        if(board[mv[0]][mv[1]] == 1):
            return -1
        else:
            return 1
    else:
        return 0
'''
Minimax using alpha-beta pruning
'''
def minimax(alpha, beta, maximizing):
    win = inWinningState()
    if(win != 0):
        return win
    res = -1
    token = 1
    if(maximizing):
        token = 2
    for i in range(0, dimens):
        if(maximizing):
            if((not(res == -1 or beta == -1)) and res > beta):
                break
        else:
            if((not(res == -1 or alpha == -1)) and res < alpha):
                break

        if(heights[i] < dimens):
            push(i, token)
            if(res == -1):
                res = minimax(alpha, beta, not maximizing)
                if(maximizing):
                    alpha = res
                else:
                    beta = res
            elif(maximizing):
                res = max(res, minimax(alpha, beta, not maximizing))
                alpha = max(res, alpha)
            else:
                res = min(res, minimax(alpha, beta, not maximizing))
                beta = min(res, beta)
            pop(i)
    return res

'''
Drops the specified token in col
'''
def push(col, token):
    global mv
    col = int(col)
    board[dimens - 1 - int(heights[col])][col] = token
    mv = (dimens - 1 - int(heights[col]), col)

    heights[col] += 1

'''
Removes the topmost token in col
'''
def pop(col):
    col = int(col)
    board[dimens - 1 - int(heights[col])][col] = 0
    heights[col] -= 1

'''
Get optimal move for computer
'''
def getNextMove():
    max = -1
    res = -1
    for i in range(0, dimens):
        if(heights[i] < dimens):
            push(i, 2)
            temp = minimax(-1, -1, False)
            if(temp > max):
                max = temp
                res = i
            pop(i)
    return res

def play():
    global turn
    win = inWinningState()
    if(win != 0):
        print(board)
        if(win == 1):
            print('Mac wins!')
        else:
            print('Human wins!')
    elif(turn == 0):
        print(board)
        print('Select a column to move to: ')
        col = int(input())
        push(col, 1)
        turn = 1 - turn
        play()
    else:
        move = getNextMove()
        print("move", move)
        push(move, 2)
        turn = 1 - turn
        play()

play()
