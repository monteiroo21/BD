import random
import string
from typing import NamedTuple

from pyodbc import IntegrityError

from bd_project.session import create_connection

class WriterDescriptor(NamedTuple):
    Fname: str
    Lname: str
    genre: str
    birthYear: str
    deathYear: str


class WriterDetails(NamedTuple):
    id: int
    Fname: str
    Lname: str
    genre: str
    birthYear: str
    deathYear: str
    musGenre: str


def list_all() -> list[WriterDescriptor]:
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT Fname, Lname, genre, birthYear, deathYear FROM Writer")

        return [WriterDescriptor(*row) for row in cursor.fetchall()]
        