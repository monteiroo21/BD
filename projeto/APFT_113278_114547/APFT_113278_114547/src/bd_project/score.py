from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Score(NamedTuple):
    register_num: int
    edition: int
    price: float
    availability: int
    difficultyGrade: int
    music: str
    editor: str
    arranger: str
    type: str

class ScoreDetails(NamedTuple):
    register_num: int
    edition: int
    price: float
    availability: int
    difficultyGrade: int
    music: str
    editor: str
    arranger: str
    type: str
    instrumentation: dict[str, str]

class Instrumentation(NamedTuple):
    instrument: str
    quantity: int
    family: str
    role: str


def list_allScores() -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name, w.Fname + ' ' + w.Lname as WriterName, ar.type
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier
							LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
							LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
							LEFT OUTER JOIN Writer w ON a.id = w.id""")
            return [Score(*row) for row in cursor.fetchall()]
        

def search_score(query: str) -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name, w.Fname + ' ' + w.Lname as WriterName, ar.type
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier
							LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
							LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
							LEFT OUTER JOIN Writer w ON a.id = w.id
                            WHERE m.title LIKE ?""", ('%' + query + '%',))
            return [Score(*row) for row in cursor.fetchall()]


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

            
def get_score_by_id(register_num: int) -> Score:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name, w.Fname + ' ' + w.Lname as WriterName, ar.type
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier
							LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
							LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
							LEFT OUTER JOIN Writer w ON a.id = w.id
            WHERE s.register_num = ?
            """, (register_num,))
            row = cursor.fetchone()
            register_num, edition, price, availability, difficultyGrade, music, editor, arranger, type = row
            if row is None:
                return None
            return Score(register_num, edition, price, availability, difficultyGrade, music, editor, arranger, type)
        

def filter_scores_by_price() -> list[Score]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.register_num, s.edition, s.price, s.availability, 
                       s.difficultyGrade, m.title as music, e.name as editor, 
                       w.Fname + ' ' + w.Lname as WriterName, ar.type
                FROM Score s
                JOIN Music m ON s.musicId = m.music_id
                JOIN Editor e ON s.editorId = e.identifier
                JOIN arranges ar ON s.register_num = ar.score_register
                JOIN Arranger a ON ar.arranger_id = a.id
                JOIN Writer w ON a.id = w.id
                ORDER BY s.price ASC
            """)
            return [Score(*row) for row in cursor.fetchall()]
        

def list_arrangers() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT w.Fname + ' ' + w.Lname
                FROM Arranger a
                JOIN Writer w ON a.id = w.id
            """)
            return [row[0] for row in cursor.fetchall()]
        
def get_instrumentations_by_score_id(register_num: int) -> list[Instrumentation]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT instrument, quantity, family, role
                FROM Instrumentation
                WHERE scoreNum = ?
            """, (register_num,))
            return [Instrumentation(*row) for row in cursor.fetchall()]
        

def detail_score(register_num: int) -> ScoreDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Query para buscar informações detalhadas sobre o compositor
            cursor.execute("""
            SELECT s.register_num, s.edition, s.price, s.availability, 
                            s.difficultyGrade, m.title as music, e.name, w.Fname + ' ' + w.Lname as WriterName, ar.type
                            FROM Score s
                            JOIN Music m ON s.musicId = m.music_id
							JOIN Editor e ON s.editorId = e.identifier
							LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
							LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
							LEFT OUTER JOIN Writer w ON a.id = w.id
            WHERE s.register_num = ?
            """, (register_num,))
            
            row = cursor.fetchone()
            if row is None:
                return None  # Se nenhuma linha for retornada, o compositor não existe

            # Extrair informações básicas sobre o compositor
            score_info = row[:9]

            # Query para buscar as músicas associadas ao compositor
            cursor.execute("""
                SELECT instrument, quantity
                FROM Instrumentation
                WHERE scoreNum = ?
            """, (register_num,))
            
            instrumentation = {instrumentation[0]: instrumentation[1] for instrumentation in cursor.fetchall()}

            return ScoreDetails(*score_info, instrumentation)
        

def create_score(score: Score):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT identifier FROM Editor WHERE name = ?", (score.editor,))
            editor_id = cursor.fetchone()
            if editor_id is None:
                raise ValueError(f"Editor '{score.editor}' does not exist")
            editor_id = editor_id[0]

            cursor.execute("SELECT music_id FROM Music WHERE title = ?", (score.music,))
            music_id = cursor.fetchone()
            if music_id is None:
                raise ValueError(f"Music '{score.music}' does not exist")
            music_id = music_id[0]

            cursor.execute("SELECT id FROM Writer WHERE Fname + ' ' + Lname = ?", (score.arranger,))
            arranger_id = cursor.fetchone()
            if arranger_id is None:
                raise ValueError(f"Arranger '{score.arranger}' does not exist")
            arranger_id = arranger_id[0]

            try:
                cursor.execute("""
                    EXEC add_score @edition=?, @price=?, @availability=?, @difficultyGrade=?, @musicId=?, @editorId=?, @arrangerId=?, @type=?
                """, (score.edition, score.price, score.availability, score.difficultyGrade, music_id, editor_id, arranger_id, score.type))
                conn.commit()
            except Exception as e:
                print(f"Failed to create score: {e}")
                conn.rollback()

def edit_score(score: Score):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT register_num FROM Score WHERE register_num = ?", (score.register_num,))
            if cursor.fetchone() is None:
                raise ValueError(f"Score with register number '{score.register_num}' does not exist")

            cursor.execute("SELECT identifier FROM Editor WHERE name = ?", (score.editor,))
            editor_id = cursor.fetchone()
            if editor_id is None:
                raise ValueError(f"Editor '{score.editor}' does not exist")
            editor_id = editor_id[0]

            cursor.execute("SELECT music_id FROM Music WHERE title = ?", (score.music,))
            music_id = cursor.fetchone()
            if music_id is None:
                raise ValueError(f"Music '{score.music}' does not exist")
            music_id = music_id[0]

            cursor.execute("SELECT id FROM Writer WHERE Fname + ' ' + Lname = ?", (score.arranger,))
            arranger_id = cursor.fetchone()
            if arranger_id is None:
                raise ValueError(f"Arranger '{score.arranger}' does not exist")
            arranger_id = arranger_id[0]

            try:
                cursor.execute("""
                    EXEC edit_score @register_num=?, @new_edition=?, @new_price=?, @new_availability=?, @new_difficultyGrade=?, @new_music_id=?, @new_editor_id=?, @new_arranger_id=?, @type=?
                """, (score.register_num, score.edition, score.price, score.availability, score.difficultyGrade, music_id, editor_id, arranger_id, score.type))
                conn.commit()
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to edit score with register number {score.register_num}: {e}")
        
def add_instrumentation(instrument: str, quantity: int, family: str, role: str, register_num: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:

            try:
                cursor.execute("""
                INSERT INTO Instrumentation (instrument, quantity, family, role, scoreNum)
                VALUES (?, ?, ?, ?, ?)
                """,(instrument, quantity, family, role, register_num))
                conn.commit()
            except Exception as e:
                conn.rollback()
                raise ValueError(f"Failed to add instrumentation: {e}")
            finally:
                cursor.close()
                conn.close()