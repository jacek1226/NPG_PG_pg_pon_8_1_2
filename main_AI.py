import sys
import os
from random import randrange


class Board:

    def __init__ (self,size):
        self.size=size
        self.tiles = [["." for col in range(size)] for row in range(size)]

    def printBoard(self):
        print()
        for row in range (0,self.size):
            for col in range (0,self.size):
                print(self.tiles[row][col], end=' ')
            print()
        print()

    def changeTile(self,row, col, value):
        row=row-1
        col=col-1
        if self.tiles[row][col]!=".":
            print("To miejsce jest juz zajete!")
            return None
        self.tiles[row][col] = value
        print("Zmienione!")
        return True

    def checkIfFull(self):
        for row in range (0,self.size):
            for col in range (0,self.size):
                if self.tiles[col][row]==".":
                    return False
        return True

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
                        return (True,self.tiles[col][row])

                    #diagnal check
                    if row >= 1 and row <= self.size - 2:
                        if self.tiles[col][row] == self.tiles[col - 1][row-1] \
                                and self.tiles[col][row] ==self.tiles[col + 1][row+1]:
                            return (True,self.tiles[col][row])
                        if self.tiles[col][row] == self.tiles[col - 1][row+1] \
                                and self.tiles[col][row] ==self.tiles[col + 1][row-1]:
                            return (True,self.tiles[col][row])

                #check vertical
                if row >= 1 and row <= self.size - 2:
                    if self.tiles[col][row] == self.tiles[col][row-1] \
                            and self.tiles[col][row] == self.tiles[col][row+1] :
                        return (True,self.tiles[col][row])
        return (False,None)

class AIPlayer:
    def __init__(self, board, sign, opponentSign):
        self.board = board
        self.sign = sign
        self.opponentSign = opponentSign

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
                return self.board.changeTile(emptyTile[0]+1, emptyTile[1]+1, self.sign)

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
                return self.board.changeTile(emptyTile[0]+1, emptyTile[1]+1, self.sign)

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
            return self.board.changeTile(emptyTile[0]+1, emptyTile[1]+1, self.sign)

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
            return self.board.changeTile(emptyTile[0] + 1, emptyTile[1] + 1, self.sign)

        return False

    def makeRandomMove(self):
        while True:
            coords=(randrange(1, self.board.size+1), randrange(1, self.board.size+1))
            if self.board.changeTile(coords[0], coords[1], self.sign):
                break

def intInput():
    try:
        x=int(input())
    except ValueError:
        print("Prosze wprowadzic liczbe!")
        return None
    except EOFError:
        print("Prosze wprowadzic liczbe!")
        return None
    return x


def newGame(size):
    os.system("cls")
    print("Zaczeto nowa gre rozmiaru " + str(size))
    board=Board(size)
    run = True
    sides={0: "Krzyzyk", 1: "Kolko"}
    values={0: "X", 1: "O"}
    side=0


    aiPlayer=AIPlayer(board, values[1], values[0])

    while run:
        board.printBoard()
        results = board.checkIfWin()
        if results[0]:
            print("Wygral zawodnik grajacy "+ results[1])
            #print("Wpisz cokolwiek, by powrocic do menu glownego!")
            #input()
            return
        if board.checkIfFull() :
            print("Remis!")
            #print("Wpisz cokolwiek, by powrocic do menu glownego!")
            #input()
            return

        print("Teraz gra "+sides[side])
        if side == 0:
            print("Prosze wybrac rzad, w ktorym chcesz umiescic " +
                  sides[side] + "(1-"+ str(size)+"), inna liczba zakonczy gre.")
            row=intInput()
            if row==None:
                return

            if row<=size and row>=1:
                print("Prosze wybrac kolumne, w ktorym chcesz umiescic " +
                      sides[side] + "(1-"+ str(size)+"), inna liczba zakonczy gre.")
                col = intInput()
                if col == None:
                    return
                if col<=size and col>=1:
                    output=board.changeTile(row, col, values[side])
                    if output==True:
                        side=(side+1)%2
                    continue
            run=False
        else:
            aiPlayer.makeMove()
            side = (side + 1) % 2

def printTUI():
    #print choises
    print("Prosze wpisac numer polecenia, ktore chcesz wykonac:")
    print("  1. Nowa gra")
    print("  2. Statystyki")
    print("  3. Zakoncz")



def main():
    run=True

    #run program while user wants to play a game
    while run:
        #os.system("cls")

        printTUI()

        # get choise
        x = intInput()
        if x == None:
            continue

        # new game
        if (x == 1):
            print("Na planszy jakiego rozmiaru od 3 do 5 chcesz zagrac?")
            print("Wpis dowolna inna liczbe aby powrocic do menu glownego.")
            x = intInput()
            if x == None:
                continue
            # play a game if x is 3,4 or 5
            if x >= 3 and x <= 5:
                newGame(x)
            continue

        # statistics
        elif x == 2:
            print("Statystyki")
            continue
        # end program
        elif x == 3:
            print("Koniec")
            run=False
            break

        # wrong choice
        print("Wprowadzono niepoprawna liczbe")
        continue
    return
main()