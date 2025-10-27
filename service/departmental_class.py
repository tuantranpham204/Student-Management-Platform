from types import SimpleNamespace as sn
from config.db import cursor, conn 
from typing import List, Optional, Any


def get_all_classes() -> List[sn]:
    query = "SELECT id, name, major_id FROM departmental_classes"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_class_by_id(id: str) -> Optional[sn]:
    query = "SELECT id, name, major_id FROM departmental_classes WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def get_classes_by_major(major_id: int) -> List[sn]:
    query = "SELECT id, name, major_id FROM departmental_classes WHERE major_id = %s"
    cursor.execute(query, (major_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_class(id: str, name: str, major_id: int) -> bool:
    query = "INSERT INTO departmental_classes (id, name, major_id) VALUES (%s, %s, %s)"
    cursor.execute(query, (id, name, major_id))
    conn.commit()
    return True

def update_class(id: str, name: str, major_id: int) -> bool:
    query = "UPDATE departmental_classes SET name = %s, major_id = %s WHERE id = %s"
    cursor.execute(query, (name, major_id, id))
    conn.commit()
    return True

def delete_class(id: str) -> bool:
    query = "DELETE FROM departmental_classes WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

