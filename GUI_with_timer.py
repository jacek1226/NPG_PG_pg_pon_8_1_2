import tkinter as tk
import queue
import threading
import time
import random as rand
from Board import Board

HEIGHT= 400
WIDTH = 400
GUI_COLOR='#5584B4'
def uaktualnij_statystyki():
    print("a")

class GuiPart:
    def __init__(self, root, mainQueue, endCommand):
        self.queue=mainQueue
        self.root=root
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
        normalGameButton = tk.Button(self.selectionFrame, text='Gra w 2 osoby', command=lambda: [self.newGame(), self.StartTimer()])
        normalGameButton.place(rely=0.2, relx=0.1, relwidth=0.8, relheight=0.15)

        computerGameButton = tk.Button(self.selectionFrame, text='Gra z komputerem')
        computerGameButton.place(rely=0.45, relx=0.1, relwidth=0.8, relheight=0.15)

        menuButton = tk.Button(self.selectionFrame, text="Powrót do menu głównego",
                               command=lambda: self.changeScreen(self.selectionFrame, self.menuFrame) )
        menuButton.place(rely=0.7, relx=0.1, relwidth=0.8, relheight=0.15)
        # next commands can be descibed also like:
        # rows3 = tk.Button(self.selectionFrame,text="3", command=lambda: self.changeRows(3))
        # rows3.place(rely=0, relx=0.1, relwidth=0.2, relheight=0.1)
        #
        # rows4 = tk.Button(self.selectionFrame, text="4", command=lambda: self.changeRows(4))
        # rows4.place(rely=0, relx=0.4, relwidth=0.2, relheight=0.1)
        #
        # rows5 = tk.Button(self.selectionFrame, text="5", command=lambda: self.changeRows(5))
        # rows5.place(rely=0, relx=0.7, relwidth=0.2, relheight=0.1)
        #
        # #creating 3 buttons to change grid size
        # self.rowButtons=[rows3, rows4, rows5]

        self.rowButtons=list(map(lambda x: tk.Button( self.selectionFrame,text=str(x),
                                                      command=lambda: self.changeSize(x)),range (3, 6)))
        for i in range (3):
            self.rowButtons[i].place(rely=0, relx=0.1+0.3*i, relwidth=0.2, relheight=0.1)

        self.menuFrame.place(anchor='n', rely=0.2, relx=0.5, relwidth=1, relheight=0.7)
        self.changeSize(3)

    def changeScreen(self, oldScreen, newScreen):
        oldScreen.place_forget()
        newScreen.place(anchor='n', rely=0.2, relx=0.5, relwidth=1, relheight=0.7)

    def changeSize(self, n):
        self.size=n
        for i in range (3):
            self.rowButtons[i]["bg"]="white"
        self.rowButtons[n-3]["bg"]="red"




    def newGame(self):
        self.gameFrame=tk.Frame(self.guiFrame,bg=GUI_COLOR)
        self.board = Board(self.size)

        self.gameButtons = list(map(lambda y: list(map(lambda x: tk.Button(self.gameFrame,
                                            command=lambda: self.gameButtonClicked(y,x)), range(self.size))), range(self.size)))
        for i in range(self.size):
            for j in range(self.size):
                self.gameButtons[i][j].place(rely=(1/self.size)*i, relx=(1/self.size)*j, relwidth=(1/self.size),
                                             relheight=(1/self.size))
        self.changeScreen(self.selectionFrame, self.gameFrame)

    def gameButtonClicked(self, row, col):
        self.board.changeTile(row, col)
        self.gameButtons[row][col]["text"]=self.board.getValue(row,col)
        if self.board.checkIfWin():
            self.stopTimer()
            self.board.swapPlayer()
            self.endOfGame("Wygrał " + self.board.player + "\n Powrót do menu głównego")
        if self.board.checkIfFull():
            self.endOfGame("Remis! \n Powrót do menu głównego")

    def StartTimer(self):
        self._start = 0.0
        self._time_passed = 0.0
        self._running = 0
        self.time_str = tk.StringVar()

        timer = tk.Label(self.guiFrame, textvariable=self.time_str, bg = GUI_COLOR, font = (20))
        self.setTime(self._time_passed)
        timer.pack()

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
            self._elapsedtime = time.time() - self._start
            self.setTime(self._time_passed)
            self._running = 0



    def endOfGame(self, text):
        for i in range(self.size):
            for j in range(self.size):
                self.gameButtons[i][j].config(command=lambda: None)

        returnButton = tk.Button(self.gameFrame, text=text, bg='#A4B691', command=lambda: self.backToMenu())
        returnButton.place(rely=0.2, relx=0.2, relwidth=0.6, relheight=0.3)

    def backToMenu(self):
        self.changeScreen(self.gameFrame, self.menuFrame)
        self.gameFrame.destroy()


    def processIncoming(self):
        while self.queue.qsize(  ):
            try:
                msg = self.queue.get(0)
                print(msg)
            except queue.Empty:
                pass



class ThreadedClient:
    """
    Launch the main part of the GUI and the worker thread. periodicCall and
    endApplication could reside in the GUI part, but putting them here
    means that you have all the thread controls in a single place.
    """

    def __init__ (self, master):
        """
        Start the GUI and the asynchronous threads. We are in the main
        (original) thread of the application, which will later be used by
        the GUI as well. We spawn a new thread for the worker (I/O).
        """
        self.master = master

        # Create the queue
        self.queue = queue.Queue(  )

        # Set up the GUI part
        self.gui = GuiPart(master, self.queue, self.endApplication)

        # Set up the thread to do asynchronous I/O
        # More threads can also be created and used, if necessary
        self.running = 1
        # self.thread1 = threading.Thread(target=self.workerThread1)
        # self.thread1.start(  )

        # Start the periodic call in the GUI to check if the queue contains
        # anything
        # self.periodicCall(  )

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        self.gui.processIncoming(  )
        if not self.running:
            # This is the brutal stop of the system. You may want to do
            # some cleanup before actually shutting it down.
            import sys
            sys.exit(1)
        self.master.after(200, self.periodicCall)

    def workerThread1(self):
        """
        This is where we handle the asynchronous I/O. For example, it may be
        a 'select(  )'. One important thing to remember is that the thread has
        to yield control pretty regularly, by select or otherwise.
        """
        while self.running:
            # To simulate asynchronous I/O, we create a random number at
            # random intervals. Replace the following two lines with the real
            # thing.
            time.sleep(rand.random(  ) * 1.5)
            # msg = rand.random(  )
            # self.queue.put(msg)

    def endApplication(self):
        self.running = 0


root=tk.Tk()

client= ThreadedClient(root)
root.mainloop()

# background_image = tk.PhotoImage(file='./hindus.png')
# background_label = tk.Label(root, image=background_image)
# background_label.place(relwidth=1, relheight=1)
#
# entry=tk.Entry(frame)
# entry.place(relwidth=0.65, relheight=1)