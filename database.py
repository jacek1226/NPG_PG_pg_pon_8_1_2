from enum import Enum
from typing import *
import sqlite3
class Result(Enum):
    """Enumereates with differents type of game results"""
    DEFEAT: int = 1
    WIN: int = 2
    TIE: int = 3


class Database:
    """Create basic interface for communication with database, storing games' statistics"""
    def __init__(self):
        try:
            # create connection with database on disc
            self.con = sqlite3.connect('test.db')
            # access to columns by indeks and name
            self.con.row_factory = sqlite3.Row
            # create cursor object
            self.cur = self.con.cursor()
            """Creates the default table if there isn't any"""
            self.createTable()
            """Creates default players if they aren't any"""
            self.addUser("Statistics 1")
            self.addUser("Statistics 2")
            self.connection : bool = True
            self.columnNames : Tuple(str, str, str, str, str)=("nazwa", "wygrane", "przegrane", "remisy", "liczba gier")
        except:
            print("blad w polaczeniu z baza danych!")
            self.connection : bool = False





    def createTable(self)-> None:
        """Creates table with custom data if there isn't any"""

        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS uzytkownik (
            userName varchar(10) PRIMARY KEY,
            wygrane INTEGER,
            przegrane INTEGER,
            remisy INTEGER,
            gameNumber INTEGER
             )""")



    def readData(self)->List[sqlite3.Row]:
        """ Select all data from the database

        RETURNS
        --------
        list
            a list of database rows representing users data
        """
        self.cur.execute('SELECT * FROM uzytkownik')
        data : List[sqlite3.Row] = self.cur.fetchall()
        return data


    def checkUser(self, userName:str)-> bool :
        """ Check existence of a user

        Parameter
        --------
        userName : str
            Name of user

        Return
        --------
        bool
            True if user exist or false if not exist
        """
        self.cur.execute('SELECT userName FROM uzytkownik WHERE userName = ?', (userName,))
        data : List[sqlite3.Row]= self.cur.fetchall()
        if not data:
            return False
        else:
            return True


    def addUser(self,userName:str)-> bool:
        """ Adds new user with empty result

                Parameter
                --------
                userName : str
                    Name of user

                Return
                --------
                bool
                    False if user exist or true if not exist
        """

        if self.checkUser(userName):
            return False
        else:
            self.cur.execute("INSERT INTO uzytkownik(userName, wygrane, przegrane, remisy, gameNumber) VALUES(?,?,?,?,?)",(userName,0,0,0,0))
            self.con.commit()
            return True

    def updateStatistics(self,userName:str, result:Result )-> bool:
        """ Updates result of specified user

                       Parameter
                       --------
                       userName : str
                           Name of user
                       Result
                            game result

                       Return
                       --------
                       bool
                           True if user exist or false if not exist
        """
        self.cur.execute('SELECT * FROM uzytkownik WHERE userName = ?', (userName,))
        data = self.cur.fetchone()
        if(not data):
            return False
        gameNumber : int =data[4]
        self.cur.execute('UPDATE uzytkownik SET gameNumber=? WHERE userName=?',
                         (gameNumber + 1, userName))
        if result == Result.DEFEAT:
            defeatNumber : int = data[2]
            self.cur.execute('UPDATE uzytkownik SET przegrane=? WHERE userName=?', (defeatNumber+1, userName))
        elif result == Result.WIN:
            winNumber : int = data[1]
            self.cur.execute('UPDATE uzytkownik SET wygrane=? WHERE userName=?', (winNumber+1, userName))
        elif result == Result.TIE:
            tieNumber : int = data[3]
            self.cur.execute('UPDATE uzytkownik SET remisy=? WHERE userName=?', (tieNumber+1, userName))

        self.con.commit()
        return True









