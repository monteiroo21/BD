from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection

class Transaction(NamedTuple):
    transaction_id: int
    value: float
    date: str
    customer_CC: int


def list_transactions() -> list[Transaction]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT transaction_id, value, date, customer_CC
                FROM [Transaction]""")
            return [Transaction(*row) for row in cursor.fetchall()]
        
    
def search_transaction(query: str) -> list[Transaction]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT transaction_id, value, date, customer_CC
                FROM [Transaction]
                WHERE customer_CC LIKE ?""", ('%' + query + '%',))
            return [Transaction(*row) for row in cursor.fetchall()]