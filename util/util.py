import os
from dotenv import load_dotenv
from types import SimpleNamespace as sn

load_dotenv()

default_vals = sn({
  "DEFAULT_BG_COLOR" : os.getenv("DEFAULT_BG_COLOR"),
})

attrs = sn({
  'student' : ('sid', 'fname', 'lname', 'dob', 'address', 'cid', 'phone', 'email', 'gender', 'generation', 'status' ,'img' , 'departmental_class_id')
})

headings = sn({
  'student' : ('Student ID', 'First name', 'Last name', 'Date of birth', 'Address', 'Citizen ID', 'Phone number', 'Email', 'Gender', 'Generation', 'Status', 'Image Directory', 'Departmental class')

})



status = {
  "0": "inactive",
  "1": "active",
  "2": "graduated",
  "-1": "repeated"
}

def gen_K(gen_int:int) -> str:
  return 'K' + str(gen_int)