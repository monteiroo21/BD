import random
import string
from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Music(NamedTuple):
    music_id: int
    title: str
    year: int
    genre_name: str
    composer_fname: str
    composer_lname: str


class MusicDetails(NamedTuple):
    music_id: int
    title: str
    year: int
    genre_name: str
    composer_fname: str
    composer_lname: str
    scores: list[str]


def list_allMusic() -> list[Music]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT m.music_id, m.title, m.[year], g.[name] AS genre_name, wr.Fname, wr.Lname
                FROM Music AS m
                JOIN MusicalGenre AS g ON m.musGenre_id = g.id
                JOIN writes AS mw ON m.music_id = mw.music_id
                JOIN Composer AS c ON mw.composer_id = c.id
                JOIN Writer AS wr ON c.id = wr.id
                """)
            return [Music(*row) for row in cursor.fetchall()]

def search_music(query: str) -> list[Music]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT m.music_id, m.title, m.[year], g.[name] AS genre_name, wr.Fname, wr.Lname
                FROM Music AS m
                JOIN MusicalGenre AS g ON m.musGenre_id = g.id
                JOIN writes AS mw ON m.music_id = mw.music_id
                JOIN Composer AS c ON mw.composer_id = c.id
                JOIN Writer AS wr ON c.id = wr.id
                WHERE m.title LIKE ?""", ('%' + query + '%',))
            return [Music(*row) for row in cursor.fetchall()]
        
def create_music(music: Music):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (music.genre_name,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{music.genre_name}' does not exist")
            genre_id = genre_id[0]
            cursor.execute("""
                EXEC insert_music @title=?, @year=?, @musGenre_id=?, @fname=?, @lname=?
                        """, (music.title, music.year, genre_id, music.composer_fname, music.composer_lname))
            conn.commit()


def list_genres() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM MusicalGenre")
            return [row[0] for row in cursor.fetchall()]
        

def delete_music(music_id: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM writes WHERE music_id = ?", (music_id,))
                cursor.execute("DELETE FROM Music WHERE music_id = ?", (music_id,))
                conn.commit()
                print(f"Music with ID {music_id} deleted successfully.")
            except IntegrityError as e:
                print(f"Failed to delete music with ID {music_id}: {e}")


def detail_music(music_id: int) -> MusicDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.music_id, m.title, m.[year], g.[name] AS genre_name, wr.Fname, wr.Lname, s.edition, e.name
                FROM Music AS m
                JOIN MusicalGenre AS g ON m.musGenre_id = g.id
                JOIN writes AS mw ON m.music_id = mw.music_id
                JOIN Composer AS c ON mw.composer_id = c.id
                JOIN Writer AS wr ON c.id = wr.id
                LEFT JOIN Score AS s ON m.music_id = s.music_id
                LEFT JOIN Editor AS e ON s.editor_id = e.editor_id
                WHERE m.music_id = ?
            """, (music_id,))
            rows = cursor.fetchall()
            if not rows:
                raise ValueError(f"Music with ID {music_id} not found")
            # Primeira linha contém os detalhes básicos da música
            music_info = rows[0][:6]  # Excluindo os dados dos scores
            scores = [score[6:] for score in rows if score[6]]  # Ignorando os scores vazios
            return MusicDetails(*music_info, scores)
