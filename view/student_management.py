import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import util.util as util
import service.student as student_service
import service.department as department_service
import service.major as major_service
import service.departmental_class as dep_cls_service
import service.sectional_class as sec_cls_service
from util.global_exception_handler import handle_exceptions
from types import SimpleNamespace as sn
import re
import pandas as pd
from datetime import datetime
from PIL import Image, ImageTk
import shutil
import csv
from fpdf import FPDF  # Import fpdf library


class StudentManagement(tk.Frame):
    def __init__(self, parent, back_callback=None):
        self.parent = parent
        self.back_callback = back_callback  # Store the callback
        super().__init__(parent)

        # Store service data
        self.departments = []
        self.majors = []
        self.dep_classes = []
        self.sec_classes = []

        # Dictionaries to map names back to IDs
        self.dep_name_to_id = {}
        self.maj_name_to_id = {}
        self.cls_name_to_id = {}
        self.status_name_to_id = {v: k for k, v in util.status.items()}
        self.gen_name_to_id = {}  # For K17 -> 17

        self.widgets()
        self.init_pro5_pic()
        self.populate_comboboxes()
        self.get_all_students()

    def widgets(self):
        self.fr_info = tk.Frame(self)
        self.fr_lst = tk.Frame(self)

        self.fr_info.grid(row=0, column=0, padx=10, pady=10)
        self.fr_lst.grid(row=1, column=0, padx=10, pady=10)

        # Configure grid weights for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # === Student Profile Pic ===
        self.fr_pro5 = tk.Frame(self.fr_info)
        self.fr_pro5.grid(row=0, column=0, padx=10, pady=10)
        self.pro5_pic = tk.Canvas(self.fr_pro5, width=140, height=220, bg="lightgrey", relief="solid", borderwidth=1)
        self.pro5_pic.grid(row=0, column=0, rowspan=6, padx=10, pady=10)
        self.pro5_pic.create_text(70, 110, text="No Image", fill="grey")

        self.btn_pro5_pic = tk.Button(self.fr_pro5, text='Select student profile picture', command=self.select_image)
        self.btn_pro5_pic.grid(row=6, column=0, padx=5, pady=5)
        self.img_path = tk.StringVar()

        # === Student Input Fields ===
        self.fr_inp = tk.Frame(self.fr_info)
        self.fr_inp.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        col1 = 0
        col2 = 1
        col3 = 2
        col4 = 3

        # --- Column 1 & 2 (Personal Info) ---
        self.lbl_sid = tk.Label(self.fr_inp, text='Student ID: ', anchor='w')
        self.lbl_sid.grid(row=0, column=col1, padx=10, pady=10, sticky='w')
        self.ent_sid = tk.Entry(self.fr_inp, width=30)
        self.ent_sid.grid(row=0, column=col2, padx=10, pady=10)

        self.lbl_fname = tk.Label(self.fr_inp, text='First name: ', anchor='w')
        self.lbl_fname.grid(row=1, column=col1, padx=10, pady=10, sticky='w')
        self.ent_fname = tk.Entry(self.fr_inp, width=30)
        self.ent_fname.grid(row=1, column=col2, padx=10, pady=10)

        self.lbl_lname = tk.Label(self.fr_inp, text='Last name: ', anchor='w')
        self.lbl_lname.grid(row=2, column=col1, padx=10, pady=10, sticky='w')
        self.ent_lname = tk.Entry(self.fr_inp, width=30)
        self.ent_lname.grid(row=2, column=col2, padx=10, pady=10)

        self.lbl_dob = tk.Label(self.fr_inp, text='Date of Birth: ', anchor='w')
        self.lbl_dob.grid(row=3, column=col1, padx=10, pady=10, sticky='w')
        self.ent_dob = DateEntry(self.fr_inp, date_pattern="yyyy-mm-dd", anchor=tk.CENTER, width=27)
        self.ent_dob.grid(row=3, column=col2, padx=10, pady=10)
        self.search_dob_var = tk.BooleanVar(value=False)
        self.chk_dob = tk.Checkbutton(self.fr_inp, text="Searchable", variable=self.search_dob_var)
        self.chk_dob.grid(row=4, column=col2, padx=10, pady=10, sticky='w')

        self.lbl_gender = tk.Label(self.fr_inp, text='Gender: ', anchor='w')
        self.lbl_gender.grid(row=5, column=col1, padx=10, pady=10, sticky='w')
        self.fr_rad_gender = tk.Frame(self.fr_inp)
        self.fr_rad_gender.grid(row=5, column=col2, padx=10, pady=10, sticky='w')
        self.gender = tk.IntVar(value=-1)
        self.rad_btn_m = tk.Radiobutton(self.fr_rad_gender, text='Male', variable=self.gender, value=0)
        self.rad_btn_m.grid(row=0, column=0, padx=5, pady=2)
        self.rad_btn_f = tk.Radiobutton(self.fr_rad_gender, text='Female', variable=self.gender, value=1)
        self.rad_btn_f.grid(row=0, column=1, padx=10, pady=2)
        self.rad_btn_any = tk.Radiobutton(self.fr_rad_gender, text='Any', variable=self.gender, value=-1)
        self.rad_btn_any.grid(row=0, column=2, padx=5, pady=10)

        self.lbl_cid = tk.Label(self.fr_inp, text='Citizen ID: ', anchor='w')
        self.lbl_cid.grid(row=6, column=col1, padx=10, pady=10, sticky='w')
        self.ent_cid = tk.Entry(self.fr_inp, width=30)
        self.ent_cid.grid(row=6, column=col2, padx=10, pady=10)

        self.lbl_addr = tk.Label(self.fr_inp, text='Address: ', anchor='w')
        self.lbl_addr.grid(row=7, column=col1, padx=10, pady=10, sticky='w')
        self.ent_addr = tk.Entry(self.fr_inp, width=30)
        self.ent_addr.grid(row=7, column=col2, padx=10, pady=10)

        self.lbl_phone = tk.Label(self.fr_inp, text='Phone: ', anchor='w')
        self.lbl_phone.grid(row=8, column=col1, padx=10, pady=10, sticky='w')
        self.ent_phone = tk.Entry(self.fr_inp, width=30)
        self.ent_phone.grid(row=8, column=col2, padx=10, pady=10)

        self.lbl_email = tk.Label(self.fr_inp, text='Email: ', anchor='w')
        self.lbl_email.grid(row=9, column=col1, padx=10, pady=10, sticky='w')
        self.ent_email = tk.Entry(self.fr_inp, width=30)
        self.ent_email.grid(row=9, column=col2, padx=10, pady=10)

        # --- Column 3 & 4 (University Info) ---
        self.lbl_dep = tk.Label(self.fr_inp, text='Department: ', anchor='w')
        self.lbl_dep.grid(row=0, column=col3, padx=10, pady=10, sticky='w')
        self.sel_dep_var = tk.StringVar()
        self.sel_dep = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_dep_var, state='readonly', width=27)
        self.sel_dep.grid(row=0, column=col4, padx=10, pady=10)
        self.sel_dep.bind("<<ComboboxSelected>>", self.on_department_select)

        self.lbl_maj = tk.Label(self.fr_inp, text='Major: ', anchor='w')
        self.lbl_maj.grid(row=1, column=col3, padx=10, pady=10, sticky='w')
        self.sel_maj_var = tk.StringVar()
        self.sel_maj = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_maj_var, state='disable', width=27)
        self.sel_maj.grid(row=1, column=col4, padx=10, pady=10)
        self.sel_maj.bind("<<ComboboxSelected>>", self.on_major_select)

        self.lbl_dep_cls = tk.Label(self.fr_inp, text='Departmental class: ', anchor='w')
        self.lbl_dep_cls.grid(row=2, column=col3, padx=10, pady=10, sticky='w')
        self.sel_dep_cls_var = tk.StringVar()
        self.sel_dep_cls = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_dep_cls_var, state='disable', width=27)
        self.sel_dep_cls.grid(row=2, column=col4, padx=10, pady=10)

        self.lbl_gen = tk.Label(self.fr_inp, text='Generation: ', anchor='w')
        self.lbl_gen.grid(row=3, column=col3, padx=10, pady=10, sticky='w')
        self.sel_gen_var = tk.StringVar()
        self.ent_gen = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_gen_var, state='readonly', width=27)
        self.ent_gen.grid(row=3, column=col4, padx=10, pady=10)

        self.lbl_status = tk.Label(self.fr_inp, text='Status: ', anchor='w')
        self.lbl_status.grid(row=4, column=col3, padx=10, pady=10, sticky='w')
        self.sel_status_var = tk.StringVar()
        self.sel_status = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_status_var, state='readonly', width=27)
        self.sel_status.grid(row=4, column=col4, padx=10, pady=10)

        self.lbl_sec_cls = tk.Label(self.fr_inp, text='Sectional Class: ', anchor='w')
        self.lbl_sec_cls.grid(row=5, column=col3, padx=10, pady=10, sticky='w')
        self.sel_sec_cls_var = tk.StringVar()
        self.sel_sec_cls = tk.ttk.Combobox(self.fr_inp, textvariable=self.sel_sec_cls_var, state='readonly', width=27)
        self.sel_sec_cls.grid(row=5, column=col4, padx=10, pady=10)

        # ================= BUTTON LAYOUT =================
        self.fr_btn = tk.Frame(self.fr_inp)
        self.fr_btn.grid(row=6, column=col3, padx=10, pady=10, columnspan=2, rowspan=4,
                         sticky='nsew')  # Changed rowspan to 4

        # Configure columns for 3-button layout
        self.fr_btn.grid_columnconfigure(0, weight=1)
        self.fr_btn.grid_columnconfigure(1, weight=1)
        self.fr_btn.grid_columnconfigure(2, weight=1)

        # Row 1: Actions (Add, Update, Refresh)
        self.btn_add = tk.Button(self.fr_btn, text='Add student', padx=10, pady=5, command=self.add_student)
        self.btn_add.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.btn_upd = tk.Button(self.fr_btn, text='Update student', padx=10, pady=5, command=self.update_student)
        self.btn_upd.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        self.btn_clr = tk.Button(self.fr_btn, text='Refresh Form', padx=10, pady=5, command=self.clear_entries)
        self.btn_clr.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')

        # Row 2: Data Tools (Search, All, Extract)
        self.btn_search = tk.Button(self.fr_btn, text='Search Student', padx=10, pady=5, command=self.search_student)
        self.btn_search.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.btn_all = tk.Button(self.fr_btn, text='Get All Students', padx=10, pady=5, command=self.get_all_students)
        self.btn_all.grid(row=1, column=1, padx=5, pady=5, sticky='nsew')

        self.btn_xls = tk.Button(self.fr_btn, text='Extract to CSV', padx=10, pady=5, command=self.export_to_csv)
        self.btn_xls.grid(row=1, column=2, padx=5, pady=5, sticky='nsew')

        # Row 3: PDF Export (New Button)
        self.btn_pdf = tk.Button(self.fr_btn, text='Extract to PDF', padx=10, pady=5, command=self.export_to_pdf)
        self.btn_pdf.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')

        # Row 4: Exit (Full width)
        self.btn_exit = tk.Button(self.fr_btn, text='Exit', padx=10, pady=5, command=self.go_back, bg='#FF6B6B',
                                  fg='white')
        self.btn_exit.grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky='nsew')
        # =====================================================

        # === List Frame (Treeview) ===
        self.lst = ttk.Treeview(self.fr_lst, columns=("ord",) + util.attrs.student, show='headings')
        self.lst.grid(row=0, column=0, sticky='nsew')

        self.lst.heading("ord", text="Order")
        for head, attr in zip(util.headings.student, util.attrs.student):
            self.lst.heading(attr, text=head)

        self.lst.column('ord', width=40, stretch=False)
        self.lst.column('sid', width=80, stretch=False)
        self.lst.column('fname', width=100)
        self.lst.column('lname', width=120)
        self.lst.column('dob', width=80, stretch=False)
        self.lst.column('gender', width=60, stretch=False)
        self.lst.column('generation', width=70, stretch=False)
        self.lst.column('status', width=70, stretch=False)
        self.lst.column('departmental_class_id', width=120)
        self.lst.column('img', width=0, stretch=False)
        self.lst.column('address', width=0, stretch=False)
        self.lst.column('cid', width=0, stretch=False)
        self.lst.column('phone', width=0, stretch=False)
        self.lst.column('email', width=0, stretch=False)

        # --- Scrollbars ---
        self.scrollbar_y = ttk.Scrollbar(self.fr_lst, orient="vertical", command=self.lst.yview)
        self.scrollbar_x = ttk.Scrollbar(self.fr_lst, orient="horizontal", command=self.lst.xview)
        self.scrollbar_y.grid(row=0, column=1, sticky='ns')
        self.scrollbar_x.grid(row=1, column=0, sticky='ew')
        self.lst.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.fr_lst.grid_rowconfigure(0, weight=1)
        self.fr_lst.grid_columnconfigure(0, weight=1)

        self.lst.bind("<<TreeviewSelect>>", self.load_student_data)

    def init_pro5_pic(self):
        """Initialize image directory paths."""
        # Calculate Project Root (parent of the 'view' folder)
        self.PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

        # Define the relative path structure
        self.PROFILE_PIC_RELATIVE_DIR = os.path.join("public", "profile_pictures")

        # Define the full absolute path for file operations
        self.PROFILE_PIC_DIR = os.path.join(self.PROJECT_ROOT, self.PROFILE_PIC_RELATIVE_DIR)

        try:
            os.makedirs(self.PROFILE_PIC_DIR, exist_ok=True)
        except OSError as e:
            print(f"Error creating profile pic directory: {e}")
            messagebox.showerror("IO Error", "Could not create image directory.")
        self.img_path_src = None

    def go_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            self.parent.quit()

    def select_item_by_sid(self, sid):
        """Helper to find and select a row by Student ID to trigger auto-fill."""
        if not sid: return
        for item in self.lst.get_children():
            values = self.lst.item(item, 'values')
            # values[1] is the SID column based on column definition
            if str(values[1]) == str(sid):
                self.lst.selection_set(item)
                self.lst.focus(item)
                self.lst.see(item)  # Scroll to item

                # Manually trigger load since selection_set doesn't always trigger the event automatically in code
                self.load_student_data()
                return

    @handle_exceptions(default_return_value=[])
    def populate_comboboxes(self):
        self.sel_status['values'] = list(util.status.values())
        gens = [util.gen_K(i) for i in range(10, 25)]
        self.gen_name_to_id = {name: int(name[1:]) for name in gens}
        self.ent_gen['values'] = gens
        self.departments = department_service.get_all_departments()
        dep_names = [dep.name for dep in self.departments]
        self.dep_name_to_id = {dep.name: dep.id for dep in self.departments}
        self.sel_dep['values'] = dep_names

    @handle_exceptions()
    def on_department_select(self, event=None):
        dep_id = self.dep_name_to_id.get(self.sel_dep_var.get())
        if not dep_id:
            self.sel_maj['values'] = []
            self.sel_dep_cls['values'] = []
            return
        self.sel_maj.config(state='readonly')
        self.majors = major_service.get_majors_by_department(dep_id)
        maj_names = [maj.name for maj in self.majors]
        self.maj_name_to_id = {maj.name: maj.id for maj in self.majors}
        self.sel_maj['values'] = maj_names
        self.sel_maj_var.set('')
        self.sel_dep_cls_var.set('')

    @handle_exceptions()
    def on_major_select(self, event=None):
        maj_id = self.maj_name_to_id.get(self.sel_maj_var.get())
        if not maj_id:
            self.sel_dep_cls['values'] = []
            return
        self.sel_dep_cls.config(state='readonly')
        self.dep_classes = dep_cls_service.get_classes_by_major(maj_id)
        dep_cls_names = [cls.name for cls in self.dep_classes]
        self.cls_name_to_id = {cls.name: cls.id for cls in self.dep_classes}
        self.sel_dep_cls['values'] = dep_cls_names
        self.sel_dep_cls_var.set('')

        self.sel_sec_cls.config(state='readonly')
        self.sec_classes = sec_cls_service.get_classes_by_major_id(maj_id)
        sec_cls_names = [cls.name for cls in self.sec_classes]
        self.sel_sec_cls['values'] = sec_cls_names
        self.sel_sec_cls_var.set('')

    def categorize(self, students_sn: list):
        for student in students_sn:
            student.gender = 'Female' if student.gender == 0 else 'Male'
            student.generation = util.gen_K(student.generation)
            student.status = util.status.get(str(student.status), "Unknown")
        return students_sn

    def validate(self, check_sid=True):
        sid = self.ent_sid.get().strip()
        fname = self.ent_fname.get().strip()
        lname = self.ent_lname.get().strip()
        email = self.ent_email.get().strip()
        phone = self.ent_phone.get().strip()

        if check_sid and not sid:
            messagebox.showerror(title='Validation Error', message='Student ID is required.')
            return False
        if not fname or not lname:
            messagebox.showerror(title='Validation Error', message='First Name and Last Name are required.')
            return False
        if email and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            messagebox.showerror(title='Invalid Email', message='Please enter a valid email address.')
            return False
        if phone and not re.match(r'^\d+$', phone):
            messagebox.showerror(title='Invalid Phone', message='Please enter a valid phone number.')
            return False
        return True

    def empty_lst(self):
        self.lst.delete(*self.lst.get_children())

    def clear_entries(self):
        self.ent_sid.config(state='normal')
        self.ent_sid.delete(0, tk.END)
        self.ent_fname.delete(0, tk.END)
        self.ent_lname.delete(0, tk.END)
        self.ent_cid.delete(0, tk.END)
        self.ent_addr.delete(0, tk.END)
        self.ent_phone.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
        self.ent_dob.set_date(datetime.now())
        self.gender.set(True)
        self.sel_gen_var.set('')
        self.sel_status_var.set('')
        self.sel_dep_var.set('')
        self.sel_maj_var.set('')
        self.sel_maj['values'] = []
        self.sel_dep_cls_var.set('')
        self.sel_dep_cls['values'] = []
        self.img_path.set('')
        self.img_path_src = None
        self.pro5_pic.delete("all")
        self.pro5_pic.create_text(70, 110, text="No Image", fill="grey")
        self.lst.selection_remove(self.lst.selection())

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg *.gif")])
        if path:
            self.img_path_src = path
            self.img_path.set(path)
            try:
                self.pro5_pic.delete("all")
                pro5_pic = Image.open(path).resize((140, 220))
                self._pro5_pic_new = ImageTk.PhotoImage(pro5_pic)
                self.pro5_pic.create_image(0, 0, anchor=tk.NW, image=self._pro5_pic_new)
            except Exception as e:
                print(f"Error loading selected image: {e}")
                self.pro5_pic.delete("all")
                self.pro5_pic.create_text(70, 110, text="Load Error", fill="red")

    def handle_image_save(self, sid):
        """Save image with relative path handling."""
        # Case 1: User selected a NEW image (self.img_path_src is set)
        if self.img_path_src and os.path.exists(self.img_path_src):
            try:
                _, ext = os.path.splitext(self.img_path_src)
                if not ext: ext = ".jpg"

                # Create standard filename: studentID.extension
                new_filename = f"{sid}{ext.lower()}"

                # Destination: Absolute path for copying
                dest_path = os.path.join(self.PROFILE_PIC_DIR, new_filename)

                # Copy the file
                shutil.copy(self.img_path_src, dest_path)

                # Return RELATIVE path for database storage
                # This makes the DB portable (e.g. "public/profile_pictures/123.jpg")
                rel_path = os.path.join(self.PROFILE_PIC_RELATIVE_DIR, new_filename)
                return rel_path.replace("\\", "/")
            except Exception as e:
                messagebox.showerror("Image Save Error", f"Could not save image: {e}")
                return self.img_path.get() or None

        # Case 2: No new image selected, return the existing path (hidden field)
        return self.img_path.get() or None

    def get_student_from_entries(self) -> sn:
        sid = self.ent_sid.get().strip() or None
        fname = self.ent_fname.get().strip() or None
        lname = self.ent_lname.get().strip() or None
        dob = self.ent_dob.get_date().strftime("%Y-%m-%d")
        address = self.ent_addr.get().strip() or None
        cid = self.ent_cid.get().strip() or None
        phone = self.ent_phone.get().strip() or None
        email = self.ent_email.get().strip() or None
        gender = self.gender.get()
        gen_str = self.sel_gen_var.get()
        generation = self.gen_name_to_id.get(gen_str)
        status_str = self.sel_status_var.get()
        status = self.status_name_to_id.get(status_str)
        cls_str = self.sel_dep_cls_var.get()
        departmental_class_id = self.cls_name_to_id.get(cls_str)

        student = sn(
            sid=sid, fname=fname, lname=lname, dob=dob, address=address,
            cid=cid, phone=phone, email=email, gender=gender,
            generation=generation, status=status, img=None,
            departmental_class_id=departmental_class_id
        )
        return student

    @handle_exceptions()
    def load_student_data(self, event=None):
        selected_item = self.lst.selection()
        if not selected_item:
            return

        self.clear_entries()
        item = self.lst.item(selected_item)
        values = item['values']
        data = dict(zip(("ord",) + util.attrs.student, values))

        # Fetch full student object from service
        student = student_service.get_student_by_sid(data['sid'])
        if not student:
            messagebox.showerror("Error", "Could not fetch student details.")
            return

        # --- Fill Text Entries ---
        self.ent_sid.insert(0, student.sid)
        self.ent_sid.config(state='disabled')
        self.ent_fname.insert(0, student.fname)
        self.ent_lname.insert(0, student.lname)
        self.ent_cid.insert(0, student.cid or "")
        self.ent_addr.insert(0, student.address or "")
        self.ent_phone.insert(0, student.phone or "")
        self.ent_email.insert(0, student.email or "")
        self.ent_dob.set_date(student.dob)

        # --- Fill Comboboxes/Radios ---
        self.gender.set(student.gender)
        self.sel_gen_var.set(util.gen_K(student.generation))
        self.sel_status_var.set(util.status.get(str(student.status), ""))

        # --- Handle Class/Major Hierarchy ---
        self.sel_sec_cls.config(state='disabled')
        if student.departmental_class_id:
            try:
                s_dep_cls = dep_cls_service.get_class_by_id(student.departmental_class_id)
                self.sel_dep_cls_var.set(s_dep_cls.name)
                s_major = major_service.get_major_by_dep_cls_id(s_dep_cls.id)
                self.sel_maj_var.set(s_major.name)
                s_dep = department_service.get_department_by_major_id(s_major.id)
                self.sel_dep_var.set(s_dep.name)
            except (StopIteration, AttributeError):
                pass

        # --- IMAGE LOADING LOGIC ---
        self.pro5_pic.delete("all")
        self.img_path_src = None  # Reset source selection

        if not student.img:
            # Case 1: No Image Path in DB
            self.pro5_pic.create_text(70, 110, text="No Image", fill="grey")
            self.img_path.set("")
        else:
            # Save the DB path to hidden var for updates
            self.img_path.set(student.img)

            # Resolve the full path
            if os.path.isabs(student.img):
                full_path = student.img
            else:
                full_path = os.path.join(self.PROJECT_ROOT, student.img)

            # Check if file actually exists
            if not os.path.exists(full_path):
                # Case 2: Path exists in DB, but file is missing
                self.pro5_pic.create_text(70, 110, text="Image Not Found", fill="red")
            else:
                # Case 3: Image found, load and display
                try:
                    pil_image = Image.open(full_path)
                    # Resize with ANTIALIAS (LANCZOS)
                    pil_image = pil_image.resize((140, 220), Image.Resampling.LANCZOS)
                    self._pro5_pic_tk = ImageTk.PhotoImage(pil_image)
                    self.pro5_pic.create_image(0, 0, anchor=tk.NW, image=self._pro5_pic_tk)
                except Exception as e:
                    print(f"Error loading valid image path: {e}")
                    self.pro5_pic.create_text(70, 110, text="File Error", fill="red")

    def get_students_from_entries_as_dict(self) -> dict:
        student_inp = {
            "sid": self.ent_sid.get().strip() or None,
            "fname": self.ent_fname.get().strip() or None,
            "lname": self.ent_lname.get().strip() or None,
            "cid": self.ent_cid.get().strip() or None,
            "address": self.ent_addr.get().strip() or None,
            "phone": self.ent_phone.get().strip() or None,
            "email": self.ent_email.get().strip() or None,
            "dob": self.ent_dob.get(),
            "gender": util.gender_get[self.gender.get()],
            "generation": self.gen_name_to_id.get(self.sel_gen_var.get()),
            "status": self.status_name_to_id.get(self.sel_status_var.get()),
            "departmental_class_id": self.cls_name_to_id.get(self.sel_dep_cls_var.get()),
            "img": self.img_path.get() or None  # Pass img to search params just in case
        }
        return student_inp

    def is_at_least_1_field_entered(self, inp) -> bool:
        is_at_least_1_field_entered = False
        for field in inp.values():
            if field is not None:
                is_at_least_1_field_entered = True
                break
        if not is_at_least_1_field_entered:
            messagebox.showerror("Error", "Student entries must have at least 1 field entered.")
        return is_at_least_1_field_entered

    @handle_exceptions()
    def get_all_students(self):
        self.empty_lst()
        students_sn = student_service.get_all_students()
        students_sn = self.categorize(students_sn)
        students = [vars(student) for student in students_sn]
        for i in range(len(students)):
            self.lst.insert('', tk.END, values=((i + 1,) + tuple(students[i].values())))
        self.clear_entries()

    @handle_exceptions()
    def add_student(self):
        if not self.validate(check_sid=True):
            return
        student = self.get_student_from_entries()
        if student.gender is None and not all(
                [student.sid, student.fname, student.lname, student.gender, student.dob, student.generation,
                 student.status, student.departmental_class_id]):
            messagebox.showerror("Error",
                                 "Please fill all required fields (ID, Name, DOB, Gender, Generation, Status, Class).")
            return
        student.img = self.handle_image_save(student.sid)
        try:
            student_service.add_student(student)
            messagebox.showinfo("Success", f"Student {student.fname} {student.lname} added successfully.")
            self.get_all_students()

            # Select the student to show the image/details immediately
            self.select_item_by_sid(student.sid)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to add student.\nError: {e}")

    @handle_exceptions()
    def update_student(self):
        if not self.validate(check_sid=False):
            return
        if not self.ent_sid.get():
            messagebox.showerror("Error", "Please select a student from the list to update.")
            return
        student = self.get_student_from_entries()
        student.img = self.handle_image_save(student.sid)
        try:
            student_service.update_student(vars(student))
            messagebox.showinfo("Success", f"Student {student.fname} {student.lname} updated successfully.")
            self.get_all_students()

            # Select the student to show the image/details immediately
            self.select_item_by_sid(student.sid)

        except Exception as e:
            messagebox.showerror("Database Error", f"Failed to update student.\nError: {e}")

    @handle_exceptions()
    def search_student(self):
        self.empty_lst()
        student_inp = self.get_students_from_entries_as_dict()
        if self.search_dob_var.get() == False:
            student_inp["dob"] = None
        if not self.is_at_least_1_field_entered(student_inp): return
        students_sn = student_service.get_student_by_params(student_inp)
        students_sn = self.categorize(students_sn)
        students = [vars(student) for student in students_sn]
        for i in range(len(students)):
            self.lst.insert('', tk.END, values=((i + 1,) + tuple(students[i].values())))

    # UPDATED: Use CSV instead of Excel to avoid openpyxl dependency and fix data formatting issues
    @handle_exceptions()
    def export_to_csv(self):
        if not self.lst.get_children():
            messagebox.showwarning("Export Error", "There is no data to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )

        if not filepath:
            return

        try:
            # Use 'headings' for nice readable headers
            headers = ["Order"] + list(util.headings.student)

            # Filter out unwanted columns (Image Directory, etc) before writing
            unwanted_headers = ['Image Directory', 'Address', 'Citizen ID', 'Phone number', 'Email']

            # Create a list of indices to KEEP
            indices_to_keep = [i for i, h in enumerate(headers) if h not in unwanted_headers]
            final_headers = [headers[i] for i in indices_to_keep]

            with open(filepath, mode='w', newline='', encoding='utf-8-sig') as file:
                writer = csv.writer(file)
                writer.writerow(final_headers)

                for item in self.lst.get_children():
                    row_values = self.lst.item(item)['values']

                    # Convert everything to string to be safe
                    full_row = [str(x) for x in row_values]

                    # Write only the columns we decided to keep
                    filtered_row = [full_row[i] for i in indices_to_keep]
                    writer.writerow(filtered_row)

            messagebox.showinfo("Export Success", f"Data exported successfully to\n{filepath}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data.\nError: {e}")

    @handle_exceptions()
    def export_to_pdf(self):
        if not self.lst.get_children():
            messagebox.showwarning("Export Error", "There is no data to export.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )

        if not filepath:
            return

        try:
            # Initialize PDF
            pdf = FPDF()
            pdf.add_page()
            # If you need Unicode characters (like Vietnamese), you must add a font that supports it.
            # Assuming standard Arial for now, but note standard FPDF doesn't support UTF-8 well without a TTF font.
            # For simplicity, let's use the built-in Arial font (standard ASCII).
            # If you need UTF-8, you'd need to load a font like DejaVuSans.
            # Example: pdf.add_font('DejaVu', '', 'DejaVuSans.ttf', uni=True)
            # pdf.set_font('DejaVu', '', 10)

            # Using Arial (might not show Vietnamese accents correctly without a custom font)
            pdf.set_font("Arial", size=10)

            # Title
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(200, 10, txt="Student List", ln=True, align='C')
            pdf.ln(10)

            # Define Columns to Export (same logic as CSV)
            headers = ["Order"] + list(util.headings.student)
            unwanted_headers = ['Image Directory', 'Address', 'Citizen ID', 'Phone number', 'Email']
            indices_to_keep = [i for i, h in enumerate(headers) if h not in unwanted_headers]
            final_headers = [headers[i] for i in indices_to_keep]

            # Table Header
            pdf.set_font("Arial", 'B', 10)

            # Simple fixed width calculation (adjust as needed)
            col_width = 190 / len(final_headers)

            for header in final_headers:
                # Truncate header if too long
                display_header = (header[:15] + '..') if len(header) > 15 else header
                pdf.cell(col_width, 10, display_header, border=1)
            pdf.ln()

            # Table Data
            pdf.set_font("Arial", size=9)
            for item in self.lst.get_children():
                row_values = self.lst.item(item)['values']
                full_row = [str(x) for x in row_values]
                filtered_row = [full_row[i] for i in indices_to_keep]

                for datum in filtered_row:
                    # Basic sanitization for standard FPDF (latin-1)
                    # This replaces non-latin-1 chars to prevent crashes, but won't show them correctly.
                    # Ideally, you should bundle a .ttf font for full UTF-8 support.
                    safe_datum = str(datum).encode('latin-1', 'replace').decode('latin-1')

                    # Truncate cell content if too long
                    display_datum = (safe_datum[:18] + '..') if len(safe_datum) > 18 else safe_datum
                    pdf.cell(col_width, 10, display_datum, border=1)
                pdf.ln()

            pdf.output(filepath)
            messagebox.showinfo("Export Success", f"Data exported successfully to\n{filepath}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export data.\nError: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(True, True)
    management = StudentManagement(root)
    management.grid(column=0, row=0, sticky='nsew')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()