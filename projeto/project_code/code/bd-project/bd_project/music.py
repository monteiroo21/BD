import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Music (NamedTuple):
    music_id: int
    title: str
    year: int
    genre: int


def list_allMusic() -> list[Music]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT music_id, title, [year], musGenre_id FROM Music")
            return [Music(*row) for row in cursor.fetchall()]
        

def search_music(query: str) -> list[Music]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT music_id, title, [year], musGenre_id FROM Music WHERE title LIKE ?", ('%' + query + '%',))
            return [Music(*row) for row in cursor.fetchall()]