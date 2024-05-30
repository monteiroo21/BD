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
    location: str

class WarehouseDetails(NamedTuple):
    name: str
    identifier: int
    storage: int
    editor_name: str
    location: str
    scores: dict[tuple[str, str, str]]


def list_warehouse() -> list[Warehouse]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT w.name, w.id, w.storage, e.name, wl.warehouse_location
                            FROM Warehouse AS w
                                JOIN Editor AS e ON w.editorId = e.identifier
								JOIN warehouse_location wl ON w.id = wl.warehouse_id
                """)
            return [Warehouse(*row) for row in cursor.fetchall()]


def search_warehouse(query: str) -> list[Warehouse]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT w.name, w.id, w.storage, e.name, wl.warehouse_location
                            FROM Warehouse AS w
                                JOIN Editor AS e ON w.editorId = e.identifier
								JOIN warehouse_location wl ON w.id = wl.warehouse_id
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

            # Get the ID of the newly created warehouse
            cursor.execute("SELECT SCOPE_IDENTITY()")
            new_warehouse_id = cursor.fetchone()[0]

            # Retrieve the availability of each score stored in the new warehouse
            cursor.execute("""
                SELECT s.availability FROM Score s
                    JOIN stores st ON s.register_num = st.score_register
                    JOIN Warehouse w ON st.warehouse_id = w.id
                    WHERE w.id = ?
            """, (new_warehouse_id,))
            
            total_availability = sum(row[0] for row in cursor.fetchall())

            # Reduce the storage of the warehouse by the total availability
            cursor.execute("""
                UPDATE Warehouse
                SET storage = storage - ?
                WHERE id = ?
            """, (total_availability, new_warehouse_id))

            try:
                cursor.execute("""
                    EXEC add_warehouse @warehouse_name=?, @storage=?, @editorId=?, @warehouse_location=?
                            """, (warehouse.name, warehouse.storage, editor_id, warehouse.location))
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
                EXEC edit_warehouse @warehouse_id=?, @new_name=?, @new_storage=?, @new_editor_id=?, @new_warehouse_location=?
            """, (warehouse.identifier, warehouse.name, warehouse.storage, editor_id, warehouse.location))
            conn.commit()


def get_warehouse_by_id(warehouse_id: int) -> Warehouse:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT w.name, w.id, w.storage, e.name FROM Warehouse AS w JOIN Editor AS e ON w.editorId = e.identifier WHERE w.id = ?", (warehouse_id,))
            row = cursor.fetchone()
            if row is None:
                return None
            return Warehouse(*row)
        
def detail_warehouse(warehouse_id: int) -> WarehouseDetails:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""SELECT w.name, w.id, w.storage, e.name, wl.warehouse_location
                            FROM Warehouse AS w
                                JOIN Editor AS e ON w.editorId = e.identifier
								JOIN warehouse_location wl ON w.id = wl.warehouse_id
                            WHERE w.id=?
                """, (warehouse_id,))


            row = cursor.fetchone()
            if row is None:
                return None  # Se nenhuma linha for retornada, o compositor não existe

            # Extrair informações básicas sobre o compositor
            warehouse_info = row[:5]

            # Query para buscar as músicas associadas ao compositor
            cursor.execute("""SELECT m.title, wr.Fname + ' ' + wr.Lname as writerName, ar.type 
                FROM stores as st
                JOIN Score as s ON st.score_register = s.register_num
                JOIN Warehouse as w ON st.warehouse_id = w.id
                JOIN Music as m ON s.musicId = m.music_id
                JOIN arranges as ar ON s.register_num = ar.score_register
                JOIN Arranger as a ON ar.arranger_id = a.id
                JOIN Writer as wr ON a.id = wr.id
                WHERE w.id = ?
            """, (warehouse_id,))
            
            scores = {(score[0], score[1], score[2]) for score in cursor.fetchall()}

            return WarehouseDetails(*warehouse_info, scores)