from Board import Board
from random import randrange

class AIPlayer:
    def __init__(self, board: Board):
        self.board = board
        self.board.swapPlayer()
        self.sign = self.board.player
        self.board.swapPlayer()
        self.opponentSign = self.board.player

    def onlyMyTiles(self, col, row):
        return self.board.tiles[col][row] == self.sign

    def onlyOpponentTiles(self, col, row):
        return self.board.tiles[col][row] == self.opponentSign

    def onlyOneEmptyTile(self, countTiles, countEmptyTiles):
        return countEmptyTiles == 1 and countTiles == self.board.size - 1

    def withoutOppositeSign(self, countTiles, countEmptyTiles):
        return (not countEmptyTiles == self.board.size) and (countTiles + countEmptyTiles == self.board.size)

    def makeMove(self):
        if not self.tryToFindWith(self.onlyMyTiles, self.onlyOneEmptyTile):
            if not self.tryToFindWith(self.onlyOpponentTiles, self.onlyOneEmptyTile):
                if not self.tryToFindWith(self.onlyMyTiles, self.withoutOppositeSign):
                    self.makeRandomMove()

    def tryToFindWith(self, equalToGivenSign, satisfies):
        # check rows
        for row in range(0, self.board.size):
            emptyTile = (None, None)
            countTiles = 0
            countEmptyTiles = 0
            for col in range(0, self.board.size):
                if self.board.tiles[col][row] == ".":
                    emptyTile = (col, row)
                    countEmptyTiles += 1
                elif equalToGivenSign(col, row):
                    countTiles += 1
            if satisfies(countTiles, countEmptyTiles):
                return self.board.changeTile(emptyTile[0], emptyTile[1])

        # check cols
        for col in range(0, self.board.size):
            emptyTile = (None, None)
            countTiles = 0
            countEmptyTiles = 0
            for row in range(0, self.board.size):
                if self.board.tiles[col][row] == ".":
                    emptyTile = (col, row)
                    countEmptyTiles += 1
                elif equalToGivenSign(col, row):
                    countTiles += 1
            if satisfies(countTiles, countEmptyTiles):
                return self.board.changeTile(emptyTile[0], emptyTile[1])

        #check diag
        emptyTile = (None, None)
        countTiles = 0
        countEmptyTiles = 0
        for i in range(0, self.board.size):
            if self.board.tiles[i][i] == ".":
                emptyTile = (i, i)
                countEmptyTiles += 1
            elif equalToGivenSign(i, i):
                countTiles += 1

        if satisfies(countTiles, countEmptyTiles):
            return self.board.changeTile(emptyTile[0], emptyTile[1])

        # check diag
        emptyTile = (None, None)
        countTiles = 0
        countEmptyTiles = 0
        for i in range(0, self.board.size):
            if self.board.tiles[i][self.board.size-i-1] == ".":
                emptyTile = (i, self.board.size-i-1)
                countEmptyTiles += 1
            elif equalToGivenSign(i, self.board.size - i - 1):
                countTiles += 1

        if satisfies(countTiles, countEmptyTiles):
            return self.board.changeTile(emptyTile[0], emptyTile[1])

        return False

    def makeRandomMove(self):
        while True:
            coords=(randrange(0, self.board.size), randrange(0, self.board.size))
            if self.board.changeTile(coords[0], coords[1]):
                break