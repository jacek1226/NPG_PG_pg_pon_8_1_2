import tkinter as tk
import time
import random as rand
from Board import Board
from AIPlayer import AIPlayer

HEIGHT= 400
WIDTH = 400
GUI_COLOR='#5584B4'

class GuiPart:
    def __init__(self, root):
        self.root=root
        self.GAMEHEIGHT = 7 / 8
        #defining always visible elements of GUI
        canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
        canvas.pack()

        self.guiFrame = tk.Frame(root, bg=GUI_COLOR, bd=5)
        self.guiFrame.place(anchor='n', rely=0, relx=0.5, relwidth=1, relheight=1)

        nameLabel = tk.Label(self.guiFrame, font=40, text='KÓŁKO I KRZYŻYK!', bg=GUI_COLOR)
        nameLabel.place(rely=0.1, relx=0, relwidth=1, relheight=0.1)

        #defining menu interface
        self.menuFrame=tk.Frame(self.guiFrame,bg=GUI_COLOR)
        startButton = tk.Button(self.menuFrame, text='Nowa gra',
                                command=lambda: self.changeScreen(self.menuFrame, self.selectionFrame))
        startButton.place(rely=0.2, relx=0.1, relwidth=0.8, relheight=0.15)

        statisticsButton = tk.Button(self.menuFrame, text='Statystyki')
        statisticsButton.place(rely=0.45, relx=0.1, relwidth=0.8, relheight=0.15)

        endButton = tk.Button(self.menuFrame, text="Wyjdź", command=lambda: endCommand())
        endButton.place(rely=0.7, relx=0.1, relwidth=0.8, relheight=0.15)

        #defining game choosing interface
        self.selectionFrame=tk.Frame(self.guiFrame,bg=GUI_COLOR)
        normalGameButton = tk.Button(self.selectionFrame, text='Gra w 2 osoby', command=lambda: [self.newGame(False), self.StartTimer()])
        normalGameButton.place(rely=0.2, relx=0.1, relwidth=0.8, relheight=0.15)

        computerGameButton = tk.Button(self.selectionFrame, text='Gra z komputerem', command=lambda: self.changeScreen(self.selectionFrame, self.AISelectionFrame))
        computerGameButton.place(rely=0.45, relx=0.1, relwidth=0.8, relheight=0.15)

        menuButton = tk.Button(self.selectionFrame, text="Powrót do menu głównego",
                               command=lambda: self.changeScreen(self.selectionFrame, self.menuFrame) )
        menuButton.place(rely=0.7, relx=0.1, relwidth=0.8, relheight=0.15)

        self.rowButtons=list(map(lambda x: tk.Button( self.selectionFrame,text=str(x),
                                                      command=lambda: self.changeSize(x)),range (3, 6)))
        for i in range (3):
            self.rowButtons[i].place(rely=0, relx=0.1+0.3*i, relwidth=0.2, relheight=0.1)

        self.menuFrame.place(anchor='n', rely=0.2, relx=0.5, relwidth=1, relheight=0.7)
        self.changeSize(3)

        self.AISelectionFrame = tk.Frame(self.guiFrame, bg=GUI_COLOR)

        EasyAIButton = tk.Button(self.AISelectionFrame, text='Tryb latwy',
                                     command=lambda: [self.newGame(True, "easy"), self.StartTimer()])
        EasyAIButton.place(rely=0.2, relx=0.1, relwidth=0.8, relheight=0.15)

        HardAIButton = tk.Button(self.AISelectionFrame, text='Tryb trudny',
                                       command=lambda: [self.newGame(True, "hard"), self.StartTimer()])
        HardAIButton.place(rely=0.45, relx=0.1, relwidth=0.8, relheight=0.15)

        menuAIButton = tk.Button(self.AISelectionFrame, text="Powrót do menu głównego",
                               command=lambda: self.changeScreen(self.AISelectionFrame, self.selectionFrame))
        menuAIButton.place(rely=0.7, relx=0.1, relwidth=0.8, relheight=0.15)
    def changeScreen(self, oldScreen, newScreen):
        oldScreen.place_forget()
        newScreen.place(anchor='n', rely=0.2, relx=0.5, relwidth=1, relheight=0.8)

    def changeSize(self, n):
        self.size=n
        for i in range (3):
            self.rowButtons[i]["bg"]="white"
        self.rowButtons[n-3]["bg"]="red"

    def newGame(self,withAI: bool,AIType="easy"):

        self.withAI: bool=withAI
        self.AIType=AIType
        self.gameFrame=tk.Frame(self.guiFrame,bg=GUI_COLOR)
        self.board = Board(self.size)
        if withAI:
            self.AIPlayer = AIPlayer(self.board)

        self.gameButtons = list(map(lambda y: list(map(lambda x: tk.Button(self.gameFrame,
                                            command=lambda: self.gameButtonClicked(y,x)), range(self.size))), range(self.size)))
        for i in range(self.size):
            for j in range(self.size):
                self.gameButtons[i][j].place(rely=(1/self.size)*i*self.GAMEHEIGHT, relx=(1/self.size)*j, relwidth=(1/self.size),
                                             relheight=(1/self.size)*self.GAMEHEIGHT)

        self.moveToStartButton = tk.Button(self.gameFrame, text="<<",
                                           command=lambda: [self.board.undo_all_moves(), self.updateAllCellsText()])
        self.moveToStartButton.place(rely=0.92, relx=0, relwidth=0.2, relheight=0.06)

        self.moveBackButton = tk.Button(self.gameFrame, text="<",
                                        command=lambda: [self.board.undo_move(), self.board.undo_move() if self.withAI else 0, self.updateAllCellsText()])
        self.moveBackButton.place(rely=0.92, relx=0.25, relwidth=0.2, relheight=0.06)

        self.moveForwardButton = tk.Button(self.gameFrame, text=">",
                                        command=lambda: [self.board.repeat_move(), self.board.repeat_move() if self.withAI else 0, self.updateAllCellsText()])
        self.moveForwardButton.place(rely=0.92, relx=0.55, relwidth=0.2, relheight=0.06)

        self.moveToLastButton = tk.Button(self.gameFrame, text=">>",
                                        command=lambda: [self.board.repeat_all_moves(), self.updateAllCellsText()])
        self.moveToLastButton.place(rely=0.92, relx=0.8, relwidth=0.2, relheight=0.06)

        self.changeScreen(self.selectionFrame, self.gameFrame)

    def updateAllCellsText(self):
        for row in range(self.size):
            for col in range(self.size):
                self.updateCellText(row,col)

    def updateCellText(self,row,col):
        if self.board.getValue(row, col) == '.':
            self.gameButtons[row][col]["text"] = ""
        else:
            self.gameButtons[row][col]["text"] = self.board.getValue(row, col)

    def checkEndGame(self):
        if self.board.checkIfWin():
            self.stopTimer()
            self.board.swapPlayer()
            self.endOfGame("Wygrał " + self.board.player + "\n Powrót do menu głównego")
            return True

        if self.board.checkIfFull():
            self.stopTimer()
            self.endOfGame("Remis! \n Powrót do menu głównego")
            return True
        return False

    def gameButtonClicked(self, row, col):
        if self.board.changeTile(row, col):
            self.updateCellText(row,col)
            if self.checkEndGame():
                return

            if self.withAI:
                if self.AIType=="hard":
                    self.AIPlayer.makeMove()
                    self.updateAllCellsText()
                    self.checkEndGame()
                    return
                if self.AIType=="easy":
                    self.AIPlayer.makeRandomMove()
                    self.updateAllCellsText()
                    self.checkEndGame()
                    return



    def endOfGame(self, text):
        for i in range(self.size):
            for j in range(self.size):
                self.gameButtons[i][j].config(command=lambda: None)

        returnButton = tk.Button(self.gameFrame, text=text, bg='#A4B691', command=lambda: self.backToMenu())
        returnButton.place(rely=0.2, relx=0.2, relwidth=0.6, relheight=0.3)

    def backToMenu(self)-> None:
        """Deletes the timer label after finished game."""
        
        self.changeScreen(self.gameFrame, self.menuFrame)
        self.gameFrame.destroy()
        self.timer.destroy()

    def StartTimer(self)-> None:
        """Starts counting time and places the label with timer."""
        
        self._start: float = 0.0
        self._time_passed: float = 0.0
        self._running: bool = 0
        self.time_str = tk.StringVar()
        
        #placing the label with timer
        self.timer = tk.Label(self.guiFrame, textvariable=self.time_str, bg = GUI_COLOR, font = (20))
        self.setTime(self._time_passed)
        self.timer.pack()
        
        #updating the timer
        if not self._running:
            self._start = time.time() - self._time_passed
            self.timeUpdate()
            self._running = 1

    def setTime(self, passed):
        minutes = int(passed / 60)
        seconds = int(passed - minutes * 60.0)
        centy_seconds = int((passed - minutes * 60.0 - seconds) * 100)
        self.time_str.set('%02d:%02d:%02d' % (minutes, seconds, centy_seconds))


    def timeUpdate(self):
        self._time_passed = time.time() - self._start
        self.setTime(self._time_passed)
        self._timer = root.after(50, self.timeUpdate)

    def stopTimer(self):
        if self._running:
            root.after_cancel(self._timer)
            self._running = 0

root=tk.Tk()

gui = GuiPart(root)
root.mainloop()
