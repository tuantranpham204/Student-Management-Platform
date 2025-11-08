import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox

from tkcalendar import DateEntry
import util.util as util
import service.student as student_service
from types import SimpleNamespace as sn
import re

class StudentManagement(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.widgets()

    def widgets(self):

        self.fr_info = tk.Frame(self)
        # self.fr_info.grid_propagate(False)

        self.fr_lst = tk.Frame(self)

        # self.fr_info.config(width=100, height=100)
        # self.fr_lst.config(width=100, height=100)

        self.fr_info.grid(row=0, column=0, padx=10, pady=10)
        self.fr_lst.grid(row=1, column=0, padx=10, pady=10)


        # process student profile pic
        self.fr_pro5 = tk.Frame(self.fr_info)
        self.fr_pro5.grid(row=0, column=0, padx=10, pady=10)
        self.pro5_pic = tk.Canvas(self.fr_pro5, width=140, height=220)
        self.pro5_pic.grid(row=0, column=0, rowspan=6, padx=10, pady=10)

        self.btn_pro5_pic = tk.Button(self.fr_pro5, text='Select student profile picture')
        self.btn_pro5_pic.grid(row=1, column=0, padx=5, pady=5)

        # student input fields
        self.fr_inp = tk.Frame(self.fr_info)
        self.fr_inp.grid(row=0, column=1, padx=10, pady=10)
        
        self.lbl_sid = tk.Label(self.fr_inp, text='Student ID: ', anchor='w')
        self.lbl_sid.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ent_sid = tk.Entry(self.fr_inp, width=30)
        self.ent_sid.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_fname = tk.Label(self.fr_inp, text='First name: ', anchor='w')
        self.lbl_fname.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_fname = tk.Entry(self.fr_inp, width=30)
        self.ent_fname.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_lname = tk.Label(self.fr_inp, text='Last name: ', anchor='w')
        self.lbl_lname.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.ent_lname = tk.Entry(self.fr_inp, width=30)
        self.ent_lname.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_cid = tk.Label(self.fr_inp, text='Citizen ID: ', anchor='w')
        self.lbl_cid.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.ent_cid = tk.Entry(self.fr_inp, width=30)
        self.ent_cid.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_addr = tk.Label(self.fr_inp, text='Address: ', anchor='w')
        self.lbl_addr.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.ent_addr = tk.Entry(self.fr_inp, width=30)
        self.ent_addr.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_phone = tk.Label(self.fr_inp, text='Phone: ', anchor='w')
        self.lbl_phone.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        self.ent_phone = tk.Entry(self.fr_inp, width=30)
        self.ent_phone.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_email = tk.Label(self.fr_inp, text='Email: ', anchor='w')
        self.lbl_email.grid(row=6, column=0, padx=10, pady=10, sticky='w')
        self.ent_email = tk.Entry(self.fr_inp, width=30)
        self.ent_email.grid(row=6, column=1, padx=10, pady=10)

        self.lbl_gender = tk.Label(self.fr_inp, text='Gender: ', anchor='w')
        self.lbl_gender.grid(row=7, column=0, padx=10, pady=10, sticky='w')
        self.fr_rad_gender = tk.Frame(self.fr_inp, width=30)
        self.fr_rad_gender.grid(row=7, column=1, padx=10, pady=10)
        self.gender = tk.BooleanVar(value=True)
        self.rad_btn_m = tk.Radiobutton(self.fr_rad_gender, text='Male', variable=self.gender, value=True)
        self.rad_btn_m.grid(row=0, column=0, padx=10, pady=10)
        self.rad_btn_f = tk.Radiobutton(self.fr_rad_gender, text='Female', variable=self.gender, value=False)
        self.rad_btn_f.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_dob = tk.Label(self.fr_inp, text='Date of Birth: ', anchor='w')
        self.lbl_dob.grid(row=8, column=0, padx=10, pady=10, sticky='w')
        self.ent_dob = DateEntry(self.fr_inp, date_pattern="dd/mm/yyyy", anchor=tk.CENTER)
        self.ent_dob.grid(row=8, column=1, padx=10, pady=10)

        # uni info

        self.lbl_gen = tk.Label(self.fr_inp, text='Generation: ', anchor='w')
        self.lbl_gen.grid(row=0, column=2, padx=10, pady=10, sticky='w')
        self.gen_int = int()
        self.ent_gen =  tk.ttk.Combobox(self.fr_inp, textvariable=tk.StringVar(value=(util.gen_K(self.gen_int))), state='readonly', width=30)
        self.ent_gen.grid(row=0, column=3, padx=10, pady=10)

        self.lbl_status = tk.Label(self.fr_inp, text='Status: ', anchor='w')
        self.lbl_status.grid(row=1, column=2, padx=10, pady=10, sticky='w')
        self.ent_status = tk.Entry(self.fr_inp, width=30)
        self.status_int = int()
        self.sel_status = tk.ttk.Combobox(self.fr_inp, textvariable=tk.StringVar(value = util.status[str(self.status_int)]), state='readonly', width=30)
        self.sel_status.grid(row=1, column=3, padx=10, pady=10)

        self.lbl_maj = tk.Label(self.fr_inp, text='Major: ', anchor='w')
        self.lbl_maj.grid(row=3, column=2, padx=10, pady=10, sticky='w')
        self.maj = {"id": int(), "name": tk.StringVar()}
        self.sel_maj = tk.ttk.Combobox(self.fr_inp, textvariable=self.maj["name"], state='readonly', width=30)
        self.sel_maj.grid(row=3, column=3, padx=10, pady=10)

        self.lbl_dep = tk.Label(self.fr_inp, text='Department: ', anchor='w')
        self.lbl_dep.grid(row=2, column=2, padx=10, pady=10, sticky='w')
        self.dep = {"id": int(), "name": tk.StringVar()}
        self.sel_dep = tk.ttk.Combobox(self.fr_inp, textvariable=self.dep["name"], state='readonly', width=30)
        self.sel_dep.grid(row=2, column=3, padx=10, pady=10)

        self.lbl_dep_cls = tk.Label(self.fr_inp, text='Departmental class: ', anchor='w')
        self.lbl_dep_cls.grid(row=4, column=2, padx=10, pady=10, sticky='w')
        self.dep_cls = {"id": int(), "name": tk.StringVar()}
        self.sel_dep_cls = tk.ttk.Combobox(self.fr_inp, textvariable=self.dep_cls["name"], state='readonly', width=30)
        self.sel_dep_cls.grid(row=4, column=3, padx=10, pady=10)

        self.lbl_sec_cls = tk.Label(self.fr_inp, text='Sectional class: ', anchor='w')
        self.lbl_sec_cls.grid(row=5, column=2, padx=10, pady=10, sticky='w')
        self.sec_cls = [{"id": int(), "name": tk.StringVar()}]
        self.sel_sec_cls = tk.ttk.Combobox(self.fr_inp, textvariable=self.sec_cls[0]["name"], state='readonly', width=30)
        self.sel_sec_cls.grid(row=5, column=3, padx=10, pady=10)
        self.txt_sec_cls = tk.Text(self.fr_inp,width=40, height=1, state=tk.DISABLED)
        self.txt_sec_cls.grid(row=6, column=2, padx=10, pady=10, columnspan=2, sticky='w')

        self.fr_btn = tk.Frame(self.fr_inp)
        self.fr_btn.grid(row=7, column=2, padx=10, pady=10, columnspan=2, rowspan=2)

        self.btn_add = tk.Button(self.fr_btn, text='Add student', padx=10, pady=10, command=self.add_student)
        self.btn_add.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.btn_upd = tk.Button(self.fr_btn, text='Update student', padx=10, pady=10)
        self.btn_upd.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.btn_clr = tk.Button(self.fr_btn, text='Refresh', padx=10, pady=10)
        self.btn_clr.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.btn_search = tk.Button(self.fr_btn, text='Search student', padx=10, pady=10, command=self.search_student)
        self.btn_search.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        self.btn_xls = tk.Button(self.fr_btn, text='Extract to XLSX', padx=10, pady=10)
        self.btn_xls.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.btn_all = tk.Button(self.fr_btn, text='Get all student', padx=10, pady=10, command=self.get_all_students)
        self.btn_all.grid(row=2, column=1, padx=10, pady=10, sticky='nsew')



        # list frame

        self.lst = ttk.Treeview(self.fr_lst, columns=("ord",) + util.attrs.student, show='headings')
        self.lst.grid(row=1, column=0, sticky='nsew', columnspan=2)

        self.lst.heading("ord", text="Order")
        for head, attr in zip(util.headings.student, util.attrs.student):
            self.lst.heading(attr, text=head)

        col_width = ( self.parent.winfo_width() // len(util.attrs.student))

        self.lst.column('ord', width=50, stretch=True)
        for attr in util.attrs.student:
            self.lst.column(attr, width=col_width, stretch=True)
            # self.lst.column(attr, width=125, stretch=True)

        # Create scrollbars as children of self.fr_lst
        self.scrollbar_y = ttk.Scrollbar(self.fr_lst, orient="vertical", command=self.lst.yview)
        self.scrollbar_x = ttk.Scrollbar(self.fr_lst, orient="horizontal", command=self.lst.xview)

        # Place scrollbars in the grid
        self.scrollbar_y.grid(row=1, column=1, sticky='ns')  # Next to the list (column 1)
        self.scrollbar_x.grid(row=2, column=0, sticky='ew')  # Below the list (row 2)

        # Configure the Treeview to use them
        self.lst.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        # Make the grid row/column containing the Treeview expandable
        # This is key for the scrollbars to work as the window resizes
        self.fr_lst.grid_rowconfigure(1, weight=1)
        self.fr_lst.grid_columnconfigure(0, weight=1)


    def categorize(self, students_sn:list):
        for student in students_sn:
            if student.gender == False:
                student.gender = 'Female'
            else: student.gender = 'Male'
            student.generation = util.gen_K(student.generation)
        return students_sn

    def validate(self):
        email = self.ent_email.get().strip()
        phone = self.ent_phone.get().strip()
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror(title='Invalid Email', message='Please enter a valid email address.')
        if phone and not re.match(r'^\d+$', phone):
            messagebox.showerror(title='Invalid Phone', message='Please enter a valid phone number.')


    def get_all_students(self):
        self.empty_lst()
        students_sn = student_service.get_all_students()
        students_sn = self.categorize(students_sn)
        students = [vars(student) for student in students_sn]
        for i in range(len(students)):
            self.lst.insert('',tk.END,values=((i+1, )+tuple(students[i].values())))

    def add_student(self):
        self.validate()

    def empty_lst(self):
        self.lst.delete(*self.lst.get_children())

    def search_student(self):
        self.empty_lst()
        self.validate()
        student_inp = self.get_student_by_entries()
        students = [vars(student) for student in student_service.get_student_by_params(student_inp)]
        for i in range(len(students)):
            self.lst.insert('', tk.END, values=((i + 1,) + tuple(students[i].values())))

    def get_student_by_entries(self):
        student = {
            "sid": self.ent_sid.get() or None,
            "fname": self.ent_fname.get() or None,
            "lname": self.ent_lname.get() or None,
            "cid": self.ent_cid.get() or None,
            "address": self.ent_addr.get() or None,
            "phone": self.ent_phone.get() or None,
            "email": self.ent_email.get() or None,
            "gender": self.gender.get() or None,
            "dob": None,
            "generation": None,
            "status": self.sel_status.get() or None,
            "departmental_class_id": None
        }
        return student



if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    management = StudentManagement(root)
    management.grid(column=0, row=0)
    root.mainloop()
