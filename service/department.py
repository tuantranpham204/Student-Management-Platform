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

def get_department_by_major_id(major_id: int) -> Optional[sn]:
    query = "SELECT d.id, d.name FROM departments d JOIN majors m ON m.department_id = d.id WHERE m.id = %s"
    cursor.execute(query, (major_id,))
    row = cursor.fetchone()
    return sn(**row)

def add_department(name: str) -> Optional[int]:
    query = "INSERT INTO departments (name) VALUES (%s)"
    cursor.execute(query, (name,))
    conn.commit()
    return cursor.lastrowid

def delete_department(id: int) -> bool:
    query = "DELETE FROM departments WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

def get_departments_by_params(department: dict) -> List[sn]:
    where, binds = select_binds(department)
    query = f"SELECT id, name FROM departments d {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_department(department: dict) -> bool:
    set_clause, binds = update_binds(department)
    query = f"UPDATE departments d {set_clause} WHERE d.id = {department['id']}"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(department: dict):
    where, binds, params = ' WHERE ', [], 0
    if department.get("id"):
        if params != 0: where += ' AND'
        where += ' d.id = %s '
        binds.append(department["id"])
        params += 1
    if department.get("name"):
        if params != 0: where += ' AND'
        where += f" d.name LIKE '%{department['name']}%' "
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(department: dict):
    set_clause, binds = ' SET', []
    if department.get("name"):
        set_clause += " d.name = %s ,"
        binds.append(department["name"])
    set_clause = set_clause[:-1]
    return set_clause, binds

