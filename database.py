from enum import Enum
import sqlite3
class Result(Enum):
    DEFEAT: int = 1
    WIN: int = 2
    TIE: int = 3


class Database:
    def __init__(self):
        # utworzenie połączenia z bazą przechowywaną na dysku
        self.con = sqlite3.connect('test.db')
        # dostęp do kolumn przez indeksy i przez nazwy
        self.con.row_factory = sqlite3.Row
        # utworzenie obiektu kursora
        self.cur = self.con.cursor()
        self.createTable()
        self.addUser("Kasia")
        self.readData()



    # tworzenie tabeli
    def createTable(self):
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS uzytkownik (
            userName varchar(10) PRIMARY KEY,
            wygrane INTEGER,
            przegrane INTEGER,
            remisy INTEGER,
            gameNumber INTEGER
             )""")


    # wyświetl dane
    def readData(self):
        self.cur.execute('SELECT * FROM uzytkownik')
        data = self.cur.fetchall()
        for row in data:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} ")
        return data


    def checkUser(self, userName:str)-> bool :
        data = self.cur.fetchall()
        self.cur.execute('SELECT userName FROM uzytkownik WHERE userName = ?', (userName,))
        data = self.cur.fetchall()
        if not data:
            return False
        else:
            return True

    def addUser(self,userName:str)-> bool:
        if self.checkUser(userName):
            return False
        else:
            self.cur.execute("INSERT INTO uzytkownik(userName, wygrane, przegrane, remisy, gameNumber) VALUES(?,?,?,?,?)",(userName,0,0,0,0))
            self.con.commit()
            return True

    def updateStatistics(self,userName:str, result:Result)-> bool:
        self.cur.execute('SELECT * FROM uzytkownik WHERE userName = ?', (userName,))
        data = self.cur.fetchone()
        if(not data):
            return False
        gameNumber=data[4]
        self.cur.execute('UPDATE uzytkownik SET gameNumber=? WHERE userName=?',
                         (gameNumber + 1, userName))
        if result == Result.DEFEAT:
            defeatNumber = data[2]
            self.cur.execute('UPDATE uzytkownik SET przegrane=? WHERE userName=?', (defeatNumber+1, userName))
        elif result == Result.WIN:
            winNumber = data[1]
            cur.execute('UPDATE uzytkownik SET wygrane=? WHERE userName=?', (winNumber+1, userName))
        elif result == Result.TIE:
            tieNumber = data[3]
            cur.execute('UPDATE uzytkownik SET remisy=? WHERE userName=?', (tieNumber+1, userName))

        self.con.commit()
        return True









