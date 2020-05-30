class Board:

    def __init__ (self,size):
        self.size=size
        self.tiles = [["." for col in range(size)] for row in range(size)]
        self.player='X'
        self.numToWin=size if size==3 else 4

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
                if self.tiles[row][col] == ".":
                    return False
        return True

    def getValue(self,row, col):
        return self.tiles[row][col]

    def checkIfWin(self):
        #check vertical
        value = False
        for col in range (0, self.size):
            value = value or self.checkLine(0,col,1,0,self.size)

        # check horizontal
        for row in range (0, self.size):
            value = value or self.checkLine(row,0,0,1, self.size)

        #check diagonal from left to right
        for move in range (0, self.size - self.numToWin + 1):
            #transpose right
            value = value or self.checkLine(0,move,1,1,self.size - move)
            #transpose down
            value = value or self.checkLine(move, 0, 1, 1, self.size - move)

        # check diagonal from left to right
        for move in range(0, self.size - self.numToWin + 1):
            # transpose right
            value = value or self.checkLine(0, self.size - 1 - move, 1, -1, self.size - move)
            # transpose down
            value = value or self.checkLine(move, self.size - 1, 1, -1, self.size - move)
            
        return value


    def checkLine(self, startRow, startCol, moveRow, moveCol, numOfElem):
        counter = 0
        countedSymbol = self.tiles[startRow][startCol]
        for elem in range(0, numOfElem):
            # print(startRow + elem * moveRow, startCol + elem * moveCol)
            currentSymbol = self.tiles[startRow + elem * moveRow][startCol + elem * moveCol]
            if currentSymbol == ".":
                counter = 0
            elif currentSymbol == countedSymbol:
                counter += 1
                if counter == self.numToWin:
                    return True
            else:
                counter = 1
                countedSymbol = currentSymbol
        return False
