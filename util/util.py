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
  "0": "Inactive",
  "1": "Active",
  "2": "Graduated",
  "-1": "Repeated"
}

gender_get = {
  1 : True,
  0: False,
  -1: None
}

def gen_K(gen_int ) -> str:
  return 'K' + str(gen_int)