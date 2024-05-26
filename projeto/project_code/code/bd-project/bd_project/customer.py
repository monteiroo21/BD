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


class CustomerWithTransactionCount(NamedTuple):
    numCC: int
    email_address: str
    numBankAccount: int
    cellNumber: int
    name: str
    transaction_count: int


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


def create_customer(customer: Customer):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                    EXEC add_customer @numCC = ?, @email_address = ?, @numBankAccount = ?, @cellNumber = ?, @name = ?
                    """, 
                    customer.numCC, customer.email_address, customer.numBankAccount, customer.cellNumber, customer.name
                )
                conn.commit()
                print("Customer added successfully.")
            except IntegrityError as e:
                print(f"An error occurred: {e}")


def list_customers_with_transaction_count() -> list[CustomerWithTransactionCount]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name, COUNT(t.transaction_id) AS transaction_count
                FROM Customer AS c
                LEFT JOIN [Transaction] AS t ON c.numCC = t.customer_CC
                GROUP BY c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name
            """)
            return [CustomerWithTransactionCount(*row) for row in cursor.fetchall()]


def search_customer_with_transaction_count(query: str) -> list[CustomerWithTransactionCount]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name, COUNT(t.transaction_id) AS transaction_count
                FROM Customer AS c
                LEFT JOIN [Transaction] AS t ON c.numCC = t.customer_CC
                WHERE c.name LIKE ?
                GROUP BY c.numCC, c.email_address, c.numBankAccount, c.cellNumber, c.name
            """, ('%' + query + '%',))
            return [CustomerWithTransactionCount(*row) for row in cursor.fetchall()]


def delete_customer(numCC: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("DELETE FROM Customer WHERE numCC = ?", (numCC,))
                conn.commit()
                print("Customer deleted successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
