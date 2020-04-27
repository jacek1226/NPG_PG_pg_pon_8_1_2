class Board:

    def __init__ (self,size):
        self.size=size
        self.tiles = [["." for col in range(size)] for row in range(size)]
        self.player='X'

    def printBoard(self):
        print()
        for row in range (0,self.size):
            for col in range (0,self.size):
                print(self.tiles[row][col], end=' ')
            print()
        print()

    def changeTile(self,row, col):
        if self.tiles[row][col]!=".":
            print("To miejsce jest juz zajete!")
            return None
        self.tiles[row][col] = self.player
        self.swapPlayer()
        print("Zmienione!")
        return True

    def swapPlayer(self):
        if(self.player=='X'):
            self.player='O'
            return
        self.player='X'

    def checkIfFull(self):
        for row in range (0,self.size):
            for col in range (0,self.size):
                if self.tiles[row][col]==".":
                    return False
        return True

    def getValue(self,row, col):
        return self.tiles[row][col]

    def checkIfWin(self):
        for row in range (0,self.size):
            for col in range (0,self.size):

                #check if empty
                if self.tiles[col][row]==".":
                    continue

                #check horizontal
                if col>=1 and col <= self.size-2:
                    if self.tiles[col][row] == self.tiles[col-1][row] \
                            and self.tiles[col][row] == self.tiles[col+1][row] :
                        return True

                    #diagnal check
                    if row >= 1 and row <= self.size - 2:
                        if self.tiles[col][row] == self.tiles[col - 1][row-1] \
                                and self.tiles[col][row] ==self.tiles[col + 1][row+1]:
                            return True
                        if self.tiles[col][row] == self.tiles[col - 1][row+1] \
                                and self.tiles[col][row] ==self.tiles[col + 1][row-1]:
                            return True

                #check vertical
                if row >= 1 and row <= self.size - 2:
                    if self.tiles[col][row] == self.tiles[col][row-1] \
                            and self.tiles[col][row] == self.tiles[col][row+1] :
                        return True
        return False