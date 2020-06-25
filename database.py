from enum import Enum
import sqlite3
class Wynik(Enum):
    PRZEGRANA: int = 1
    WYGRANA: int = 2
    REMIS: int = 3


class Database:
    def __init__(self):
        # utworzenie połączenia z bazą przechowywaną na dysku
        self.con = sqlite3.connect('test.db')
        # dostęp do kolumn przez indeksy i przez nazwy
        self.con.row_factory = sqlite3.Row
        # utworzenie obiektu kursora
        self.cur = self.con.cursor()
        self.createTable()
        self.dodajUzytkownika("Kasia")
        self.czytajDane()
        self.zaaktualizujStatystyki("Kasia", Wynik.PRZEGRANA)
        self.czytajDane()



    # tworzenie tabeli
    def createTable(self):
        self.cur.executescript("""
        CREATE TABLE IF NOT EXISTS uzytkownik (
            nazwaUzytkownika varchar(10) PRIMARY KEY,
            wygrane INTEGER,
            przegrane INTEGER,
            remisy INTEGER,
            liczbaGier INTEGER
             )""")


    # wyświetl dane
    def czytajDane(self):
        self.cur.execute('SELECT * FROM uzytkownik')
        data = self.cur.fetchall()
        for row in data:
            print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} ")
        return data


    def sprawdzUzytkownika(self, nazwaUzytkownika)-> bool :
        data = self.cur.fetchall()
        self.cur.execute('SELECT nazwaUzytkownika FROM uzytkownik WHERE nazwaUzytkownika = ?', (nazwaUzytkownika,))
        data = self.cur.fetchall()
        if not data:
            return False
        else:
            return True

    def dodajUzytkownika(self,nazwaUzytkownika):
        if self.sprawdzUzytkownika(nazwaUzytkownika):
            return False
        else:
            self.cur.execute("INSERT INTO uzytkownik(nazwaUzytkownika, wygrane, przegrane, remisy, liczbaGier) VALUES(?,?,?,?,?)",(nazwaUzytkownika,0,0,0,0))
            self.con.commit()
            return True

    def zaaktualizujStatystyki(self,nazwaUzytkownika, wynik:Wynik):
        self.cur.execute('SELECT * FROM uzytkownik WHERE nazwaUzytkownika = ?', (nazwaUzytkownika,))
        data = self.cur.fetchone()
        if(not data):
            return False
        liczbaGier=data[4]
        self.cur.execute('UPDATE uzytkownik SET liczbaGier=? WHERE nazwaUzytkownika=?',
                         (liczbaGier + 1, nazwaUzytkownika))
        if wynik == Wynik.PRZEGRANA:
            liczbaPrzegranych = data[2]
            self.cur.execute('UPDATE uzytkownik SET przegrane=? WHERE nazwaUzytkownika=?', (liczbaPrzegranych+1, nazwaUzytkownika))
        elif wynik == Wynik.WYGRANA:
            liczbaWygranych = data[1]
            cur.execute('UPDATE uzytkownik SET wygrane=? WHERE nazwaUzytkownika=?', (liczbaWygranych+1, nazwaUzytkownika))
        elif wynik == Wynik.REMIS:
            liczbaRemisow = data[3]
            cur.execute('UPDATE uzytkownik SET remisy=? WHERE nazwaUzytkownika=?', (liczbaRemisow+1, nazwaUzytkownika))

        self.con.commit()
        return True









