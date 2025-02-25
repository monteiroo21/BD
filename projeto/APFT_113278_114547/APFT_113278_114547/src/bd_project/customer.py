from typing import NamedTuple
from pyodbc import IntegrityError
from bd_project.session import create_connection
from decimal import Decimal


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


class CustomerDetails(NamedTuple):
    numCC: int
    email_address: str
    numBankAccount: int
    cellNumber: int
    name: str
    transactions: dict[str, str]


class ScoreDetail(NamedTuple):
    register_num: int
    edition: int
    price: float
    availability: int
    difficultyGrade: int
    music: str
    editor_name: str
    writer_name: str
    arranger_type: str


def list_all_scores_with_details() -> list[ScoreDetail]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.register_num, s.edition, s.price, s.availability, 
                       s.difficultyGrade, m.title as music, e.name, 
                       w.Fname + ' ' + w.Lname as writer_name, ar.type
                FROM Score s
                JOIN Music m ON s.musicId = m.music_id
                JOIN Editor e ON s.editorId = e.identifier
                LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
                LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
                LEFT OUTER JOIN Writer w ON a.id = w.id
            """)
            return [ScoreDetail(*row) for row in cursor.fetchall()]
        
        
def search_scores(query: str) -> list[ScoreDetail]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.register_num, s.edition, s.price, s.availability, 
                       s.difficultyGrade, m.title as music, e.name, 
                       w.Fname + ' ' + w.Lname as writer_name, ar.type
                FROM Score s
                JOIN Music m ON s.musicId = m.music_id
                JOIN Editor e ON s.editorId = e.identifier
                LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
                LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
                LEFT OUTER JOIN Writer w ON a.id = w.id
                WHERE m.title LIKE ?
            """, ('%' + query + '%',))
            return [ScoreDetail(*row) for row in cursor.fetchall()]


def list_all_scores_sorted_by_price() -> list[ScoreDetail]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT s.register_num, s.edition, s.price, s.availability, 
                       s.difficultyGrade, m.title as music, e.name, 
                       w.Fname + ' ' + w.Lname as writer_name, ar.type
                FROM Score s
                JOIN Music m ON s.musicId = m.music_id
                JOIN Editor e ON s.editorId = e.identifier
                LEFT OUTER JOIN arranges ar ON s.register_num = ar.score_register
                LEFT OUTER JOIN Arranger a ON ar.arranger_id = a.id
                LEFT OUTER JOIN Writer w ON a.id = w.id
                ORDER BY s.price
            """)
            return [ScoreDetail(*row) for row in cursor.fetchall()]


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


def detail_customer(numCC: int) -> CustomerDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT numCC, email_address, numBankAccount, cellNumber, name FROM Customer WHERE numCC = ?", (numCC,))
            customer_row = cursor.fetchone()
            if not customer_row:
                raise ValueError("Customer not found")
            customer = Customer(*customer_row)
            
            cursor.execute("""
                SELECT t.transaction_id, t.[date], s.register_num, m.title, s.price
                FROM [Transaction] t
                JOIN constitutes c ON t.transaction_id = c.transaction_id
                JOIN Score s ON c.score_register = s.register_num
                JOIN Music m ON s.musicId = m.music_id
                WHERE t.customer_CC = ?
                ORDER BY t.transaction_id
            """, (numCC,))
            transactions = cursor.fetchall()
            
            transaction_dict = {}
            for transaction_id, date, register_num, title, price in transactions:
                if transaction_id not in transaction_dict:
                    transaction_dict[transaction_id] = {"date": date, "scores": [], "total_value": Decimal(0)}
                transaction_dict[transaction_id]["scores"].append(title)
                transaction_dict[transaction_id]["total_value"] += price
            
            formatted_transactions = {
                f"Transaction {tid} on {details['date']} (Total: ${details['total_value']:.2f})": ", ".join(details["scores"])
                for tid, details in transaction_dict.items()
            }
            
            return CustomerDetails(
                numCC=customer.numCC,
                email_address=customer.email_address,
                numBankAccount=customer.numBankAccount,
                cellNumber=customer.cellNumber,
                name=customer.name,
                transactions=formatted_transactions
            )


def edit_customer(numCC: int, new_name: str, new_email: str, new_bank_account: int, new_cell_number: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute("""
                        EXEC edit_customer @numCC = ?, @new_name = ?, @new_email_address = ?, @new_numBankAccount = ?, @new_cellNumber = ?
                    """, (numCC, new_name, new_email, new_bank_account, new_cell_number))
                conn.commit()
                print("Customer edited successfully.")
            except Exception as e:
                print(f"An error occurred: {e}")
