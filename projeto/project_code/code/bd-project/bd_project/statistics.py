from typing import List, Dict
from pyodbc import IntegrityError
from bd_project.session import create_connection

def get_composer_revenue() -> List[Dict[str, float]]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT w.Fname + ' ' + w.Lname AS ComposerName, SUM(t.value) AS TotalRevenue
                FROM Composer c
                JOIN Writer w ON c.id = w.id
                JOIN writes wr ON c.id = wr.composer_id
                JOIN Music m ON wr.music_id = m.music_id
                JOIN Score s ON m.music_id = s.musicId
                JOIN constitutes ct ON s.register_num = ct.score_register
                JOIN [Transaction] t ON ct.transaction_id = t.transaction_id
                GROUP BY w.Fname, w.Lname
                ORDER BY TotalRevenue DESC
            """)
            results = cursor.fetchall()
            # Convertendo os resultados em um formato JSON compatível
            composer_revenue = [{"ComposerName": row[0], "TotalRevenue": float(row[1])} for row in results]
            return composer_revenue

def get_genre_sales() -> List[Dict[str, str]]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT g.name AS GenreName, YEAR(t.date) AS Year, COUNT(*) AS SalesCount
                FROM Music m
                JOIN MusicalGenre g ON m.musGenre_id = g.id
                JOIN Score s ON m.music_id = s.musicId
                JOIN constitutes co ON s.register_num = co.score_register
                JOIN [Transaction] t ON co.transaction_id = t.transaction_id
                WHERE YEAR(t.date) >= YEAR(GETDATE()) - 10
                GROUP BY g.name, YEAR(t.date)
                ORDER BY Year, SalesCount DESC
            """)
            results = cursor.fetchall()
            # Convertendo os resultados em um formato JSON compatível
            genre_sales = [{"GenreName": row[0], "Year": str(row[1]), "SalesCount": str(row[2])} for row in results]
            return genre_sales

def get_composition_count_by_composer() -> List[Dict[str, int]]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT w.Fname + ' ' + w.Lname AS ComposerName, COUNT(*) AS CompositionCount
                FROM Composer c
                JOIN Writer w ON c.id = w.id
                JOIN writes wr ON c.id = wr.composer_id
                GROUP BY w.Fname, w.Lname
                ORDER BY CompositionCount DESC
            """)
            results = cursor.fetchall()
            # Convertendo os resultados em um formato JSON compatível
            composition_count = [{"ComposerName": row[0], "CompositionCount": row[1]} for row in results]
            return composition_count

def get_music_sales_by_genre() -> List[Dict[str, str]]:
    with create_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT g.name AS GenreName, m.title AS MusicTitle, COUNT(*) AS SalesCount
                FROM MusicalGenre g
                JOIN Music m ON g.id = m.musGenre_id
                JOIN Score s ON m.music_id = s.musicId
                JOIN constitutes co ON s.register_num = co.score_register
                JOIN [Transaction] t ON co.transaction_id = t.transaction_id
                GROUP BY g.name, m.title
                ORDER BY SalesCount DESC
            """)
            results = cursor.fetchall()
            # Convertendo os resultados em um formato JSON compatível
            music_sales = [{"GenreName": row[0], "MusicTitle": row[1], "SalesCount": str(row[2])} for row in results]
            return music_sales
