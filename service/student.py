from types import SimpleNamespace as sn
from config.db import cursor, conn
from typing import List, Optional
import re


def get_all_students() -> List[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students"
    cursor.execute(query)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]
def get_students_by_class(class_id):

    from config.db import conn

    from types import SimpleNamespace as sn
    
    cursor = conn.cursor(dictionary=True)  # ✅ ĐÚNG - dùng dictionary=True
    query = """
        SELECT sid, fname, lname, dob, address, cid, phone, email, 
               gender, generation, status, img, departmental_class_id
        FROM students
        WHERE departmental_class_id = %s
        ORDER BY sid
    """
    cursor.execute(query, (class_id,))

    students = []
    for row in cursor.fetchall():
        students.append(sn(**row))

    cursor.close()
    return students
def get_student_by_sid(sid: str) -> Optional[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students WHERE sid = %s"
    cursor.execute(query, (sid,))
    row = cursor.fetchone()
    return sn(**row)

def get_student_by_params(student:dict) -> List[sn]:
    where, binds = select_binds(student)
    query = f"SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students s {where}"
    cursor.execute(query, binds)
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def add_student(student: sn) -> bool:
    query = """
    INSERT INTO students (
        sid, fname, lname, dob, address, cid, phone, email,
        gender, generation, status, img, departmental_class_id
    ) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    binds = (
        student.sid, student.fname, student.lname, student.dob, student.address,
        student.cid, student.phone, student.email, student.gender,
        student.generation, student.status, student.img ,student.departmental_class_id
    )
    cursor.execute(query, binds)
    conn.commit()
    return True

def update_student(student:dict) -> bool:
    set, binds = update_binds(student)
    query = f"""UPDATE students s {set} WHERE s.sid = {student["sid"]}"""
    cursor.execute(query, binds)
    conn.commit()
    return True

def delete_student(sid: str) -> bool:
    query = "DELETE FROM students WHERE sid = %s"
    cursor.execute(query, (sid,))
    conn.commit()
    return True

def get_students_by_major(major_id: int) -> List[sn]:
    query = """SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students s 
               JOIN departmental_classes dc ON dc.departmental_class_id = s.departmental_class_id
               WHERE dc.major_id = %s"""
    cursor.execute(query, (major_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def get_students_by_departmental_class(class_id: str) -> List[sn]:
    query = "SELECT sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id FROM students WHERE departmental_class_id = %s"
    cursor.execute(query, (class_id,))
    rows = cursor.fetchall()
    return [sn(**row) for row in rows]

def select_binds(student: dict):
    where, binds, params = ' WHERE ', [], 0

    if student["sid"]:
        if params != 0: where += ' AND'
        where += f" s.sid LIKE '%{student['sid']}%' "
        params += 1

    if student["fname"]:
        if params != 0: where += ' AND'
        where += f" s.fname LIKE '%{student['fname']}%' "
        params += 1

    if student["lname"]:
        if params != 0: where += ' AND'
        where += f" s.lname LIKE '%{student['lname']}%' "
        params += 1

    if student["dob"] is not None:
        if params != 0: where += ' AND'
        where += ' s.dob = %s '
        binds.append(student["dob"])
        params += 1

    if student["address"]:
        if params != 0: where += ' AND'
        where += f" s.address LIKE '%{student['address']}%' "
        params += 1

    if student["cid"]:
        if params != 0: where += ' AND'
        where += f" s.cid LIKE '%{student['cid']}%' "
        params += 1

    if student["phone"]:
        if params != 0: where += ' AND'
        where += f" s.phone LIKE '%{student['phone']}%' "
        params += 1

    if student["email"]:
        if params != 0: where += ' AND'
        where += f" s.email LIKE '%{student['email']}%' "
        params += 1

    if student["gender"] is not None:
        if params != 0: where += ' AND'
        where += ' s.gender = %s '
        binds.append(1 if student["gender"] else 0)
        params += 1

    if student["status"]:
        if params != 0: where += ' AND'
        where += ' s.status = %s '
        binds.append(student["status"])
        params += 1

    if student["departmental_class_id"]:
        if params != 0: where += ' AND'
        where += ' s.departmental_class_id = %s '
        binds.append(student["departmental_class_id"])
        params += 1

    if params == 0:
        where = ''

    return where, binds

def update_binds(student:dict):
    set, binds = ' SET', []
    if student["fname"]:
        set += f" s.fname = %s ,"
        binds.append(student["fname"])
    if student["lname"]:
        set += f" s.lname = %s,"
        binds.append(student["lname"])
    if student["dob"] is not None:
        set += f" s.dob = %s ,"
        binds.append(student["dob"])
    if student["address"]:
        set += f" s.address = %s ,"
        binds.append(student["address"])
    if student["cid"]:
        set += f" s.cid = %s ,"
        binds.append(student["cid"])
    if student["phone"]:
        set += f" s.phone = %s ,"
        binds.append(student["phone"])
    if student["email"]:
        set += f" s.email = %s ,"
        binds.append(student["email"])
    if student["gender"]:
        set += f" s.gender = %s ,"
        if student["gender"] == True: binds.append(1)
        else: binds.append(0)
    if student["status"]:
        set += f" s.status = %s ,"
        binds.append(student["status"])
    if student["departmental_class_id"]:
        set += f" s.departmental_class_id = ? ,"
        binds.append(student["departmental_class_id"])
    set = re.sub(r'.$', '', set)
    return set, binds




