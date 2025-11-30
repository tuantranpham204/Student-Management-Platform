from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional, Any

def get_all_scores() -> List[sn]:
    query = "SELECT sectional_class_id, student_id, regular1, regular2, regular3, midterm, final FROM scores"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]
def get_scores_by_student(student_id):
    """Lấy điểm của một sinh viên"""
    from config.db import conn  # ✅ ĐÚNG
    from types import SimpleNamespace as sn
    
    cursor = conn.cursor(dictionary=True)  # ✅ ĐÚNG
    query = """
        SELECT sectional_class_id, student_id, regular1, regular2, 
               regular3, midterm, final
        FROM scores
        WHERE student_id = %s
    """
    cursor.execute(query, (student_id,))
    
    scores = []
    for row in cursor.fetchall():
        scores.append(sn(**row))  # ✅ ĐÚNG - dùng **row với dictionary
    
    cursor.close()
    return scores
def get_score_by_pk(sectional_class_id: int, student_id: str) -> Optional[sn]:
    query = "SELECT sectional_class_id, student_id, regular1, regular2, regular3, midterm, final FROM scores WHERE sectional_class_id = %s AND student_id = %s"
    cursor.execute(query, (sectional_class_id, student_id))
    row = cursor.fetchone()
    return sn(**row)

def get_scores_by_student(student_id: str) -> List[sn]:
    query = "SELECT sectional_class_id, student_id, regular1, regular2, regular3, midterm, final FROM scores WHERE student_id = %s"
    cursor.execute(query, (student_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_scores_by_sectional_class(sectional_class_id: int) -> List[sn]:
    query = "SELECT sectional_class_id, student_id, regular1, regular2, regular3, midterm, final FROM scores WHERE sectional_class_id = %s"
    cursor.execute(query, (sectional_class_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_or_update_score(score: sn) -> bool:
    query = """
    INSERT INTO scores (sectional_class_id, student_id, regular1, regular2, regular3, midterm, final)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
        regular1 = VALUES(regular1),
        regular2 = VALUES(regular2),
        regular3 = VALUES(regular3),
        midterm = VALUES(midterm),
        final = VALUES(final)
    """
    values = (
        score.sectional_class_id, score.student_id, score.regular1,
        score.regular2, score.regular3, score.midterm, score.final
    )
    cursor.execute(query, values)
    conn.commit()
    return True

def delete_score(sectional_class_id: int, student_id: str) -> bool:
    query = "DELETE FROM scores WHERE sectional_class_id = %s AND student_id = %s"
    cursor.execute(query, (sectional_class_id, student_id))
    conn.commit()
    return True

def get_scores_by_params(score: dict) -> List[sn]:
    where, binds = select_binds(score)
    query = f"SELECT sectional_class_id, student_id, regular1, regular2, regular3, midterm, final FROM scores s {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def update_score(score: dict) -> bool:
    set_clause, binds = update_binds(score)
    # Composite PK
    query = f"UPDATE scores s {set_clause} WHERE s.sectional_class_id = {score['sectional_class_id']} AND s.student_id = '{score['student_id']}'"
    cursor.execute(query, binds)
    conn.commit()
    return True

def select_binds(score: dict):
    where, binds, params = ' WHERE ', [], 0
    if score.get("sectional_class_id"):
        if params != 0: where += ' AND'
        where += ' s.sectional_class_id = %s '
        binds.append(score["sectional_class_id"])
        params += 1
    if score.get("student_id"):
        if params != 0: where += ' AND'
        where += ' s.student_id = %s '
        binds.append(score["student_id"])
        params += 1
    if params == 0: where = ''
    return where, binds

def update_binds(score: dict):
    set_clause, binds = ' SET', []
    # For numeric scores, check is not None
    if score.get("regular1") is not None:
        set_clause += " s.regular1 = %s ,"
        binds.append(score["regular1"])
    if score.get("regular2") is not None:
        set_clause += " s.regular2 = %s ,"
        binds.append(score["regular2"])
    if score.get("regular3") is not None:
        set_clause += " s.regular3 = %s ,"
        binds.append(score["regular3"])
    if score.get("midterm") is not None:
        set_clause += " s.midterm = %s ,"
        binds.append(score["midterm"])
    if score.get("final") is not None:
        set_clause += " s.final = %s ,"
        binds.append(score["final"])
    set_clause = set_clause[:-1]
    return set_clause, binds

