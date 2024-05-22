import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Arranger (NamedTuple):   
    identifier: int
    fname:  str
    lname:  str
    genre:  str
    birthYear:  int
    deathYear:  int
    name:   str


def list_arranger() -> list[Arranger]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT a.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, mg.name
                FROM Arranger AS a 
                JOIN Writer AS w ON a.id = w.id
                JOIN MusicalGenre as mg on w.musGenre_id = mg.id
                """)
            return [Arranger(*row) for row in cursor.fetchall()]


def search_arranger(query: str) -> list[Arranger]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT a.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, mg.name
                FROM Arranger AS a 
                JOIN Writer AS w ON a.id = w.id
                JOIN MusicalGenre as mg on w.musGenre_id = mg.id
                WHERE w.Fname LIKE ? OR w.Lname LIKE ?""", ('%' + query + '%', '%' + query + '%'))
            return [Arranger(*row) for row in cursor.fetchall()]
        
def create_arranger(arranger: Arranger):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (arranger.name,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{arranger.name}' does not exist")
            genre_id = genre_id[0]
            cursor.execute("""
                EXEC add_arranger @Fname=?, @Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
                        """, (arranger.fname, arranger.lname, arranger.genre, arranger.birthYear, arranger.deathYear, genre_id))
            conn.commit()


def list_genres() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM MusicalGenre")
            return [row[0] for row in cursor.fetchall()]