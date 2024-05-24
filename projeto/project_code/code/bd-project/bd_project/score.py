from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Score (NamedTuple):
    register_num: int
    edition: int
    price: float
    availability: int
    difficultyGrade: int
    music: str
    editor: str


def list_allScores() -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier""")
            return [Score(*row) for row in cursor.fetchall()]
        

def search_score(query: str) -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier
                            WHERE m.title LIKE ?""", ('%' + query + '%',))
            return [Score(*row) for row in cursor.fetchall()]
        

def create_score(score: Score):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT identifier FROM Editor WHERE name = ?", (score.editor,))
            editor_id = cursor.fetchone()
            if editor_id is None:
                raise ValueError(f"Editor '{score.editor}' does not exist")
            editor_id = editor_id[0]

            try:
                cursor.execute("SELECT music_id FROM Music WHERE title = ?", (score.music,))
                music_id = cursor.fetchone()
                if editor_id is None:
                    raise ValueError(f"Music '{score.music}' does not exist")
                music_id = music_id[0]
                cursor.execute("""
                    EXEC add_score @edition=?, @price=?, @availability=?, @difficultyGrade=?, @musicId=?, @editorId=?
                            """, (score.edition, score.price, score.availability, score.difficultyGrade, music_id, editor_id))
                conn.commit()
            except Exception as e:
                print(f"Failed to create score: {e}")
                conn.rollback()


def list_editors() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM Editor")
            return [row[0] for row in cursor.fetchall()]
        

def list_musics() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT title FROM Music")
            return [row[0] for row in cursor.fetchall()]
        

def delete_score(register_num: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the score exists
            cursor.execute("SELECT register_num FROM Score WHERE register_num = ?", (register_num,))
            if cursor.fetchone() is None:
                raise ValueError(f"Score with register number '{register_num}' does not exist")

            # Delete the score entry from the Score table
            try:
                cursor.execute("DELETE FROM Score WHERE register_num = ?", (register_num,))
                conn.commit()
                print(f"Score with register number {register_num} deleted successfully.")
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete score with register number {register_num}: {e}")