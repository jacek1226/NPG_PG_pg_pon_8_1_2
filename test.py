#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#cur.fetchall - pobierasz z bazy danych
#con.commit - wysyłasz do bazy danych
from enum import Enum
import sqlite3
class Wynik(Enum):
    przegrana = 1
    wygrana = 2
    remis = 3

# utworzenie połączenia z bazą przechowywaną na dysku
con = sqlite3.connect('test.db')

# dostęp do kolumn przez indeksy i przez nazwy
con.row_factory = sqlite3.Row

# utworzenie obiektu kursora
cur = con.cursor()

# tworzenie tabeli
def create_table():
    global cur
    cur.executescript("""
    DROP TABLE IF EXISTS uzytkownik;
    CREATE TABLE IF NOT EXISTS uzytkownik (
        id INTEGER PRIMARY KEY ASC AUTOINCREMENT,
        nazwa_uzytkownika varchar(10),
        wygrane INTEGER,
        przegrane INTEGER,
        remisy INTEGER,
        il_gier INTEGER
         )""")
create_table()
uzytkownicy = ()

# dodawanie danych do bazych

cur.executemany("INSERT INTO uzytkownik VALUES(?,?,?,?,?,?)",uzytkownicy)

uzytkownicy = (
    ("pawel",1,2,3,6),
)


cur.executemany("INSERT INTO uzytkownik(nazwa_uzytkownika, wygrane, przegrane, remisy, il_gier) VALUES(?,?,?,?,?)",uzytkownicy)


con.commit()
cur.execute('SELECT * FROM uzytkownik')

rows = cur.fetchall()

# wyświetl dane
def czytajdane():

    for row in rows:
        print(f"{row[0]} {row[1]} {row[2]} {row[3]} {row[4]} {row[5]} ")

czytajdane()
con.close()

def sprawdz_uzytkownika(nazwa_uzytkownika)-> bool :
    data = cur.fetchall()  # czyszczcenie danych
    cur.execute('SELECT nazwa_uzytkownika FROM uzytkownik WHERE nazwa_uzytkownika = ?', ('Pawel',))  # sql znajdz wszysstkich uzytkownikow o takim imieniu
    data = cur.fetchall()  # przypisawanie wszystkich uzytkownikow do zmiennej data
    if not data:  # sprawdzasz czy data nie jest pusta
        return False
    else:
        return True

def dodaj_uzytkownika(nazwa_uzytkownika):
    if sprawdz_uzytkownika(nazwa_uzytkownika):
        raise NameError
    else:
        cur.execute("INSERT INTO uzytkownik(nazwa_uzytkownika, wygrane, przegrane, remisy, il_gier) VALUES(?,?,?,?,?)",(nazwa_uzytkownika,0,0,0,0))
        con.commit()
        return

def zaaktualizuj_statystyki(nazwa_uzytkownika, wynik:Wynik):
    cur.execute('SELECT nazwa_uzytkownika FROM uzytkownik WHERE nazwa_uzytkownika = ?', ('Pawel',))
    if wynik == 1:
        przegrane = cur.fetchone()[0]
        cur.execute('UPDATE uzytkownik SET przegrane=? WHERE nazwa_uzytkownika=?', (przegrane, 1))
    elif wynik == 2:
        wygrane = cur.fetchone()[0]
        cur.execute('UPDATE uzytkownik SET wygrane=? WHERE nazwa_uzytkownika=?', (wygrane, 2))
    elif wynik == 3:
        remisy = cur.fetchone()[0]
        cur.execute('UPDATE uzytkownik SET remisy=? WHERE nazwa_uzytkownika=?', (remisy, 3))


def pobierz_dane():

    cur.execute(
        """
        SELECT uzytkownik.nazwa_uzytkownika, wygrane, przegrane, remisy, il_gier FROM uzytkownik
        """)
    uzytkownik = cur.fetchall()
    for row in rows:
        print()
    print()


pobierz_dane()









