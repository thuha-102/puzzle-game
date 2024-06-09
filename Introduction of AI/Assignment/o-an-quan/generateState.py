from state import *
import csv
import random
import copy

def getCurrent(board: Board, index: int, direction: str):
    move = [index, direction]
    move += [board.leftLargeCell.value()]
    move += [board.rightLargeCell.value()]
    for i in range(5):
        move += [board.playerCells[i].value()]
    for i in range(5):
        move += [board.opponentCells[i].value()]
    
    return move
    
for _ in range(1000):
    board = Board()
    
    currentPlayer = -1 #random.randint(0, 1)

    while not board.isTerminalState('player' if currentPlayer == 1 else 'opponent'):
        depth = random.randint(1, 5)
        temp = copy.deepcopy(board)
        tree = minimaxTree(-currentPlayer, depth, temp)
        index, direction = tree.findBestMove()
        move = [depth] + getCurrent(board, index, direction)
        
        if currentPlayer == 1:
            board.playerMove(index, direction)
            currentPlayer = -1
        else:
            board.opponentMove(index, direction)
            currentPlayer = 1
        with open("trainningData.csv", "a") as f:
            csv.writer(f).writerow(move)   
