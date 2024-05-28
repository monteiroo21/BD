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


class ComposerDetails(NamedTuple):
    id: int
    Fname:  str
    Lname:  str
    genre:  str
    birth_year: int
    death_year: int
    mus_genre:  str
    musics: dict[str, str]


def list_Composers() -> list[Composer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT Composer.id, Fname, Lname, genre, birthYear, deathYear, MusicalGenre.name FROM Composer
			LEFT OUTER JOIN Writer ON Composer.id=Writer.id
			JOIN MusicalGenre ON Writer.musGenre_id=MusicalGenre.id""")
            return [Composer(*row) for row in cursor.fetchall()]
        

def search_composer(query: str) -> list[Composer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT Composer.id, Fname, Lname, genre, birthYear, deathYear, MusicalGenre.name FROM Composer
			LEFT OUTER JOIN Writer ON Composer.id=Writer.id
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

            try:
                cursor.execute("""
                    EXEC add_composer @Fname=?, @Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
                            """, (composer.Fname, composer.Lname, composer.genre, composer.birth_year, composer.death_year, genre_id))
                conn.commit()
            except Exception as e:
                print(f"Failed to create composer: {e}")
                conn.rollback()


def detail_composer(composer_id: int) -> ComposerDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Query para buscar informações detalhadas sobre o compositor
            cursor.execute("""
                SELECT w.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, g.name AS mus_genre
                FROM Writer w
                LEFT OUTER JOIN Composer c ON w.id = c.id
                JOIN MusicalGenre g ON w.musGenre_id = g.id
                WHERE w.id = ?
            """, (composer_id,))
            
            row = cursor.fetchone()
            if row is None:
                return None  # Se nenhuma linha for retornada, o compositor não existe

            # Extrair informações básicas sobre o compositor
            composer_info = row[:7]

            # Query para buscar as músicas associadas ao compositor
            cursor.execute("""
                SELECT m.title, mg.name AS music_genre
                FROM writes wr
                JOIN Music m ON wr.music_id = m.music_id
                JOIN MusicalGenre mg ON m.musGenre_id = mg.id
                WHERE wr.composer_id = ?
            """, (composer_id,))
            
            musics = {music[0]: music[1] for music in cursor.fetchall()}

            return ComposerDetails(*composer_info, musics)


def list_genres() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM MusicalGenre")
            return [row[0] for row in cursor.fetchall()]
        

def delete_composer(composer_id: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the composer exists
            cursor.execute("SELECT id FROM Composer WHERE id = ?", (composer_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"Composer with ID '{composer_id}' does not exist")

            # Delete the composer entry from the Composer table
            try:
                cursor.execute("DELETE FROM Composer WHERE id = ?", (composer_id,))
                conn.commit()
                print(f"Composer with ID {composer_id} deleted successfully.")
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete composer with ID {composer_id}: {e}")
            

def edit_composer(composer: Composer, old_fname: str, old_lname: str):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Get the genre ID
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (composer.mus_genre,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{composer.mus_genre}' does not exist")
            genre_id = genre_id[0]
            
            # Execute the stored procedure to edit the composer
            cursor.execute("""
                EXEC edit_composer @old_Fname=?, @old_Lname=?, @new_Fname=?, @new_Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
            """, (old_fname, old_lname, composer.Fname, composer.Lname, composer.genre, composer.birth_year, composer.death_year, genre_id))
            
            # Commit the transaction
            conn.commit()

def get_composer_by_id(composer_id: int) -> Composer:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT w.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, g.name AS mus_genre
                FROM Writer w
                LEFT OUTER JOIN Composer c ON w.id = c.id
                JOIN MusicalGenre g ON w.musGenre_id = g.id
                WHERE w.id = ?
            """, (composer_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Composer(*row)

        