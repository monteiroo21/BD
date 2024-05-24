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


# class MusicDetails(NamedTuple):
#     music_id: int
#     title: str
#     year: int
#     genre_name: str
#     composer_fname: str
#     composer_lname: str
#     scores: list[str]

class MusicDetails(NamedTuple):
    music_id: int
    title: str
    year: int
    genre_name: str
    composer_fname: str
    composer_lname: str
    scores: dict[str, str]


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

            try:
                cursor.execute("""
                    EXEC insert_music @title=?, @year=?, @musGenre_id=?, @fname=?, @lname=?
                            """, (music.title, music.year, genre_id, music.composer_fname, music.composer_lname))
                conn.commit()
            except Exception as e:
                print(f"Failed to insert music: {e}")
                conn.rollback()


def get_music_by_id(music_id: int) -> Music:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.title, m.year, g.name AS genre_name, w.Fname, w.Lname
                FROM Music m
                JOIN MusicalGenre g ON m.musGenre_id = g.id
                JOIN Writes wr ON m.music_id = wr.music_id
                JOIN Writer w ON wr.composer_id = w.id
                WHERE m.music_id = ?
            """, (music_id,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            title, year, genre_name, composer_fname, composer_lname = row
            return Music(music_id, title, year, genre_name, composer_fname, composer_lname)


def edit_music(music: Music):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Get the genre ID
            cursor.execute("SELECT id FROM MusicalGenre WHERE name = ?", (music.genre_name,))
            genre_id = cursor.fetchone()
            if genre_id is None:
                raise ValueError(f"Genre '{music.genre_name}' does not exist")
            genre_id = genre_id[0]
            
            # Execute the stored procedure to edit the music
            cursor.execute("""
                EXEC edit_music @music_id=?, @title=?, @year=?, @musGenre_id=?, @fname=?, @lname=?
            """, (music.music_id, music.title, music.year, genre_id, music.composer_fname, music.composer_lname))
            
            # Commit the transaction
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


# def detail_music(music_id: int) -> MusicDetails:
#     with create_connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute("""
#                 SELECT m.music_id, m.title, m.[year], g.[name] AS genre_name, wr.Fname, wr.Lname,
#                        s.register_num, s.edition, s.availability, s.difficultyGrade, s.price, e.name AS editor_name
#                 FROM Music AS m
#                 JOIN MusicalGenre AS g ON m.musGenre_id = g.id
#                 JOIN writes AS mw ON m.music_id = mw.music_id
#                 JOIN Composer AS c ON mw.composer_id = c.id
#                 JOIN Writer AS wr ON c.id = wr.id
#                 LEFT JOIN Score AS s ON m.music_id = s.musicId
#                 LEFT JOIN Editor AS e ON s.editorId = e.identifier
#                 WHERE m.music_id = ?
#             """, (music_id,))

#             rows = cursor.fetchall()
#             if not rows:
#                 raise ValueError(f"Music with ID {music_id} not found")

#             music_info = rows[0][:6]
#             scores = [{
#                 "register_num": score[6],
#                 "edition": score[7],
#                 "availability": score[8],
#                 "difficultyGrade": score[9],
#                 "price": score[10],
#                 "editor_name": score[11]
#             } for score in rows if score[6]]
            
#             return MusicDetails(*music_info, scores)


def detail_music(music_id: int) -> MusicDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT m.music_id, m.title, m.[year], g.[name] AS genre_name, wr.Fname, wr.Lname,
                       s.register_num, s.edition, s.availability, s.difficultyGrade, s.price, e.name AS editor_name,
                       arw.Fname AS arranger_fname, arw.Lname AS arranger_lname
                FROM Music AS m
                JOIN MusicalGenre AS g ON m.musGenre_id = g.id
                JOIN writes AS mw ON m.music_id = mw.music_id
                JOIN Composer AS c ON mw.composer_id = c.id
                JOIN Writer AS wr ON c.id = wr.id
                LEFT JOIN Score AS s ON m.music_id = s.musicId
                LEFT JOIN Editor AS e ON s.editorId = e.identifier
                LEFT JOIN arranges AS a ON s.register_num = a.score_register
                LEFT JOIN Arranger AS ar ON a.arranger_id = ar.id
                LEFT JOIN Writer AS arw ON ar.id = arw.id
                WHERE m.music_id = ?
            """, (music_id,))

            rows = cursor.fetchall()
            if not rows:
                raise ValueError(f"Music with ID {music_id} not found")

            music_info = rows[0][:6]
            scores = [{
                "register_num": score[6],
                "edition": score[7],
                "availability": score[8],
                "difficultyGrade": score[9],
                "price": score[10],
                "editor_name": score[11],
                "arranger_name": f"{score[12]} {score[13]}" if score[12] and score[13] else None
            } for score in rows if score[6]]
            
            return MusicDetails(*music_info, scores)
