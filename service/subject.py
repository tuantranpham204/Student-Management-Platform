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

def delete_subject(id: str) -> bool:
    query = "DELETE FROM subjects WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True


def get_subjects_by_params(subject: dict) -> List[sn]:
    where, binds = select_binds(subject)
    query = f"SELECT id, name, coff FROM subjects s {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_subject(subject: dict) -> bool:
    set_clause, binds = update_binds(subject)
    # id is CHAR
    query = f"UPDATE subjects s {set_clause} WHERE s.id = '{subject['id']}'"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(subject: dict):
    where, binds, params = ' WHERE ', [], 0
    if subject.get("id"):
        if params != 0: where += ' AND'
        where += f" s.id LIKE '%{subject['id']}%' "
        params += 1
    if subject.get("name"):
        if params != 0: where += ' AND'
        where += f" s.name LIKE '%{subject['name']}%' "
        params += 1
    if subject.get("coff"):
        if params != 0: where += ' AND'
        where += ' s.coff = %s '
        binds.append(subject["coff"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(subject: dict):
    set_clause, binds = ' SET', []
    if subject.get("name"):
        set_clause += " s.name = %s ,"
        binds.append(subject["name"])
    if subject.get("coff"):
        set_clause += " s.coff = %s ,"
        binds.append(subject["coff"])
    set_clause = set_clause[:-1]
    return set_clause, binds
