from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any

def get_all_departments() -> List[sn]:
    query = "SELECT id, name FROM departments"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_department_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, name FROM departments WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def add_department(name: str) -> Optional[int]:
    query = "INSERT INTO departments (name) VALUES (%s)"
    cursor.execute(query, (name,))
    conn.commit()
    return cursor.lastrowid 

def update_department(id: int, name: str) -> bool:
    query = "UPDATE departments SET name = %s WHERE id = %s"
    cursor.execute(query, (name, id))
    conn.commit()
    return True

def delete_department(id: int) -> bool:
    query = "DELETE FROM departments WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

