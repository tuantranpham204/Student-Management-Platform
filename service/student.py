from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional
import util.util as util
from service import departmental_class


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

def get_student_by_params(student:dict) -> List[sn]:
    where, binds = bind_student(student)
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students s "
    query += where
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

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

def bind_student(student:dict):
    where, binds, params = ' WHERE ', [], 0
    if student["sid"]:
        if params != 0: where += ' AND'
        where += f" s.sid LIKE '%{student["sid"]}%' "
        params += 1
    if student["fname"]:
        if params != 0: where += ' AND'
        where += f" s.fname LIKE '%{student["fname"]}%' "
        params += 1
    if student["lname"]:
        if params != 0: where += ' AND'
        where += f" s.lname LIKE '%{student["lname"]}%' "
        params += 1
    if student["dob"] is not None:
        if params != 0: where += ' AND'
        where += ' s.dob = %s '
        binds.append(student["dob"])
        params += 1
    if student["address"]:
        if params != 0: where += ' AND'
        where += f" s.address LIKE '%{student["address"]}%' "
        params += 1
    if student["cid"]:
        if params != 0: where += ' AND'
        where += f" s.cid LIKE '%{student["cid"]}%' "
        params += 1
    if student["phone"]:
        if params != 0: where += ' AND'
        where += f" s.phone LIKE '%{student["phone"]}%' "
        params += 1
    if student["email"]:
        if params != 0: where += ' AND'
        where += f" s.email LIKE '%{student["email"]}%' "
        params += 1
    if student["gender"]:
        if params != 0: where += ' AND'
        where += ' s.gender = %s '
        if student["gender"] == True: binds.append(1)
        else: binds.append(0)
        params += 1
    if student["status"]:
        if params != 0: where += ' AND'
        where += f" s.status = %{student["status"]}%' "
        params += 1
    if student["departmental_class_id"]:
        if params != 0: where += ' AND'
        where += ' s.departmental_class_id = %s '
        binds.append(student["departmental_class_id"])
        params += 1
    return where, binds



