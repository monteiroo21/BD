import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Warehouse (NamedTuple):
    name: str
    identifier: int
    storage: int
    editor_name: str


def list_warehouse() -> list[Warehouse]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT w.name, w.id, w.storage, e.name 
                            FROM Warehouse AS w
                                JOIN Editor AS e ON w.editorId = e.identifier
                """)
            return [Warehouse(*row) for row in cursor.fetchall()]


def search_warehouse(query: str) -> list[Warehouse]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT w.name, w.id, w.storage, e.name 
                FROM Warehouse AS w
                    JOIN Editor AS e ON w.editorId = e.identifier
                WHERE w.name LIKE ?""", ('%' + query + '%',))
            return [Warehouse(*row) for row in cursor.fetchall()]
        
def create_warehouse(warehouse: Warehouse):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT identifier FROM Editor WHERE name = ?", (warehouse.editor_name,))
            editor_id = cursor.fetchone()
            if editor_id is None:
                raise ValueError(f"Editor '{warehouse.editor_name}' does not exist")
            editor_id = editor_id[0]
            cursor.execute("""
                EXEC add_warehouse @warehouse_name=?, @storage=?, @editorId=?
                        """, (warehouse.name, warehouse.storage, editor_id))
            conn.commit()


def list_editors() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM Editor")
            return [row[0] for row in cursor.fetchall()]