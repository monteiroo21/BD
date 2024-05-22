import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Editor (NamedTuple):
    name: str
    identifier: int
    location: str


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
            cursor.execute("""
                EXEC add_editor @name=?, @location=?
                        """, (editor.name, editor.location))
            conn.commit()

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