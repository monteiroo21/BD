import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class Editor (NamedTuple):
    namr: str
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