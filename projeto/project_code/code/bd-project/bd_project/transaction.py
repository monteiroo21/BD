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
        

def create_transaction(transaction: Transaction, scores: list[int]):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                for score in scores:
                    cursor.execute("""
                        SELECT availability FROM Score WHERE register_num = ?
                    """, (score,))
                    result = cursor.fetchone()
                    if result is None or result[0] <= 0:
                        raise ValueError(f"Score with register_num {score} is not available.")

                cursor.execute("""
                    INSERT INTO [Transaction] (transaction_id, value, date, customer_CC)
                    VALUES (?, ?, ?, ?)""",
                    (transaction.transaction_id, transaction.value, transaction.date, transaction.customer_CC)
                )

                for score in scores:
                    cursor.execute("""
                        INSERT INTO constitutes (score_register, transaction_id)
                        VALUES (?, ?)""",
                        (score, transaction.transaction_id)
                    )

                    cursor.execute("""
                        UPDATE Score
                        SET availability = availability - 1
                        WHERE register_num = ?""",
                        (score,)
                    )

                conn.commit()
            except IntegrityError as e:
                print(f"An error occurred: {e}")
                conn.rollback()
            except ValueError as e:
                print(e)
                conn.rollback()


def list_customers():
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT numCC, name FROM Customer")
            return cursor.fetchall()


def list_scores():
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.register_num, m.title
                FROM Score s
                JOIN Music m ON s.musicId = m.music_id
            """)
            return cursor.fetchall()
