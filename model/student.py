from model.major import Major
from model.classes import Class

class Student:
    def __init__(self, name:str, dob:dt.date , cid:str, phone:str, email:str, gender:int, img:str):
        self.name = name
        self.dob = dob
        self.cid = cid
        self.phone = phone
        self.email = email
        self.gender = gender
        self.img = img
        self.major = Major()
        self.class = Class()
