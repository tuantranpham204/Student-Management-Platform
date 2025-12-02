import os
from dotenv import load_dotenv
from types import SimpleNamespace

# Load .env file
from types import SimpleNamespace

# Load .env file
load_dotenv()

default_vals = SimpleNamespace(
    DEFAULT_BG_COLOR=os.getenv("DEFAULT_BG_COLOR"),
    BG_COLOR=os.getenv("BG_COLOR"),
    FG_COLOR=os.getenv("FG_COLOR"),
    ACCENT_COLOR=os.getenv("ACCENT_COLOR"),
    HOVER_COLOR=os.getenv("HOVER_COLOR"),
    BORDER_COLOR=os.getenv("BORDER_COLOR"),
    INPUT_COLOR=os.getenv("INPUT_COLOR"),
)

attrs = SimpleNamespace(
    student=('sid', 'fname', 'lname', 'dob', 'address', 'cid', 'phone', 'email', 'gender', 'generation', 'status', 'img', 'departmental_class_id'),
    department=('id', 'name'),
    major=('id', 'name', 'department_id'),
    departmental_class=('id', 'name', 'major_id'),
    # Expanded attributes for Subject to handle split columns
    subject=('id', 'name', 'reg1', 'reg2', 'reg3', 'mid', 'fin'),
    semester=('id', 'year', 'term_order'),
    sectional_class=('id', 'name', 'semester_id', 'subject_id', 'major_id'),
    score=('sectional_class_id', 'student_id', 'regular1', 'regular2', 'regular3', 'midterm', 'final'),
    user=('id', 'username', 'password', 'name', 'email')
)

headings = SimpleNamespace(
    student=('Student ID', 'First name', 'Last name', 'Date of birth', 'Address', 'Citizen ID',
             'Phone number', 'Email', 'Gender', 'Generation', 'Status', 'Image Directory', 'Departmental class'),
    department=('Department ID', 'Department Name'),
    major=('Major ID', 'Major Name', 'Department ID'),
    departmental_class=('Class ID', 'Class Name', 'Major ID'),
    # Expanded headings for Subject
    subject=('Subject ID', 'Subject Name', 'Reg 1', 'Reg 2', 'Reg 3', 'Midterm', 'Final'),
    semester=('Semester ID', 'Year', 'Term'),
    sectional_class=('Sectional Class ID', 'Class Name', 'Semester ID', 'Subject ID', 'Major ID'),
    score=('Sectional Class ID', 'Student ID', 'Regular 1', 'Regular 2', 'Regular 3', 'Midterm', 'Final'),
    user=('User ID', 'Username', 'Password', 'Full Name', 'Email')
)

status = {
    "0": "Inactive",
    "1": "Active",
    "2": "Graduated",
    "-1": "Repeated"
}

gender_get = {
    1: True,
    0: False,
    -1: None
}

def gen_coeff_dict(reg1: float, reg2: float, reg3: float, midterm:float, final:float) -> dict:
    return {
        "reg1": reg1,
        "reg2": reg2,
        "reg3": reg3,
        "mid": midterm,
        "fin": final
    }
def gen_coeff_sn(reg1: float, reg2: float, reg3: float, midterm:float, final:float) -> SimpleNamespace:
    return SimpleNamespace(**gen_coeff_dict(reg1, reg2, reg3, midterm, final))

def gen_K(gen_int: int) -> str:
    """Sinh ra chuỗi 'K' + generation number"""
    return 'K' + str(gen_int)