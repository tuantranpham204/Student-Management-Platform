from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any

def get_all_majors() -> List[sn]:
    query = "SELECT id, name, department_id FROM majors"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_major_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, name, department_id FROM majors WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def get_major_by_name(name: str) -> Optional[sn]:
    query = "SELECT id, name, department_id FROM majors WHERE name = %s"
    cursor.execute(query, (name,))
    row = cursor.fetchone()
    return sn(**row)

def get_majors_by_department(department_id: int) -> List[sn]:
    query = "SELECT id, name, department_id FROM majors WHERE department_id = %s"
    cursor.execute(query, (department_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_major(name: str, department_id: int) -> Optional[int]:
    query = "INSERT INTO majors (name, department_id) VALUES (%s, %s)"
    cursor.execute(query, (name, department_id))
    conn.commit()
    return cursor.lastrowid

def update_major(id: int, name: str, department_id: int) -> bool:
    query = "UPDATE majors SET name = %s, department_id = %s WHERE id = %s"
    cursor.execute(query, (name, department_id, id))
    conn.commit()
    return True

def delete_major(id: int) -> bool:
    query = "DELETE FROM majors WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

