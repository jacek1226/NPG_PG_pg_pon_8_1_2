from Board import Board
from random import randrange

class AIPlayer:
    """Class is responsible for considering the best AI's move"""
    def __init__(self, board: Board):
        self.board = board
        self.board.swapPlayer()
        self.sign = self.board.player
        self.board.swapPlayer()
        self.opponentSign = self.board.player

    def onlyMyTiles(self, col:int, row:int)-> bool:
        """Checks if in given tile is AI's sign
        Parameters
        ------
        col : int
            number of column
        row : int
            number of row
        Returns
        ------
        bool
            true if there is AI's sign in that tile and false otherwise
        """
        return self.board.tiles[col][row] == self.sign

    def onlyOpponentTiles(self, col:int, row:int)-> bool:
         """Checks if in given tile is not AI's sign
        Parameters
        ------
        col : int
            number of column
        row : int
            number of row
        Returns
        ------
        bool
            true if there isn't AI's sign in that tile and false otherwise
        """
        return self.board.tiles[col][row] == self.opponentSign

    def onlyOneEmptyTile(self, countTiles:int, countEmptyTiles:int)-> bool:
        """Checks if there is only one empty tile on a line and the rest is AI's sign
        
        Parameters
        ------
        countTiles : int
            number of AI's or player's tiles 
        countEmptyTiles : int
            number of empty tiles
        Returns
        ------
        bool
            true if there is only one empty tile and the rest is AI's, false otherwise
        """
        return countEmptyTiles == 1 and countTiles == self.board.size - 1

    def withoutOppositeSign(self, countTiles:int, countEmptyTiles:int)-> bool:
        """Checs if there is a line without opposite sign
        
        Parameters
        ------
        countTiles : int
            number of AI's tiles 
        countEmptyTiles : int
            numer of empty tiles
        Returns
        bool
            true when there is at least one player's sign and others are empty, false otherwise 
        """
        return (not countEmptyTiles == self.board.size) and (countTiles + countEmptyTiles == self.board.size)

    def makeMove(self)-> None:
         """If there isn't any good move, it goes to function makeRandomMove
         First checks if AI can win this round, 
         then chcecks if his opponent is about to win, 
         next it checks if there is any possibility of winning. 
         At the end it makes random move"""
         
        if not self.tryToFindWith(self.onlyMyTiles, self.onlyOneEmptyTile):
            if not self.tryToFindWith(self.onlyOpponentTiles, self.onlyOneEmptyTile):
                if not self.tryToFindWith(self.onlyMyTiles, self.withoutOppositeSign):
                    self.makeRandomMove()

    def tryToFindWith(self, equalToGivenSign:method, satisfies:method)-> bool:
        print(aaaa)
        """Chcecks if there is a line meeting requirements, return false when there is no such a line.
        
        Parameters
        ------
        equalToGivenSign : method
            Check whose sign is it
        satisfies : method
            Check if line is proper
        Returns
        ------
        bool
            true if optimal line was found or false when it wasn't"""
            
        """check rows"""
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

        """check cols"""
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

        """check diag"""
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

        """check diag"""
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

    def makeRandomMove(self)-> None:
        """Makes random move for AI."""
        
        while True:
            coords=(randrange(0, self.board.size), randrange(0, self.board.size))
            if self.board.changeTile(coords[0], coords[1]):
                break
