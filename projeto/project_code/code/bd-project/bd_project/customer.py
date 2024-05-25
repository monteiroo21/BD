import random
import string
from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Customer(NamedTuple):
    numCC: int
    email_address: str
    numBankAccount: int
    cellNumber: int
    name: str


def list_customers() -> list[Customer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name
                FROM Customer AS c
                """)
            return [Customer(*row) for row in cursor.fetchall()]
        

def search_customer(query: str) -> list[Customer]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name
                FROM Customer AS c
                WHERE c.name LIKE ?""", ('%' + query + '%',))
            return [Customer(*row) for row in cursor.fetchall()]