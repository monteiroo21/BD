import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Editor (NamedTuple):
    name: str
    identifier: int
    location: str

class EditorDetails (NamedTuple):
    name: str
    identifier: int
    location: str
    warehouses: dict[str, str]


def list_editor() -> list[Editor]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT name, identifier, location
                           FROM Editor
                """)
            return [Editor(*row) for row in cursor.fetchall()]


def search_editor(query: str) -> list[Editor]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT name, identifier, location
                            FROM Editor
                WHERE name LIKE ?""", ('%' + query + '%',))
            return [Editor(*row) for row in cursor.fetchall()]
        

def create_editor(editor: Editor):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                    EXEC add_editor @name=?, @location=?
                            """, (editor.name, editor.location))
                conn.commit()
            except Exception as e:
                print(f"Failed to create editor: {e}")
                conn.rollback()

def detail_editor(editor_id: int) -> EditorDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Query para buscar informações detalhadas sobre o compositor
            cursor.execute("""
                SELECT name, identifier, location
                FROM Editor
                WHERE identifier = ?
            """, (editor_id,))
            
            row = cursor.fetchone()
            if row is None:
                return None  # Se nenhuma linha for retornada, o compositor não existe

            # Extrair informações básicas sobre o compositor
            editor_info = row[:3]

            # Query para buscar as músicas associadas ao compositor
            cursor.execute("""
            SELECT w.name, wl.warehouse_location FROM Editor as e
                    LEFT OUTER JOIN Warehouse as w ON e.identifier = w.editorId
                    JOIN warehouse_location as wl ON w.id = wl.warehouse_id
                    WHERE e.identifier = ?
            """, (editor_id,))
            
            musics = {music[0]: music[1] for music in cursor.fetchall()}

            return EditorDetails(*editor_info, musics)


def delete_editor(editor_id: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the editor exists
            cursor.execute("SELECT identifier FROM Editor WHERE identifier = ?", (editor_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"Editor with ID '{editor_id}' does not exist")

            # Delete the editor entry from the Editor table
            try:
                cursor.execute("DELETE FROM Editor WHERE identifier = ?", (editor_id,))
                conn.commit()
                print(f"Editor with ID {editor_id} deleted successfully.")
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete editor with ID {editor_id}: {e}")
            

def edit_editor(old_name: str, new_name: str, location: str):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                EXEC edit_editor @old_name=?, @new_name=?, @location=?
            """, (old_name, new_name, location))
            conn.commit()


def get_editor_by_id(editor_id: int) -> Editor:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT name, identifier, location
                FROM Editor
                WHERE identifier = ?
            """, (editor_id,))
            row = cursor.fetchone()
            
            if row is None:
                return None
            
            name, identifier, location = row
            return Editor(name, identifier, location)