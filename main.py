import sys
import os

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