import copy
import sys
import random

WIDTH = 1200
HEIGHT = 720

CELL_HEIGHT = HEIGHT // 4
CELL_WIDTH = WIDTH // 8

BASE_X = (WIDTH - CELL_WIDTH*7) // 2
BASE_Y = (HEIGHT - CELL_HEIGHT*2) // 2

sys.setrecursionlimit(10**9 + 10**9)

dct = {}

class EmptyCellException(Exception):
    def __init__(self, side, index):
        super().__init__(f"Ô {side} {index} không có quân, chọn ô khác")

def random_point(side: str, index: int = -1):
    xAxis = [BASE_X + CELL_WIDTH, BASE_X + 2*CELL_WIDTH, BASE_X + 3*CELL_WIDTH, BASE_X + 4*CELL_WIDTH, BASE_X + 5*CELL_WIDTH, BASE_X + 6*CELL_WIDTH,]
        
    x, y = -1, -1
    if side == 'left':
        x = random.uniform(BASE_X + 50, BASE_X + CELL_WIDTH - 50)
        y = random.uniform(BASE_Y + 50, BASE_Y + CELL_HEIGHT*2 - 80)
    if side == 'right':
        x = random.uniform(BASE_X + 6*CELL_WIDTH + 50, BASE_X + 7*CELL_WIDTH - 50)
        y = random.uniform(BASE_Y + 50, BASE_Y + CELL_HEIGHT*2 - 80)
    
    if side == 'opponent':
        index = 5 - index
        x = random.uniform(xAxis[index - 1] + 50, xAxis[index] - 70 - 50)
        y = random.uniform(BASE_Y + 50, BASE_Y + CELL_HEIGHT - 50)
    if side == 'player':
        x = random.uniform(xAxis[index] + 50, xAxis[index + 1] - 70 - 50)
        y = random.uniform(BASE_Y + CELL_HEIGHT + 50, BASE_Y + 2*CELL_HEIGHT - 50)
        
    return x, y
class Cell:
    def __init__(self, numberSeed, numberLarge = 0):
        self.numberSeed: int = numberSeed
        self.numberLarge: int = numberLarge
    
    def __str__(self):
        return self.value()
    
    def emptyCell(self):
        return self.numberSeed == 0 and self.numberLarge == 0
    
    def numberOfSeed(self):
        return self.numberSeed + self.numberLarge
    
    def value(self) -> int:
        return self.numberSeed + self.numberLarge*10
    
    def setSeedZero(self):
        self.numberSeed = 0
        self.numberLarge = 0
        
    def getValue(self):
        value = copy.deepcopy(self.value())
        self.setSeedZero()
        return value
    
    def addOneSeed(self):
        self.numberSeed += 1

    def makeHashString(self):
        return str(self.numberSeed) + "-" + str(self.numberLarge)

    def hash(self):
        return hash((self.numberSeed, self.numberLarge))

class Move():
    def __init__(self, index: int, direction: str):
        #direction = "right" | "left"
        self.index = index
        self.direction = direction

class Board:
    def __init__(self):
        #declare 2 player's seed
        self.playerSeed = 0      #its me
        self.opponentSeed = 0  #its opponent
        
        self.playerLargeSeed = 0      #its me
        self.opponentLargeSeed = 0    #its opponent
        
        #state of board
        self.opponentCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        self.playerCells: list[Cell] = [Cell(5), Cell(5), Cell(5), Cell(5), Cell(5)]
        
        self.borrowPlayer = 0
        self.borrowOpponent = 0
        
        self.leftLargeCell = Cell(0, 1)    # index: 5 for player, -1 for opponent
        self.rightLargeCell = Cell(0, 1)   # index: -1 for player, 5 for opponent
        
        self.leftNormalPosition = []
        self.rightNormalPosition = []
        
        self.playerNormalPosition = [[], [], [], [], []]
        self.opponentNormalPosition = [[], [], [], [], []]
        
        self.initPosition(BASE_X + CELL_WIDTH, BASE_Y, CELL_WIDTH, CELL_HEIGHT)

    def hash(self):
        return hash((self.playerCells, self.opponentCells, self.leftLargeCell, self.rightLargeCell))
        
    def initPosition(self, baseX: float, baseY: float, cell_width: float, cell_height: float):
        for _ in range(5):
            for __ in range(5):
                x = random.uniform(baseX + 50, baseX + cell_width - 50)
                y = random.uniform(baseY + 50, baseY + cell_height - 50)
                
                self.opponentNormalPosition[4 - _] += [(x, y)]
                self.playerNormalPosition[_] += [(x, y + cell_height)]
            baseX += cell_width
            
    def addPosition(self, side: str, indexCell: int = -1):
        x, y = random_point(side, indexCell)
        
        if side == 'left':
            self.leftNormalPosition += [(x, y)]
        elif side == 'right':
            self.rightNormalPosition += [(x, y)]
        elif side == 'player':
            self.playerNormalPosition[indexCell] += [(x, y)]
        else:
            self.opponentNormalPosition[indexCell] += [(x, y)]
    
    def removeAllPosition(self, side: str, indexCell: int = -1):
        if side == 'left':
            self.leftNormalPosition = []
        elif side == 'right':
            self.rightNormalPosition = []
        elif side == 'player':
            self.playerNormalPosition[indexCell] = []
        else:
            self.opponentNormalPosition[indexCell] = []
            
    def print(self):
        print("---------------------------------------------")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.opponentCells[4].value()}  |  {self.opponentCells[3].value()}  |  {self.opponentCells[2].value()}  |  {self.opponentCells[1].value()}  |  {self.opponentCells[0].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print(f"|  {self.leftLargeCell.value() if self.leftLargeCell.value() else ' ' + str(self.leftLargeCell.value())}  |-----------------------------|  {self.rightLargeCell.value()}  |")
        print("|      |     |     |     |     |     |      |")
        print(f"|      |  {self.playerCells[0].value()}  |  {self.playerCells[1].value()}  |  {self.playerCells[2].value()}  |  {self.playerCells[3].value()}  |  {self.playerCells[4].value()}  |      |")
        print("|      |     |     |     |     |     |      |")
        print("---------------------------------------------")
        
        """"
        opponentO = copy.deepcopy(self.opponentNormalPosition)
        opponentO.reverse()
        
        print(self.leftNormalPosition)
        print(opponentO)
        print(self.playerNormalPosition)
        print(self.rightNormalPosition)
        
        print(self.leftLargeCell.numberLarge, self.leftLargeCell.numberSeed)
        print(self.rightLargeCell.numberLarge, self.rightLargeCell.numberSeed)
        """
        
        # print(self.calcPlayerSeed() - self.calcOpponentSeed())
        print("Player:", self.playerSeed, self.playerLargeSeed)
        print("Opponent:", self.opponentSeed, self.opponentLargeSeed)
        
    def outOfNormalSeed(self, side):
        normalSeed =  0
        if side == 'player':
            normalSeed = self.playerSeed - 10*self.playerLargeSeed
            if normalSeed <= 5: return True
        else:
            normalSeed = self.opponentSeed - 10*self.opponentLargeSeed
            if normalSeed <= 5: return True 
        return False
    
    def isTerminalState(self, side: str):        
        playerCanNotBorrow, opponentCanNotBorrow = False, False
        
        if side == 'player':
            playerNormalSeed = self.playerSeed - 10*self.playerLargeSeed
            playerCanNotBorrow = self.shouldPlayerBorrow() and playerNormalSeed == 0 and self.outOfNormalSeed('opponent')
        else: 
            opponentNormalSeed = self.opponentSeed - 10*self.opponentLargeSeed
            opponentCanNotBorrow = self.shouldOpponentBorrow() and opponentNormalSeed == 0 and self.outOfNormalSeed('player')
            
        outOfLargeCell = self.leftLargeCell.value() == 0 and self.rightLargeCell.value() == 0
        borrowToMuch = self.borrowOpponent >= 36 or self.borrowPlayer >= 36
        
        terminal = playerCanNotBorrow or opponentCanNotBorrow or outOfLargeCell or borrowToMuch
        return terminal
    def calcPlayerSeed(self):
        return self.playerSeed
    
    def calcOpponentSeed(self):
        return self.opponentSeed
    
    def winner(self):
        if self.calcPlayerSeed() > self.calcOpponentSeed():
            return "PLAYER"
        return "OPPONENT"
    
    def shouldPlayerBorrow(self):
        for i in range(5):
                if self.playerCells[i].value() != 0:
                    return False
        return True
            
    def shouldOpponentBorrow(self):
        for i in range(5):
            if self.opponentCells[i].value() != 0:
                return False
        return True
    
    def noSeedAllCells(self, side):
        if side == 'player':
            for i in range(5):
                if self.playerCells[i].value() != 0: return
                            
            normalSeed = self.playerSeed - 10*self.playerLargeSeed #seed can give
            
            if normalSeed < 5 and self.opponentSeed - 10*self.opponentLargeSeed > 5 - normalSeed:
                self.borrowPlayer = self.borrowPlayer + (5 - normalSeed)
                self.opponentSeed = self.opponentSeed - (5 - normalSeed)
                normalSeed = 5
            
            for i in range(5):
                if normalSeed == 0: break
                
                normalSeed -= 1
                self.playerCells[i].addOneSeed()
                self.addPosition('player', i)
            
            self.playerSeed = normalSeed + 10*self.playerLargeSeed

        else:
            for i in range(5):
                if self.opponentCells[i].value() != 0: return
                        
            normalSeed = self.opponentSeed - 10*self.opponentLargeSeed
            
            if normalSeed < 5 and self.playerSeed - 10*self.playerLargeSeed > 5 - normalSeed:
                self.borrowOpponent = self.borrowOpponent + (5 - normalSeed)
                self.playerSeed = self.playerSeed - (5 - normalSeed)
                normalSeed = 5
            
            for i in range(5):
                if normalSeed == 0: break
                
                normalSeed -= 1
                self.opponentCells[i].addOneSeed()
                self.addPosition('opponent', i)
            
            self.opponentSeed = normalSeed + 10*self.opponentLargeSeed    
                            
    def leftToRight(self, side: str, index: int) -> tuple[str, int, bool]: # return side, next index
        if side == 'rightMiddle' and index == 5:
            return 'opponent', 0, False
        
        if side == 'rightMiddle' and index == -1:
            return 'player', 4, False
        
        if side == 'leftMiddle' and index == 5:
            return 'opponent', 4, True
        
        if side == 'leftMiddle' and index == -1:
            return 'player', 0, True
        
        if side == 'player' and index + 1 == 5:
            return 'rightMiddle', -1, False
        
        if side == 'opponent' and index - 1 == -1:
            return 'rightMiddle', 5, False
        
        if side == 'player':
            return side, index + 1, True
        
        if side == 'opponent':
            return side, index - 1, True
        
    def rightToLeft(self, side: str, index: int) -> tuple[str, int, bool]: # return next index
        if side == 'rightMiddle' and index == -1:
            return 'opponent', 0, False
        
        if side == 'rightMiddle' and index == 5:
            return 'player', 4, False
        
        if side == 'leftMiddle' and index == 5:
            return 'player', 0, True
        
        if side == 'leftMiddle' and index == -1:
            return 'opponent', 4, True
        
        if side == 'opponent' and index + 1 == 5:
            return 'leftMiddle', -1, True
        
        if side == 'player' and index - 1 == -1:
            return 'leftMiddle', 5, True
        
        if side == 'player':
            return side, index - 1, False
        
        if side == 'opponent':
            return side, index + 1, False

    def handleEmptyCell(self, side: str, index: int, left_to_right: bool) -> int:
        # bang bang
        zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
        winSeed = 0
        
        while zero == 0:
            side, nextIndex, left_to_right = self.leftToRight(side, index) if left_to_right else self.rightToLeft(side, index)
            
            nextWin = 0
            if side == 'leftMiddle':
                nextWin = self.leftLargeCell.getValue()
                self.removeAllPosition('left')
                
            elif side == 'rightMiddle':
                nextWin = self.rightLargeCell.getValue()
                self.removeAllPosition('right')
                
            elif side == 'player':
                nextWin = self.playerCells[nextIndex].getValue()
                self.removeAllPosition('player', nextIndex)
                
            elif side == 'opponent':
                nextWin = self.opponentCells[nextIndex].getValue()
                self.removeAllPosition('opponent', nextIndex)
            
            if nextWin == 0:
                return winSeed
            
            winSeed += nextWin    
            side, index, left_to_right = self.leftToRight(side, nextIndex) if left_to_right else self.rightToLeft(side, nextIndex)
            if side == 'leftMiddle' or side == 'rightMiddle':
                break
            zero = self.playerCells[index].value() if side == 'player' else self.opponentCells[index].value()
            
        return winSeed

    def playerMove(self, index: int, direction: str):
        leftLargeBelong = not (self.leftLargeCell.numberLarge > 0)
        rightLargeBelong = not (self.rightLargeCell.numberLarge > 0)
        
        self.noSeedAllCells('player')
        
        if self.playerCells[index].value() == 0:
            raise EmptyCellException('player', index)
        
        current = self.playerCells[index].getValue()
        self.removeAllPosition('player', index)
        
        side = 'player'
        left_to_right = True
        if direction == 'left':
            left_to_right = False

        while True:        
            while current != 0:
                if left_to_right:
                    side, index, left_to_right = self.leftToRight(side, index)
                else:
                    side, index, left_to_right = self.rightToLeft(side, index)
                
                current -= 1
                if side == 'leftMiddle':
                    self.leftLargeCell.addOneSeed()
                    self.addPosition("left")
                    
                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    self.addPosition("right")
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    self.addPosition("player", index)
                    
                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    self.addPosition("opponent", index)
                    
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
                self.removeAllPosition('player', index)
                
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                self.removeAllPosition('opponent', index)
                
                
            if value == 0:
                self.playerSeed += self.handleEmptyCell(side, index, left_to_right)
                break
            current = value
            
        if (not leftLargeBelong and self.leftLargeCell.numberLarge == 0 ):
            self.playerLargeSeed += 1
        if (not rightLargeBelong and self.rightLargeCell.numberLarge == 0):
            self.playerLargeSeed += 1

    def opponentMove(self, index: int, direction: str):
        leftLargeBelong = not (self.leftLargeCell.numberLarge > 0)
        rightLargeBelong = not (self.rightLargeCell.numberLarge > 0)
        
        self.noSeedAllCells('opponent')
        
        if self.opponentCells[index].value() == 0:
            raise EmptyCellException('opponent', index)
        
        current = self.opponentCells[index].getValue()
        self.removeAllPosition('opponent', index)        
        
        side = 'opponent'
        left_to_right = False
        if direction == 'left':
            left_to_right = True

        while True:        
            while current != 0:
                if left_to_right:
                    side, index, left_to_right = self.leftToRight(side, index)
                else:
                    side, index, left_to_right = self.rightToLeft(side, index)
                
                current -= 1
                if side == 'leftMiddle':
                    self.leftLargeCell.addOneSeed()
                    self.addPosition("left")

                elif side == 'rightMiddle':
                    self.rightLargeCell.addOneSeed()
                    self.addPosition("right")
                    
                elif side == 'player':
                    self.playerCells[index].addOneSeed()
                    self.addPosition("player", index)

                elif side == 'opponent':
                    self.opponentCells[index].addOneSeed()
                    self.addPosition("opponent", index)
            
            if left_to_right:
                side, index, left_to_right = self.leftToRight(side, index)
            else:
                side, index, left_to_right = self.rightToLeft(side, index)
                    
            if side == 'leftMiddle' or side == 'rightMiddle':
                break

            value = -1
            if side == 'player':
                value = self.playerCells[index].getValue()
                self.removeAllPosition('player', index)
                
            elif side == 'opponent':
                value = self.opponentCells[index].getValue()
                self.removeAllPosition('opponent', index)
                
                
            if value == 0:
                self.opponentSeed += self.handleEmptyCell(side, index, left_to_right)
                break
            current = value
        
        if (not leftLargeBelong and self.leftLargeCell.numberLarge == 0 ):
            self.opponentLargeSeed += 1
        if (not rightLargeBelong and self.rightLargeCell.numberLarge == 0):
            self.opponentLargeSeed += 1
                
    def makeHashString(self):
        playerCellsString = "#".join([playerCell.makeHashString() for playerCell in self.playerCells])
        opponentCellsString = "#".join([opponentCell.makeHashString() for opponentCell in self.opponentCells])
        return "#".join((playerCellsString, opponentCellsString, self.leftLargeCell.makeHashString(), self.rightLargeCell.makeHashString()))
class minimaxNode:
    def __init__(self, level: int = 0, playerTurn: int = 0, board: Board = None, index: int = 0, direction: str = ""):
        self.level = level
        self.playerTurn = playerTurn
        self.index = index
        self.direction = direction

        if self.level != 0:
            self.board = self.build(board)
        else:
            self.board = board
            
        self.value = self.board.calcPlayerSeed() - self.board.calcOpponentSeed()

        self.bestPath = []
        self.children = []

    def build(self, board: Board) -> Board:        
        if self.playerTurn == 1:
            board.playerMove(self.index, self.direction)
        else:
            board.opponentMove(self.index, self.direction)
        return board
    
    def isLeaf(self):
        if self.board is None: return True
        return self.board.isTerminalState('player' if self.playerTurn == 1 else 'opponent')
    
    def isWin(self):
        return self.board.winner() == "PLAYER"
    
    def makeHashString(self):
        if self.board is None: return None
        return "+".join((str(self.playerTurn), str(self.index), str(self.direction), self.board.makeHashString()))
    
    def hash(self):
        return hash((self.playerTurn, self.index, self.direction, self.board))

class minimaxTree:    
    def __init__(self, playerTurn: int = -1, maxLevel: int = -1, board: Board = Board() ):
        self.root = minimaxNode(0, playerTurn, board)
        self.maxLevel = maxLevel #float("inf")
        self.bestPath = []
        self.isFound = False

    def findBestMove(self):
        if self.root.isLeaf():
            return None, None
        value, path = self.build(self.root)
        return path[1].index, path[1].direction
        
    def build(self, curNode: minimaxNode, visited: set = set(), alpha = -10**10, beta = 10**10) -> tuple[int, list[minimaxNode]]:
        if curNode.isLeaf() or self.maxLevel <= curNode.level:
            if curNode.isLeaf():
                if curNode.isWin():
                    self.maxLevel = min(self.maxLevel, curNode.level)
            return curNode.value, [curNode]
        
        bestPath = []

        for index in range(5):           
            if (curNode.playerTurn == 1 and not curNode.board.shouldOpponentBorrow() and curNode.board.opponentCells[index].value() == 0) or (curNode.playerTurn == -1 and not curNode.board.shouldPlayerBorrow() and curNode.board.playerCells[index].value() == 0):
                continue
            newValue = None
            
            for direction in ('left', 'right'):
                board = copy.deepcopy(curNode.board)
                
                newNode = minimaxNode(curNode.level + 1, -curNode.playerTurn, board, index, direction)
                
                if newNode.makeHashString() not in visited:
                    visited.add(newNode.makeHashString())
                    curNode.children.append(newNode)
                    newValue, newPath = self.build(newNode, visited, alpha, beta)
                    visited.remove(newNode.makeHashString())

                    if curNode.playerTurn == 1:
                        if curNode.level == 0:
                            if beta > newValue:
                                beta = newValue
                                bestPath = newPath
                        elif alpha < newValue:
                            alpha = newValue
                            bestPath = newPath
                    else:
                        if curNode.level == 0:
                            if alpha < newValue:
                                alpha = newValue
                                bestPath = newPath
                        elif beta > newValue:
                            beta = newValue
                            bestPath = newPath

                if alpha >= beta:   
                    break

        # print (curNode.level, curNode.playerTurn, alpha, beta)
        
        if curNode.playerTurn == 1:
            return [alpha, [curNode] + bestPath]
        return [beta, [curNode] + bestPath]


# orig_stdout = sys.stdout
# f = open('out.txt', 'w')
# sys.stdout = f
# board = Board()
# board.print()

# playerTurn = -1
# start = True

# while not board.isTerminalState('player' if playerTurn == 1 else 'opponent'):
#     tree = minimaxTree(-playerTurn, 20, board) if playerTurn == 1 else minimaxTree(-playerTurn, 5, board)
#     start = False
#     index, direction = tree.findBestMove()
    
#     print("player, index, direction: ", playerTurn, index, direction)
#     if playerTurn == 1:
#         board.playerMove(index, direction)
#         playerTurn = -1
#     else:
#         board.opponentMove(index, direction)
#         playerTurn = 1    
#     board.print()

# sys.stdout = orig_stdout    
# f.close()

# print(board.winner())    

# print(dct)