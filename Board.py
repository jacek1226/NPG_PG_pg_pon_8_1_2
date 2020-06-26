from typing import *

class Board:

    def __init__(self, size: int):
        self.moves: List[Tuple[int, int]] = []  #List of moves' coordinates
        self.undone_moves: List[Tuple[int, int]] = []  #List of undone moves' coordinates
        self.size: int = size #size of the game board
        self.tiles: List[List[str]] = [["." for col in range(size)] for row in range(size)] #board filled with "."
        self.player: str = 'X' #player
        self.numToWin: int = size if size == 3 else 4 #number of one symbol in a row which is enough to win

    def changeTile(self, row: int, col: int)-> bool:
        """Makes the move - places the right symbol (O or X) in the chosen cell.

        Parameters
        ----------
        row : int
        Row in which is placed the cell that was chosen.
        col : int
        Column in which is placed the cell that was chosen.

        Returns
        -------
        bool
            true if the change was successful or false if the chosen cell is already full.
        """

        if self.tiles[row][col] != ".":
            print("To miejsce jest juz zajete!")
            return False
        #adding move coordinates to the 'moves' list
        self.moves.append((row, col))
        self.tiles[row][col] = self.player
        self.swapPlayer()
        return True

    def swapPlayer(self)-> None:
        """Swaps the current player."""

        if (self.player == 'X'):
            self.player = 'O'
            return
        self.player = 'X'

    def checkIfFull(self)-> bool:
        """Checks if the board is full - if there are any empty cells.

        Returns
        -------
        bool
            true if the board is full (draw) or false if there are some empty cells left (game goes on).
        """

        for row in range(0, self.size):
            for col in range(0, self.size):
                if self.tiles[row][col] == ".":
                    return False
        return True

    def getValue(self, row: int, col: int)-> str:
        """Gets the content from the choosen cell.

        Parameters
        ----------
        row : int
        Row in which is placed the choosen cell.
        col : int
        Column in which is placed the choosen cell.

        Returns
        -------
        str
            content of the choosen cell
        """


        return self.tiles[row][col]

    def checkIfWin(self)-> bool:
        """Checks if player won.

        Returns
        -------
        bool
            True if somebody won or false if game is still going.
        """

        # check vertical
        value: bool = False
        for col in range(0, self.size):
            value = value or self.checkLine(0, col, 1, 0, self.size)

        # check horizontal
        for row in range(0, self.size):
            value = value or self.checkLine(row, 0, 0, 1, self.size)

        # check diagonal from left to right
        for move in range(0, self.size - self.numToWin + 1):
            # transpose right
            value = value or self.checkLine(0, move, 1, 1, self.size - move)
            # transpose down
            value = value or self.checkLine(move, 0, 1, 1, self.size - move)

        # check diagonal from right to left
        for move in range(0, self.size - self.numToWin + 1):
            # transpose left
            value = value or self.checkLine(0, self.size - 1 - move, 1, -1, self.size - move)
            # transpose down
            value = value or self.checkLine(move, self.size - 1, 1, -1, self.size - move)

        return value

    def checkLine(self, startRow: int, startCol: int, moveRow: int, moveCol: int, numOfElem: int)-> bool:
        """Checks, if there are enought symbols in row in given line, to end the game

        Parameters
        ----------
        startRow: int
        Row, in which is starting point of given line
        startCol: int
        Column, in which is starting point of given line
        moveRow: int
        How many cells to the down direction moves the line by each step
        moveCol: int
        How many cells to the rigth direction moves the line by each step
        numOfElem: int
        Number of Elements in given Line

        Returns
        -------
        bool
            true, if there are enought symbols in a row, to end the game (player/AI won), false otherwise.
        """
        counter = 0
        countedSymbol = self.tiles[startRow][startCol]
        for elem in range(0, numOfElem):
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

    def undo_move(self) -> None:
        """Undoes the previous move, which coordinates are
        deleted from list 'moves' and added to list 'undone moves'."""

        try:
            undo_coordinates: Tuple[int, int] = self.moves[-1]
        except IndexError:
            print("Nie możesz już dalej cofnąć! Jesteś na początku gry!")
        else:
            undo_row: int
            undo_col: int
            undo_row, undo_col = undo_coordinates
            self.tiles[undo_row][undo_col] = "."
            self.swapPlayer()
            self.moves.pop(-1)
            self.undone_moves.append(undo_coordinates)
        return

    def repeat_move(self) -> None:
        """Restores the last undone move, which coordinates are
        deleted from list 'undone_moves' and added to list 'moves'."""

        try:
            repeat_coordinates: Tuple[int, int] = self.undone_moves[-1]
        except IndexError:
            print("Nie ma już ruchów do przywrócenia!")
        else:
            repeat_row: int
            repeat_col: int
            repeat_row, repeat_col = repeat_coordinates

            self.tiles[repeat_row][repeat_col] = self.player
            self.swapPlayer()

            self.moves.append(repeat_coordinates)
            for i in range(len(self.moves) - 1):
                if self.moves[i] == repeat_coordinates:
                    del self.moves[i]

            self.undone_moves.pop(-1)
        return

    def undo_all_moves(self) -> None:
        """Undoes all the moves, which coordinates are
        deleted from list 'moves' and added to list 'undone moves'."""

        try:
            undo_all_coordinates: Tuple[int, int] = self.moves[-1]
        except IndexError:
            print("Już jesteś na początku gry!")
        else:
            for i in range(len(self.moves)):
                undo_all_coordinates = self.moves[-1]
                undo_all_row: int
                undo_all_col: int
                undo_all_row, undo_all_col = undo_all_coordinates
                self.tiles[undo_all_row][undo_all_col] = "."
                self.swapPlayer()
                self.moves.pop(-1)
                self.undone_moves.append(undo_all_coordinates)

        return

    def repeat_all_moves(self) -> None:
        """Restores all the undone moves, which coordinates are
        deleted from list 'undone_moves' and added to list 'moves'."""

        try:
            repeat_all_coordinates: Tuple[int, int] = self.undone_moves[-1]
        except IndexError:
            print("Wszystkie ruchy zostały już przywrócone!")
        else:
            for i in range(len(self.undone_moves)):
                repeat_all_coordinates = self.undone_moves[-1]
                repeat_all_row: int
                repeat_all_col: int
                repeat_all_row, repeat_all_col = repeat_all_coordinates

                self.tiles[repeat_all_row][repeat_all_col] = self.player
                self.swapPlayer()
                self.undone_moves.pop(-1)
                self.moves.append(repeat_all_coordinates)
        return
