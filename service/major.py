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

def get_major_by_dep_cls_id(dep_cls_id: int) -> Optional[sn]:
    query = "SELECT m.id, m.name FROM majors m JOIN departmental_classes dc ON dc.major_id = m.id WHERE dc.id = %s"
    cursor.execute(query, (dep_cls_id,))
    row = cursor.fetchone()
    return sn(**row)

def add_major(name: str, department_id: int) -> Optional[int]:
    query = "INSERT INTO majors (name, department_id) VALUES (%s, %s)"
    cursor.execute(query, (name, department_id))
    conn.commit()
    return cursor.lastrowid

def delete_major(id: int) -> bool:
    query = "DELETE FROM majors WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

def get_majors_by_params(major: dict) -> List[sn]:
    where, binds = select_binds(major)
    query = f"SELECT id, name, department_id FROM majors m {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_major(major: dict) -> bool:
    set_clause, binds = update_binds(major)
    query = f"UPDATE majors m {set_clause} WHERE m.id = {major['id']}"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(major: dict):
    where, binds, params = ' WHERE ', [], 0
    if major.get("id"):
        if params != 0: where += ' AND'
        where += ' m.id = %s '
        binds.append(major["id"])
        params += 1
    if major.get("name"):
        if params != 0: where += ' AND'
        where += f" m.name LIKE '%{major['name']}%' "
        params += 1
    if major.get("department_id"):
        if params != 0: where += ' AND'
        where += ' m.department_id = %s '
        binds.append(major["department_id"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(major: dict):
    set_clause, binds = ' SET', []
    if major.get("name"):
        set_clause += " m.name = %s ,"
        binds.append(major["name"])
    if major.get("department_id"):
        set_clause += " m.department_id = %s ,"
        binds.append(major["department_id"])
    set_clause = set_clause[:-1]
    return set_clause, binds

