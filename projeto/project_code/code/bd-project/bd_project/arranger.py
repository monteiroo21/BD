import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Arranger (NamedTuple):   
    identifier: int
    fname:  str
    lname:  str
    birthYear:  int
    deathYear:  int
    name:   str


def list_arranger() -> list[Arranger]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT a.id, w.Fname, w.Lname, w.birthYear, w.deathYear, mg.name
                FROM Arranger AS a 
                JOIN Writer AS w ON a.id = w.id
                JOIN MusicalGenre as mg on w.musGenre_id = mg.id
                """)
            return [Arranger(*row) for row in cursor.fetchall()]


def search_arranger(query: str) -> list[Arranger]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT a.id, w.Fname, w.Lname, w.birthYear, w.deathYear, mg.name
                FROM Arranger AS a 
                JOIN Writer AS w ON a.id = w.id
                JOIN MusicalGenre as mg on w.musGenre_id = mg.id
                WHERE w.Fname LIKE ? OR w.Lname LIKE ?""", ('%' + query + '%', '%' + query + '%'))
            return [Arranger(*row) for row in cursor.fetchall()]