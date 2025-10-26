from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional

STUDENT_COLUMNS = (
    'sid', 'fname', 'lname', 'bod', 'address', 'cid', 'phone', 'email',
    'gender', 'generation', 'img', 'departmental_class_id', 'major_id',
    'graduated', 'active'
)

def _map_row_to_student(row: tuple) -> Optional[sn]:
    if not row:
        return None
    return sn(**dict(zip(STUDENT_COLUMNS, row)))

def get_all_students() -> List[sn]:
    query = "SELECT sid, fname, lname, bod, address, cid, phone, email, gender, generation, img, departmental_class_id, major_id, graduated, active FROM students"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [_map_row_to_student(row) for row in rows]

def get_student_by_sid(sid: str) -> Optional[sn]:
    query = "SELECT sid, fname, lname, bod, address, cid, phone, email, gender, generation, img, departmental_class_id, major_id, graduated, active FROM students WHERE sid = %s"
    cursor.execute(query, (sid,))
    row = cursor.fetchone()
    return _map_row_to_student(row)

def add_student(student: sn) -> bool:
    query = """
    INSERT INTO students (
        sid, fname, lname, bod, address, cid, phone, email,
        gender, generation, img, departmental_class_id, major_id,
        graduated, active
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        student.sid, student.fname, student.lname, student.bod, student.address,
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
        fname = %s, lname = %s, bod = %s, address = %s, cid = %s,
        phone = %s, email = %s, gender = %s, generation = %s, img = %s,
        departmental_class_id = %s, major_id = %s,
        graduated = %s, active = %s
    WHERE sid = %s
    """
    values = (
        student.fname, student.lname, student.bod, student.address,
        student.cid, student.phone, student.email, student.gender,
        student.generation, student.img, student.departmental_class_id,
        student.major_id, student.graduated, student.active, student.sid
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
    query = "SELECT sid, fname, lname, bod, address, cid, phone, email, gender, generation, img, departmental_class_id, major_id, graduated, active FROM students WHERE major_id = %s"
    cursor.execute(query, (major_id,))
    rows = cursor.fetchall()
    return [_map_row_to_student(row) for row in rows]

def get_students_by_departmental_class(class_id: str) -> List[sn]:
    query = "SELECT sid, fname, lname, bod, address, cid, phone, email, gender, generation, img, departmental_class_id, major_id, graduated, active FROM students WHERE departmental_class_id = %s"
    cursor.execute(query, (class_id,))
    rows = cursor.fetchall()
    return [_map_row_to_student(row) for row in rows]

