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

def get_classes_by_major_id(major_id: int) -> List[sn]:
    query = "SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes WHERE major_id = %s"
    cursor.execute(query, (major_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_classes_by_subject_id(subject_id: int) -> Optional[sn]:
    query = "SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes WHERE subject_id = %s"
    cursor.execute(query, (subject_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

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

def delete_class(id: int) -> bool:
    query = "DELETE FROM sectional_classes WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

def get_sectional_classes_by_params(sec_class: dict) -> List[sn]:
    where, binds = select_binds(sec_class)
    query = f"SELECT id, name, semester_id, subject_id, major_id FROM sectional_classes sc {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_class(sec_class: dict) -> bool:
    set_clause, binds = update_binds(sec_class)
    query = f"UPDATE sectional_classes sc {set_clause} WHERE sc.id = {sec_class['id']}"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(sec_class: dict):
    where, binds, params = ' WHERE ', [], 0
    if sec_class.get("id"):
        if params != 0: where += ' AND'
        where += ' sc.id = %s '
        binds.append(sec_class["id"])
        params += 1
    if sec_class.get("name"):
        if params != 0: where += ' AND'
        where += f" sc.name LIKE '%{sec_class['name']}%' "
        params += 1
    if sec_class.get("semester_id"):
        if params != 0: where += ' AND'
        where += ' sc.semester_id = %s '
        binds.append(sec_class["semester_id"])
        params += 1
    if sec_class.get("subject_id"):
        if params != 0: where += ' AND'
        where += ' sc.subject_id = %s '
        binds.append(sec_class["subject_id"])
        params += 1
    if sec_class.get("major_id"):
        if params != 0: where += ' AND'
        where += ' sc.major_id = %s '
        binds.append(sec_class["major_id"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(sec_class: dict):
    set_clause, binds = ' SET', []
    if sec_class.get("name"):
        set_clause += " sc.name = %s ,"
        binds.append(sec_class["name"])
    if sec_class.get("semester_id"):
        set_clause += " sc.semester_id = %s ,"
        binds.append(sec_class["semester_id"])
    if sec_class.get("subject_id"):
        set_clause += " sc.subject_id = %s ,"
        binds.append(sec_class["subject_id"])
    if sec_class.get("major_id"):
        set_clause += " sc.major_id = %s ,"
        binds.append(sec_class["major_id"])
    set_clause = set_clause[:-1]
    return set_clause, binds

