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

def delete_class(id: str) -> bool:
    query = "DELETE FROM departmental_classes WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

def get_classes_by_params(dep_class: dict) -> List[sn]:
    where, binds = select_binds(dep_class)
    query = f"SELECT id, name, major_id FROM departmental_classes dc {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_class(dep_class: dict) -> bool:
    set_clause, binds = update_binds(dep_class)
    # id is varchar in DB
    query = f"UPDATE departmental_classes dc {set_clause} WHERE dc.id = '{dep_class['id']}'"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(dep_class: dict):
    where, binds, params = ' WHERE ', [], 0
    if dep_class.get("id"):
        if params != 0: where += ' AND'
        where += f" dc.id LIKE '%{dep_class['id']}%' "
        params += 1
    if dep_class.get("name"):
        if params != 0: where += ' AND'
        where += f" dc.name LIKE '%{dep_class['name']}%' "
        params += 1
    if dep_class.get("major_id"):
        if params != 0: where += ' AND'
        where += ' dc.major_id = %s '
        binds.append(dep_class["major_id"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(dep_class: dict):
    set_clause, binds = ' SET', []
    if dep_class.get("name"):
        set_clause += " dc.name = %s ,"
        binds.append(dep_class["name"])
    if dep_class.get("major_id"):
        set_clause += " dc.major_id = %s ,"
        binds.append(dep_class["major_id"])
    set_clause = set_clause[:-1]
    return set_clause, binds
