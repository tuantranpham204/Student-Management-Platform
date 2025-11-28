from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any


def get_all_semesters() -> List[sn]:
    query = "SELECT id, year, term_order FROM semesters"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_semester_by_id(id: int) -> Optional[sn]:
    query = "SELECT id, year, term_order FROM semesters WHERE id = %s"
    cursor.execute(query, (id,))
    row = cursor.fetchone()
    return sn(**row)

def get_semesters_by_year(year: int) -> List[sn]:
    query = "SELECT id, year, term_order FROM semesters WHERE year = %s"
    cursor.execute(query, (year,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_semester(year: int, term_order: str) -> Optional[int]:
    query = "INSERT INTO semesters (year, term_order) VALUES (%s, %s)"
    cursor.execute(query, (year, term_order))
    conn.commit()
    return cursor.lastrowid

def delete_semester(id: int) -> bool:
    query = "DELETE FROM semesters WHERE id = %s"
    cursor.execute(query, (id,))
    conn.commit()
    return True

def get_semesters_by_params(semester: dict) -> List[sn]:
    where, binds = select_binds(semester)
    query = f"SELECT id, year, term_order FROM semesters s {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_semester(semester: dict) -> bool:
    set_clause, binds = update_binds(semester)
    query = f"UPDATE semesters s {set_clause} WHERE s.id = {semester['id']}"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(semester: dict):
    where, binds, params = ' WHERE ', [], 0
    if semester.get("id"):
        if params != 0: where += ' AND'
        where += ' s.id = %s '
        binds.append(semester["id"])
        params += 1
    if semester.get("year"):
        if params != 0: where += ' AND'
        where += ' s.year = %s '
        binds.append(semester["year"])
        params += 1
    if semester.get("term_order"):
        if params != 0: where += ' AND'
        where += ' s.term_order = %s '
        binds.append(semester["term_order"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(semester: dict):
    set_clause, binds = ' SET', []
    if semester.get("year"):
        set_clause += " s.year = %s ,"
        binds.append(semester["year"])
    if semester.get("term_order"):
        set_clause += " s.term_order = %s ,"
        binds.append(semester["term_order"])
    set_clause = set_clause[:-1]
    return set_clause, binds

