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