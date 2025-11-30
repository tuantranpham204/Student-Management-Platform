import os
from dotenv import load_dotenv
from types import SimpleNamespace

# Load .env file
load_dotenv()

# SimpleNamespace sử dụng keyword arguments, không nhận dict trực tiếp
default_vals = SimpleNamespace(
    DEFAULT_BG_COLOR=os.getenv("DEFAULT_BG_COLOR")
)

attrs = SimpleNamespace(
    student=('sid', 'fname', 'lname', 'dob', 'address', 'cid', 'phone', 'email', 'gender', 'generation', 'status', 'img', 'departmental_class_id')
)

headings = SimpleNamespace(
    student=('Student ID', 'First name', 'Last name', 'Date of birth', 'Address', 'Citizen ID',
             'Phone number', 'Email', 'Gender', 'Generation', 'Status', 'Image Directory', 'Departmental class')
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

def gen_K(gen_int: int) -> str:
    """Sinh ra chuỗi 'K' + generation number"""
    return 'K' + str(gen_int)