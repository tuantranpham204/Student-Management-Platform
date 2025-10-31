from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional


def get_all_students() -> List[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_student_by_sid(sid: str) -> Optional[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students WHERE sid = %s"
    cursor.execute(query, (sid,))
    row = cursor.fetchone()
    return sn(**row)

def add_student(student: sn) -> bool:
    query = """
    INSERT INTO students (
        sid, fname, lname, dob, address, cid, phone, email,
        gender, generation, status, img, departmental_class_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student.sid, student.fname, student.lname, student.dob, student.address,
        student.cid, student.phone, student.email, student.gender,
        student.generation, student.img, student.departmental_class_id, student.major_id,
        student.graduated, student.active
    )
    cursor.execute(query, values)
    conn.commit()
    return True

def update_student(student: sn) -> bool:
    query = """
    UPDATE students SET
        sid, fname, lname, dob, address, cid, phone, email,
        gender, generation, status, img, departmental_class_id
    WHERE sid = %s
    """
    values = (
        student.fname, student.lname, student.dob, student.address,
        student.cid, student.phone, student.email, student.gender,
        student.generation, student.status, student.status,student.img, student.departmental_class_id, student.sid
    )
    cursor.execute(query, values)
    conn.commit()
    return True

def delete_student(sid: str) -> bool:
    query = "DELETE FROM students WHERE sid = %s"
    cursor.execute(query, (sid,))
    conn.commit()
    return True

def get_students_by_major(major_id: int) -> List[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students WHERE major_id = %s"
    cursor.execute(query, (major_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_students_by_departmental_class(class_id: str) -> List[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students WHERE departmental_class_id = %s"
    cursor.execute(query, (class_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]