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

            try:
                cursor.execute("""
                    EXEC add_warehouse @warehouse_name=?, @storage=?, @editorId=?
                            """, (warehouse.name, warehouse.storage, editor_id))
                conn.commit()
            except Exception as e:
                print(f"Failed to create warehouse: {e}")
                conn.rollback()


def list_editors() -> list[str]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT [name] FROM Editor")
            return [row[0] for row in cursor.fetchall()]
        

def delete_warehouse(warehouse_id: int):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Check if the warehouse exists
            cursor.execute("SELECT id FROM Warehouse WHERE id = ?", (warehouse_id,))
            if cursor.fetchone() is None:
                raise ValueError(f"Warehouse with ID '{warehouse_id}' does not exist")

            # Delete the warehouse entry from the Warehouse table
            try:
                cursor.execute("DELETE FROM Warehouse WHERE id = ?", (warehouse_id,))
                conn.commit()
                print(f"Warehouse with ID {warehouse_id} deleted successfully.")
            except IntegrityError as e:
                conn.rollback()
                raise RuntimeError(f"Failed to delete warehouse with ID {warehouse_id}: {e}")
            

def edit_warehouse(warehouse: Warehouse):
    with create_connection() as conn:
        with conn.cursor() as cursor:
            # Fetch the editor ID for the new editor name
            cursor.execute("SELECT identifier FROM Editor WHERE name = ?", (warehouse.editor_name,))
            editor_id = cursor.fetchone()
            if editor_id is None:
                raise ValueError(f"Editor '{warehouse.editor_name}' does not exist")
            editor_id = editor_id[0]

            # Execute the stored procedure to update the warehouse
            cursor.execute("""
                EXEC edit_warehouse @warehouse_id=?, @new_name=?, @new_storage=?, @new_editor_id=?
            """, (warehouse.identifier, warehouse.name, warehouse.storage, editor_id))
            conn.commit()


def get_warehouse_by_id(warehouse_id: int) -> Warehouse:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT w.name, w.id, w.storage, e.name FROM Warehouse AS w JOIN Editor AS e ON w.editorId = e.identifier WHERE w.id = ?", (warehouse_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Warehouse(*row)