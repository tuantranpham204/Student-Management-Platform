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

