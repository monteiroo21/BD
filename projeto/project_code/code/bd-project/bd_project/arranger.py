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

class ArrangerDetails (NamedTuple):
    identifier: int
    fname:  str
    lname:  str
    genre:  str
    birthYear:  int
    deathYear:  int
    name:   str
    musics: dict[str, str]


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
            
            try:
                cursor.execute("""
                    EXEC add_arranger @Fname=?, @Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
                            """, (arranger.fname, arranger.lname, arranger.genre, arranger.birthYear, arranger.deathYear, genre_id))
                conn.commit()
            except Exception as e:
                print(f"Failed to create arranger: {e}")
                conn.rollback()

def detail_arranger(arranger_id: int) -> ArrangerDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Query para buscar informações detalhadas sobre o compositor
            cursor.execute("""
            SELECT w.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, g.name AS mus_genre
                FROM Writer w
                JOIN Arranger a ON w.id = a.id
                JOIN MusicalGenre g ON w.musGenre_id = g.id
                WHERE w.id = ?
            """, (arranger_id,))
            
            row = cursor.fetchone()
            if row is None:
                return None  # Se nenhuma linha for retornada, o compositor não existe

            # Extrair informações básicas sobre o compositor
            arranger_info = row[:7]

            # Query para buscar as músicas associadas ao compositor
            cursor.execute("""
                SELECT m.title, mg.name AS music_genre
                FROM arranges ar
                JOIN Score s ON ar.score_register = s.register_num
				JOIN Music m ON s.musicId = m.music_id
                JOIN MusicalGenre mg ON m.musGenre_id = mg.id
                WHERE ar.arranger_id = ?
            """, (arranger_id,))
            
            musics = {music[0]: music[1] for music in cursor.fetchall()}

            return ArrangerDetails(*arranger_info, musics)    


def list_genres() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM MusicalGenre")
            return [row[0] for row in cursor.fetchall()]
        
        
def edit_arranger(arranger: Arranger, old_fname: str, old_lname: str):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Get the genre ID
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (arranger.name,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{arranger.name}' does not exist")
            genre_id = genre_id[0]
            
            # Execute the stored procedure to edit the arranger
            cursor.execute("""
                EXEC edit_arranger @old_Fname=?, @old_Lname=?, @new_Fname=?, @new_Lname=?, @genre=?, @birthYear=?, @deathYear=?, @musGenre_id=?
            """, (old_fname, old_lname, arranger.fname, arranger.lname, arranger.genre, arranger.birthYear, arranger.deathYear, genre_id))
            
            # Commit the transaction
            conn.commit()


def get_arranger_by_id(arranger_id: int) -> Arranger:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT w.id, w.Fname, w.Lname, w.genre, w.birthYear, w.deathYear, g.name AS mus_genre
                FROM Writer w
                JOIN Arranger a ON w.id = a.id
                JOIN MusicalGenre g ON w.musGenre_id = g.id
                WHERE w.id = ?
            """, (arranger_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Arranger(*row)
        
        
def delete_arranger(arranger_id: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the arranger exists
            cursor.execute("SELECT id FROM Arranger WHERE id = ?", (arranger_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"Arranger with ID '{arranger_id}' does not exist")

            # Delete the arranger entry from the Arranger table
            try:
                cursor.execute("DELETE FROM Arranger WHERE id = ?", (arranger_id,))
                conn.commit()
                print(f"Arranger with ID {arranger_id} deleted successfully.")
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete arranger with ID {arranger_id}: {e}")