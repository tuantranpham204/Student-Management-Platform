from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any

def get_all_classes() -> List[sn]:
    query = "SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_class_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def get_classes_by_semester(semester_id: int) -> List[sn]:
    query = "SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes WHERE semester_id = %s"
    cursor.execute(query, (semester_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_class(name: str, semester_id: int, subject_id: str, major_id: int) -> Optional[int]:
    query = "INSERT INTO sectional_classes (name, semester_id, subject_id, major_id) VALUES (%s, %s, %s, %s)"
    cursor.execute(query, (name, semester_id, subject_id, major_id))
    conn.commit()
    return cursor.lastrowid

def update_class(id: int, name: str, semester_id: int, subject_id: str, major_id: int) -> bool:
    query = "UPDATE sectional_classes SET name = %s, semester_id = %s, subject_id = %s, major_id = %s WHERE id = %s"
    cursor.execute(query, (name, semester_id, subject_id, major_id, id))
    conn.commit()
    return True

def delete_class(id: int) -> bool:
    query = "DELETE FROM sectional_classes WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

