from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Score (NamedTuple):
    register_num: int
    edition: int
    price: float
    availability: int
    difficultyGrade: int
    musicId: int
    editorId: int
    music: str


def list_allScores() -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, s.musicId, s.editorId, m.title as music
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id""")
            return [Score(*row) for row in cursor.fetchall()]
        

def search_score(query: str) -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, s.musicId, s.editorId, m.title as music
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
                            WHERE m.title LIKE ?""", ('%' + query + '%',))
            return [Score(*row) for row in cursor.fetchall()]