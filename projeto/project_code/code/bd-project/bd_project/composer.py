import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Composer (NamedTuple):
    id: int
    Fname:  str
    Lname:  str
    genre:  str
    birth_year: int
    death_year: int
    mus_genre:  str

def list_Composers() -> list[Composer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT Composer.id, Fname, Lname, genre, birthYear, deathYear, MusicalGenre.name FROM Composer
			JOIN Writer ON Composer.id=Writer.id
			JOIN MusicalGenre ON Writer.musGenre_id=MusicalGenre.id""")
            return [Composer(*row) for row in cursor.fetchall()]
        

def search_composer(query: str) -> list[Composer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT Composer.id, Fname, Lname, genre, birthYear, deathYear, MusicalGenre.name FROM Composer
			JOIN Writer ON Composer.id=Writer.id
			JOIN MusicalGenre ON Writer.musGenre_id=MusicalGenre.id
            WHERE Fname LIKE ? OR Lname LIKE ?""", ('%' + query + '%', '%' + query + '%'))
            return [Composer(*row) for row in cursor.fetchall()]
        

def create_composer(composer: Composer):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (composer.mus_genre,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{composer.mus_genre}' does not exist")
            genre_id = genre_id[0]
            cursor.execute("""
                EXEC add_composer @Fname=?, @Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
                        """, (composer.Fname, composer.Lname, composer.genre, composer.birth_year, composer.death_year, genre_id))
            conn.commit()


def list_genres() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM MusicalGenre")
            return [row[0] for row in cursor.fetchall()]

        