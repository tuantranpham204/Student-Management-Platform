from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any


def get_all_subjects() -> List[sn]:
    query = "SELECT id, name, coff FROM subjects"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_subject_by_id(id: str) -> Optional[sn]:
    query = "SELECT id, name, coff FROM subjects WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def add_subject(id: str, name: str, coff: str) -> bool:
    query = "INSERT INTO subjects (id, name, coff) VALUES (%s, %s, %s)"
    cursor.execute(query, (id, name, coff))
    conn.commit()
    return True

def update_subject(id: str, name: str, coff: str) -> bool:
    query = "UPDATE subjects SET name = %s, coff = %s WHERE id = %s"
    cursor.execute(query, (name, coff, id))
    conn.commit()
    return True

def delete_subject(id: str) -> bool:
    query = "DELETE FROM subjects WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

