from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any

SEMESTER_COLUMNS = ('id', 'year', 'term_order')

def _map_row_to_semester(row: tuple) -> Optional[sn]:
    if not row:
        return None
    return sn(**dict(zip(SEMESTER_COLUMNS, row)))

def get_all_semesters() -> List[sn]:
    query = "SELECT id, year, term_order FROM semesters"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [_map_row_to_semester(row) for row in rows]

def get_semester_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, year, term_order FROM semesters WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return _map_row_to_semester(row)

def get_semesters_by_year(year: int) -> List[sn]:
    query = "SELECT id, year, term_order FROM semesters WHERE year = %s"
    cursor.execute(query, (year,))
    rows = cursor.fetchall()
    return [_map_row_to_semester(row) for row in rows]

def add_semester(year: int, term_order: str) -> Optional[int]:
    query = "INSERT INTO semesters (year, term_order) VALUES (%s, %s)"
    cursor.execute(query, (year, term_order))
    conn.commit()
    return cursor.lastrowid

def update_semester(id: int, year: int, term_order: str) -> bool:
    query = "UPDATE semesters SET year = %s, term_order = %s WHERE id = %s"
    cursor.execute(query, (year, term_order, id))
    conn.commit()
    return True

def delete_semester(id: int) -> bool:
    query = "DELETE FROM semesters WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

