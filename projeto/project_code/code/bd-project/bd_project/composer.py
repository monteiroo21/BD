import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Composer (NamedTuple):
    id: int
    Fname:  str
    Lname:  str
    birth_year: int
    death_year: int
    mus_genre:  str

def list_Composers() -> list[Composer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT Composer.id, Fname, Lname, birthYear, deathYear, MusicalGenre.name FROM Composer
			JOIN Writer ON Composer.id=Writer.id
			JOIN MusicalGenre ON Writer.musGenre_id=MusicalGenre.id""")
            return [Composer(*row) for row in cursor.fetchall()]

        