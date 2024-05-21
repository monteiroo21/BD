import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Music (NamedTuple):
    music_id: int
    title: str
    year: int
    genre_name: str
    composer_fname: str
    composer_lname: str


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
        

def create(music: Music):
    id_str = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))

    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO Writer (Fname, Lname)
                VALUES (?, ?);
                INSERT INTO Composer (id)
                VALUES (?);
                IF NOT EXISTS (SELECT 1 FROM MusicalGenre WHERE name = ?)
                BEGIN
                    INSERT INTO MusicalGenre (name)
                    VALUES (?);
                END
                SELECT id FROM MusicalGenre WHERE name = ?;
                INSERT INTO Music (music_id, title, [year], musGenre_id)
                VALUES (?, ?, ?, id);
                INSERT INTO writes (music_id, composer_id)
                VALUES (?, ?);
            """,
            id_str,
            music.music_id,
            music.title,
            music.year,
            music.genre_name,
            music.composer_fname,
            music.composer_lname,
        )

        cursor.commit()


def delete(c_id: str):
    with create_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE Customers WHERE CustomerID = ?;", c_id)
            cursor.commit()
        except IntegrityError as ex:
            if ex.args[0] == "23000":
                raise Exception(f"Customer {c_id} cannot be deleted. Probably has orders.") from ex