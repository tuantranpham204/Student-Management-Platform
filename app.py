from types import SimpleNamespace as sn
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
import pandas as pd
from fpdf import FPDF
import os

# Import all services
import service.student as student_service
import service.user as user_service
import service.department as department_service
import service.major as major_service
import service.departmental_class as departmental_class_service
import service.subject as subject_service
import service.score as score_service

# Import the exception handler
from util.global_exception_handler import handle_exceptions

# Import views (assuming they are in a 'views' folder)
from views import LoginView, AdminDashboardView, StudentView, SubjectView, TopLeveSubjectlView


class AppController:
    def __init__(self, root):
        self.root = root
        self.root.title('Student Management')
        self.root.geometry("1280x800")
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.configure(bg='#C8EBF3')

        self.user_name = None  # Store username after login

        self.show_login_view('<Button-1>')

    def show_login_view(self, event):
        self.clear_frame()
        self.login_view = LoginView(self.root)
        self.login_view.grid(row=0, column=0)
        self.login_view.configure(width=800, height=500)
        self.login_view.checkbtn_showpw.bind('<Button-1>', self.show_password)
        self.login_view.btn_login.bind('<Button-1>', self.valid_account)

    @handle_exceptions(default_return_value=None)
    def valid_account(self, event):
        self.user_name = self.login_view.ent_us.get()
        password = self.login_view.ent_pw.get()

        if not self.user_name.strip() or not password.strip():
            messagebox.showwarning('Lỗi', 'Dữ liệu không hợp lệ')
            return

        # Use the user_service to verify login
        account = user_service.verify_user_login(self.user_name, password)

        if account:
            self.show_admin_dashboard_view('<Button-1>')
        else:
            messagebox.showwarning('Lỗi', 'Tài khoản hoặc mật khẩu không chính xác')

    @handle_exceptions(default_return_value=None)
    def show_admin_dashboard_view(self, event):
        self.clear_frame()
        self.admin_dashboard_view = AdminDashboardView(self.root)
        self.set_welcome(self.user_name)
        self.admin_dashboard_view.grid(row=0, column=0)
        self.admin_dashboard_view.configure(width=400, height=200)
        self.admin_dashboard_view.btn_students.bind('<Button-1>', self.show_student_view)
        self.admin_dashboard_view.btn_result.bind('<Button-1>', self.show_subject_view)
        self.admin_dashboard_view.btn_logout.bind('<Button-1>', self.dashboard_logout)

    @handle_exceptions(default_return_value=None)
    def set_welcome(self, user_name):
        # Get user details from the service
        account = user_service.get_user_by_username(user_name)
        if account and account.name:
            self.admin_dashboard_view.lbl_welcome.config(text=f'Welcome {account.name}')
        else:
            self.admin_dashboard_view.lbl_welcome.config(text=f'Welcome {user_name}')

    @handle_exceptions(default_return_value=None)
    def show_student_view(self, event):
        self.student_view = StudentView(self.root)
        self.student_view.grid(row=0, column=0, sticky='nsew')
        self.student_view.configure(width=400, height=200)

        self.student_view.tree.bind('<<TreeviewSelect>>', self.on_select_student_view)
        self.student_view.btn_showall.bind('<Button-1>', self.get_all_students)
        self.student_view.btn_select_image.bind('<Button-1>', self.on_select_image)
        self.student_view.student_btn_add.bind('<Button-1>', self.add_student)
        self.student_view.student_btn_update.bind('<Button-1>', self.update_student)
        self.student_view.student_btn_delete.bind('<Button-1>', self.delete_student)
        self.student_view.btn_export.bind('<Button-1>', self.export_file_student)
        self.student_view.student_btn_refresh.bind('<Button-1>', self.refresh_infor)
        self.student_view.student_btn_back.bind('<Button-1>', self.studentview_back_dashboard)
        self.student_view.btn_find.bind('<Button-1>', self.find_student)

        for col in ('stt', 'student_id', 'name', 'gender', 'birth', 'generation', 'major', 'class', 'gpa'):
            self.student_view.tree.heading(col,
                                           command=lambda c=col: self.sort_heading(self.student_view.tree, c, False))

        # Load combobox data from services
        departments = department_service.get_all_departments()
        self.student_view.combo_department['values'] = [d.name for d in departments]
        if departments:
            self.student_view.combo_department.current(0)

        classes = departmental_class_service.get_all_classes()
        self.student_view.combo_class['values'] = [c.name for c in classes]
        if classes:
            self.student_view.combo_class.current(0)

        majors = major_service.get_all_majors()
        self.student_view.combo_major['values'] = [m.name for m in majors]
        if majors:
            self.student_view.combo_major.current(0)

    def show_password(self, event):
        if self.login_view.show_pw.get():
            self.login_view.ent_pw.config(show='*')
        else:
            self.login_view.ent_pw.config(show='')

    @handle_exceptions(default_return_value=None)
    def find_student(self, event):
        find_criteria_ui = self.student_view.find.get()
        find_data = self.student_view.ent_find.get()

        criteria_map = {
            'Mã sinh viên': 's.sid',
            'Tên sinh viên': 'student_name',
            'Chuyên ngành': 'm.name',
            'Khóa': 's.generation',
            'Lớp': 'dc.name'
        }

        find_criteria_db = criteria_map.get(find_criteria_ui)

        if not find_criteria_db:
            messagebox.showwarning("Lỗi", "Tiêu chí tìm kiếm không hợp lệ.")
            return

        students = student_service.search_students_with_gpa(find_criteria_db, find_data)

        self.delete_all_items_tree(self.student_view)

        for i, student in enumerate(students):
            formatted_birth = self.format_birth(str(student.bod))
            gpa_display = f"{student.gpa:.2f}" if student.gpa is not None else "N/A"
            self.student_view.tree.insert('', tk.END, values=(
                i + 1,
                student.sid,
                student.student_name,
                student.gender,
                formatted_birth,
                student.generation,
                student.major_name,
                student.class_name,
                gpa_display
            ))

    @handle_exceptions(default_return_value=None)
    def show_subject_view(self, event):
        self.subject_view = SubjectView(self.root)
        self.subject_view.grid(row=0, column=0, sticky='nsew')
        self.subject_view.configure(width=400, height=200)

        self.subject_view.btn_find.bind('<Button-1>', self.get_subject_by_id_semester)
        self.subject_view.btn_add_subject.bind('<Button-1>', self.show_form_subject_add)
        self.subject_view.btn_update_subject.bind('<Button-1>', self.show_form_subject_update)
        self.subject_view.btn_delete_subject.bind('<Button-1>', self.delete_subject_student)
        self.subject_view.btn_export.bind('<Button-1>', self.export_file_subject)
        self.subject_view.btn_back.bind('<Button-1>', self.subjectview_back_dashboard)
        self.subject_view.tree.bind('<<TreeviewSelect>>', self.on_selected_subject_student_view)

        for col in ('stt', 'subject_id', 'subject_name', 'semester', 'subject_credit', 'score_regular', 'score_midterm',
                    'score_final', 'score_avarage', 'rating'):
            self.subject_view.tree.heading(col,
                                           command=lambda c=col: self.sort_heading(self.subject_view.tree, c, False))

    @handle_exceptions(default_return_value=None)
    def show_form_subject_add(self, event):
        self.form_subject_view = TopLeveSubjectlView(self.subject_view)
        self.form_subject_view.geometry('800x500')

        self.form_subject_view.combo_subject_id.bind('<<ComboboxSelected>>', self.set_value_by_subject_id)
        self.form_subject_view.ent_student_id.bind('<FocusOut>', self.set_value_by_student_id)
        self.form_subject_view.btn_add_confirm.bind('<Button-1>', self.add_subject_student)
        self.form_subject_view.btn_add_cancel.bind('<Button-1>', lambda event: self.form_subject_view.destroy())

        subjects = subject_service.get_all_subjects()
        self.form_subject_view.combo_subject_id['values'] = [s.id for s in subjects]
        if subjects:
            self.form_subject_view.combo_subject_id.current(0)

    @handle_exceptions(default_return_value=None)
    def show_form_subject_update(self, event):
        values = self.get_item_on_select_subject_view()
        if not values:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một môn học để cập nhật.")
            return

        self.form_subject_view = TopLeveSubjectlView(self.subject_view)
        self.form_subject_view.geometry('800x500')

        self.form_subject_view.btn_add_confirm.bind('<Button-1>', self.update_subject_student)
        self.form_subject_view.btn_add_cancel.bind('<Button-1>', lambda event: self.form_subject_view.destroy())

        self.form_subject_view.title1.config(text='Sửa học phần')
        values = values[1:]  # Skip STT

        self.form_subject_view.combo_semester.set(values[2])
        self.form_subject_view.combo_semester.config(state='disable')
        self.form_subject_view.combo_subject_id.set(values[0])
        self.form_subject_view.combo_subject_id.config(state='disable')

        self.form_subject_view.ent_subject_name.config(state='normal')
        self.form_subject_view.ent_subject_name.insert(0, values[1])
        self.form_subject_view.ent_subject_name.config(state='readonly')

        self.form_subject_view.ent_student_id.config(state='normal')
        self.form_subject_view.ent_student_id.insert(0, self.subject_view.ent_id.get())
        self.form_subject_view.ent_student_id.config(state='readonly')

        self.form_subject_view.ent_student_name.config(state='normal')
        self.form_subject_view.ent_student_name.insert(0, self.subject_view.ent_student_name.get())
        self.form_subject_view.ent_student_name.config(state='readonly')

        self.form_subject_view.ent_credit.config(state='normal')
        self.form_subject_view.ent_credit.insert(0, values[3])
        self.form_subject_view.ent_credit.config(state='readonly')

        self.form_subject_view.ent_score_regular.insert(0, values[4])
        self.form_subject_view.ent_score_midterm.insert(0, values[5])
        self.form_subject_view.ent_score_final.insert(0, values[6])

    def on_selected_subject_student_view(self, event):
        if self.subject_view.tree.selection():
            self.subject_view.btn_update_subject.config(state='normal')
            self.subject_view.btn_delete_subject.config(state='normal')
        else:
            self.subject_view.btn_update_subject.config(state='disable')
            self.subject_view.btn_delete_subject.config(state='disable')

    def get_item_on_select_subject_view(self):
        if self.subject_view.tree.selection():
            select_item = self.subject_view.tree.selection()[0]
            return self.subject_view.tree.item(select_item, 'values')
        return None

    @handle_exceptions(default_return_value=None)
    def set_value_by_subject_id(self, event):
        subject_id = self.form_subject_view.subject_id.get()
        subject = subject_service.get_subject_by_id(subject_id)

        if subject:
            self.form_subject_view.ent_subject_name.config(state='normal')
            self.form_subject_view.ent_subject_name.delete(0, tk.END)
            self.form_subject_view.ent_subject_name.insert(0, subject.name)
            self.form_subject_view.ent_subject_name.config(state='readonly')

            self.form_subject_view.ent_credit.config(state='normal')
            self.form_subject_view.ent_credit.delete(0, tk.END)
            self.form_subject_view.ent_credit.insert(0, subject.coff)
            self.form_subject_view.ent_credit.config(state='readonly')

    @handle_exceptions(default_return_value=None)
    def set_value_by_student_id(self, event):
        student_id = self.form_subject_view.ent_student_id.get()
        student = student_service.get_student_by_sid(student_id)

        self.form_subject_view.ent_student_name.config(state='normal')
        self.form_subject_view.ent_student_name.delete(0, tk.END)

        if student:
            self.form_subject_view.ent_student_name.insert(0, f"{student.fname} {student.lname}")
        else:
            messagebox.showwarning('Lỗi', 'Mã sinh viên không tồn tại')
            self.form_subject_view.ent_student_name.insert(0, "Không tìm thấy")

        self.form_subject_view.ent_student_name.config(state='readonly')

    @handle_exceptions(default_return_value=None)
    def on_select_student_view(self, event):
        if not self.student_view.tree.selection():
            self.student_view.student_btn_update.config(state='disable')
            self.student_view.student_btn_delete.config(state='disable')
            self.student_view.student_btn_add.config(state='normal')
            self.student_view.ent_id.config(state='normal')
            return

        self.student_view.ent_id.config(state='normal')
        selected_item = self.student_view.tree.selection()[0]
        values = self.student_view.tree.item(selected_item, 'values')
        student_id = values[1]

        student = student_service.get_student_details_by_sid(student_id)
        if not student:
            messagebox.showerror("Lỗi", f"Không tìm thấy chi tiết cho sinh viên {student_id}")
            return

        self.student_view.ent_id.delete(0, tk.END)
        self.student_view.ent_id.insert(0, student.sid)

        self.student_view.ent_name.delete(0, tk.END)
        self.student_view.ent_name.insert(0, student.student_name)

        self.student_view.ent_address.delete(0, tk.END)
        self.student_view.ent_address.insert(0, student.address)

        self.student_view.ent_cccd.delete(0, tk.END)
        self.student_view.ent_cccd.insert(0, student.cid)

        self.student_view.ent_phone.delete(0, tk.END)
        self.student_view.ent_phone.insert(0, student.phone)

        self.student_view.ent_email.delete(0, tk.END)
        self.student_view.ent_email.insert(0, student.email)

        self.student_view.date_birth.set_date(student.bod)
        self.student_view.combo_gender.set(student.gender)
        self.student_view.combo_department.set(student.department_name)
        self.student_view.combo_major.set(student.major_name)
        self.student_view.combo_class.set(student.class_name)
        self.student_view.combo_gen.set(student.generation)

        self.image_path = student.img
        try:
            image = Image.open(self.image_path)
            resized_image = image.resize((140, 220))
            self.photo = ImageTk.PhotoImage(resized_image)
            self.student_view.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
        except Exception as e:
            print(f"Error loading image {self.image_path}: {e}")
            self.student_view.canvas.delete("all")  # Clear canvas if image fails

        self.student_view.student_btn_update.config(state='normal')
        self.student_view.student_btn_delete.config(state='normal')
        self.student_view.student_btn_add.config(state='disable')
        self.student_view.ent_id.config(state='readonly')

    def on_select_image(self, event):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        if self.image_path:
            try:
                image = Image.open(self.image_path)
                resized_image = image.resize((140, 220))
                self.photo = ImageTk.PhotoImage(resized_image)
                self.student_view.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)
            except Exception as e:
                messagebox.showerror("Lỗi ảnh", f"Không thể mở file ảnh: {e}")
                self.image_path = None  # Reset path if loading fails

    def delete_all_items_tree(self, parent):
        for item in parent.tree.get_children():
            parent.tree.delete(item)

    @handle_exceptions(default_return_value=None)
    def get_all_students(self, event):
        self.delete_all_items_tree(self.student_view)
        students = student_service.get_all_student_details_with_gpa()

        for i, student in enumerate(students):
            formatted_birth = self.format_birth(str(student.bod))
            gpa_display = f"{student.gpa:.2f}" if student.gpa is not None else "N/A"
            self.student_view.tree.insert('', tk.END, values=(
                i + 1,
                student.sid,
                student.student_name,
                'Nam' if student.gender == 0 else 'Nữ' if student.gender == 1 else 'Khác',  # Assuming 0=Nam, 1=Nữ
                formatted_birth,
                student.generation,
                student.major_name,
                student.class_name,
                gpa_display
            ))

    def format_birth(self, old_birth):
        if not old_birth:
            return ""
        try:
            parts = str(old_birth).split('-')
            if len(parts) == 3:
                return f"{parts[2]}/{parts[1]}/{parts[0]}"
            return old_birth
        except Exception:
            return old_birth

    @handle_exceptions(default_return_value=None)
    def get_subject_by_id_semester(self, event):
        self.delete_all_items_tree(self.subject_view)

        student_id = self.subject_view.ent_id.get()
        semester_str = self.subject_view.semester.get()  # e.g., "HK1 (2023-2024)"

        if not student_id.strip():
            messagebox.showwarning("Lỗi", "Vui lòng nhập Mã sinh viên.")
            return

        # Assuming semester_str needs to be parsed to get semester_id
        # This logic depends on how you populate the semester combobox
        # For now, I'll assume it's just the ID.
        # This part needs to be adapted.
        # Let's assume the semester string is just the ID for now.
        try:
            # This is a placeholder. You need to get the semester ID.
            # Let's assume the user enters a student ID and *all* semesters are shown.
            # The old code `(student_id, semester)` implies semester is just a string 'HK1'.
            # I will use the new service function which queries by student_id only.
            pass
        except Exception:
            messagebox.showwarning("Lỗi", "Học kì không hợp lệ.")
            return

        student = student_service.get_student_by_sid(student_id)
        if not student:
            messagebox.showwarning('Lỗi', 'Mã sinh viên không tồn tại')
            self.subject_view.ent_student_name.configure(state='normal')
            self.subject_view.ent_student_name.delete(0, tk.END)
            self.subject_view.ent_student_name.configure(state='disable')
            return

        # Update student name
        self.subject_view.ent_student_name.configure(state='normal')
        self.subject_view.ent_student_name.delete(0, tk.END)
        self.subject_view.ent_student_name.insert(0, f"{student.fname} {student.lname}")
        self.subject_view.ent_student_name.configure(state='disable')

        # Get subjects using the new service function
        subjects = score_service.get_subject_details_for_student(student_id)

        for i, subject in enumerate(subjects):
            self.subject_view.tree.insert('', tk.END, values=(
                i + 1,
                subject.subject_id,
                subject.subject_name,
                subject.semester_name,  # Using the semester name
                subject.subject_credit,
                subject.score_regular,
                subject.score_midterm,
                subject.score_final,
                f"{subject.score_average:.2f}" if subject.score_average is not None else "N/A",
                subject.rating
            ))

    @handle_exceptions(default_return_value=None)
    def add_student(self, event):
        student_id = self.student_view.ent_id.get().strip()

        # Simple validation
        if not student_id:
            messagebox.showwarning('Lỗi', 'Mã sinh viên không được bỏ trống')
            return

        # Check for existence
        if student_service.get_student_by_sid(student_id):
            messagebox.showwarning('Lỗi', 'Mã sinh viên đã tồn tại')
            return

        student_cccd = self.student_view.ent_cccd.get().strip()
        if student_cccd and student_service.get_student_by_cid(student_cccd):
            messagebox.showwarning('Lỗi', 'CCCD/CMT đã tồn tại')
            return

        student_email = self.student_view.ent_email.get().strip()
        if student_email and student_service.get_student_by_email(student_email):
            messagebox.showwarning('Lỗi', 'Email đã tồn tại')
            return

        # Get IDs from names
        major = major_service.get_major_by_name(self.student_view.major.get())
        d_class = departmental_class_service.get_class_by_name(self.student_view.classs.get())

        if not major or not d_class:
            messagebox.showwarning('Lỗi', 'Chuyên ngành hoặc Lớp không hợp lệ')
            return

        # Create SimpleNamespace object for the service
        full_name = self.student_view.ent_name.get().strip().split(' ', 1)
        gender_str = self.student_view.gender.get().strip()

        new_student = sn(
            sid=student_id,
            fname=full_name[0],
            lname=full_name[1] if len(full_name) > 1 else '',
            bod=self.format_birth_to_db(self.student_view.date_birth.get()),
            address=self.student_view.ent_address.get().strip(),
            cid=student_cccd,
            phone=self.student_view.ent_phone.get().strip(),
            email=student_email,
            gender=0 if gender_str == 'Nam' else 1 if gender_str == 'Nữ' else 2,  # Assuming 0=Nam, 1=Nữ, 2=Khác
            generation=int(self.student_view.gen.get().strip()),
            img=self.image_path,
            departmental_class_id=d_class.id,
            major_id=major.id,
            graduated=0,  # Default
            active=1  # Default
        )

        ask_confirm = messagebox.askokcancel('Thêm sinh viên', 'Bạn có muốn thêm sinh viên ?')
        if ask_confirm:
            student_service.add_student(new_student)
            messagebox.showinfo('Thêm thành công', 'Thêm thành công')
            self.get_all_students('<Button-1>')

    @handle_exceptions(default_return_value=None)
    def update_student(self, event):
        student_id = self.student_view.ent_id.get().strip()
        if not student_id:
            messagebox.showwarning("Lỗi", "Không có sinh viên nào được chọn.")
            return

        major = major_service.get_major_by_name(self.student_view.major.get())
        d_class = departmental_class_service.get_class_by_name(self.student_view.classs.get())

        if not major or not d_class:
            messagebox.showwarning('Lỗi', 'Chuyên ngành hoặc Lớp không hợp lệ')
            return

        full_name = self.student_view.ent_name.get().strip().split(' ', 1)
        gender_str = self.student_view.gender.get().strip()

        updated_student = sn(
            sid=student_id,
            fname=full_name[0],
            lname=full_name[1] if len(full_name) > 1 else '',
            bod=self.format_birth_to_db(self.student_view.date_birth.get()),
            address=self.student_view.ent_address.get().strip(),
            cid=self.student_view.ent_cccd.get().strip(),
            phone=self.student_view.ent_phone.get().strip(),
            email=self.student_view.ent_email.get().strip(),
            gender=0 if gender_str == 'Nam' else 1 if gender_str == 'Nữ' else 2,
            generation=int(self.student_view.gen.get().strip()),
            img=self.image_path,
            departmental_class_id=d_class.id,
            major_id=major.id,
            # graduated and active are not on the form, so we don't update them
            # To update them, you'd need to fetch the student first
            # For this example, I'll assume they don't change.
            # A better implementation would fetch student, merge changes, then update.
            # Let's just fetch the original student to keep them.
            original_student=student_service.get_student_by_sid(student_id),
            graduated=original_student.graduated,
            active=original_student.active
        )

        ask_confirm = messagebox.askokcancel('Sửa sinh viên', 'Bạn có muốn sửa sinh viên ?')
        if ask_confirm:
            student_service.update_student(updated_student)
            messagebox.showinfo('Sửa thành công', 'Sửa thành công')
            self.get_all_students('<Button-1>')

    @handle_exceptions(default_return_value=None)
    def delete_student(self, event):
        student_id = self.student_view.ent_id.get()
        ask_confirm = messagebox.askokcancel('Xóa sinh viên', 'Bạn có muốn xóa sinh viên ?')
        if ask_confirm:
            student_service.delete_student(student_id)
            messagebox.showinfo('Xóa thành công', 'Xóa thành công')
            self.refresh_infor('<Button-1>')
            self.get_all_students('<Button-1>')

    @handle_exceptions(default_return_value=None)
    def add_subject_student(self, event):
        student_id = self.form_subject_view.ent_student_id.get()
        subject_id = self.form_subject_view.subject_id.get()

        # This is complex. The form needs to let user pick a SECTIONAL_CLASS, not just a subject.
        # The old code `(subject_id,student_id,semester)` is not the PK of `scores`.
        # The PK is `(sectional_class_id, student_id)`.
        # This part of the UI logic is flawed given the new DB schema.

        # I will assume the user needs to select a sectional class.
        # For now, I will show a warning.
        messagebox.showwarning("Logic Error",
                               "This UI is not mapped to the database correctly. Cannot add subject score.")

        # TODO: Refactor UI to select a SectionalClass ID, not SubjectID+Semester

        # --- Old logic (commented out) ---
        # student_name = self.form_subject_view.ent_student_name.get()
        # score_regular = float(self.form_subject_view.ent_score_regular.get())
        # ...
        # if student_name != 'Không tìm thấy':
        #    ...
        #    new_score = sn(sectional_class_id=???, student_id=student_id, ...)
        #    score_service.add_or_update_score(new_score)

    @handle_exceptions(default_return_value=None)
    def update_subject_student(self, event):
        student_id = self.form_subject_view.ent_student_id.get()
        subject_id = self.form_subject_view.subject_id.get()

        # This has the same logic flaw as add_subject_student
        messagebox.showwarning("Logic Error", "This UI is not mapped to the database correctly. Cannot update score.")

    @handle_exceptions(default_return_value=None)
    def delete_subject_student(self, event):
        student_id = self.subject_view.ent_id.get()
        values_item = self.get_item_on_select_subject_view()

        # This has the same logic flaw. We need the sectional_class_id to delete.
        # values_item[1] is subject_id, not sectional_class_id.
        messagebox.showwarning("Logic Error", "This UI is not mapped to the database correctly. Cannot delete score.")
        # old_call: self.student_model.delete_subject_student((values_item[1],student_id,values_item[3]))
        # new_call: score_service.delete_score(sectional_class_id=???, student_id=student_id)

    @handle_exceptions(default_return_value=None)
    def export_file_student(self, event):
        data = []
        for item in self.student_view.tree.get_children():
            data.append(self.student_view.tree.item(item, 'values'))

        columns_name = ['STT', 'Mã sinh viên', 'Họ và tên', 'Giới tính', 'Ngày sinh', 'Khóa', 'Chuyên ngành', 'Lớp',
                        'GPA']

        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                 filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf"),
                                                            ("All files", "*.*")])

        if not file_path:
            return

        _, file_extension = os.path.splitext(file_path)

        if file_extension == '.xlsx':
            df = pd.DataFrame(data=data, columns=columns_name)
            df.to_excel(file_path, index=False)
            messagebox.showinfo('Thành công', 'Xuất EXCEL thành công')

        elif file_extension == '.pdf':
            self.create_pdf(file_path, "Danh Sách Sinh Viên", columns_name, data, cell_width=22)
            messagebox.showinfo('Thành công', 'Xuất PDF thành công')
        else:
            messagebox.showwarning('Lỗi', 'Định dạng không phù hợp')

    @handle_exceptions(default_return_value=None)
    def export_file_subject(self, event):
        data = []
        for item in self.subject_view.tree.get_children():
            data.append(self.subject_view.tree.item(item, 'values'))

        columns_name = ['STT', 'Mã học phần', 'Tên học phần', 'Học kì', 'Số tín chỉ', 'Điểm thường xuyên',
                        'Điểm giữa kì', 'Điểm cuối kì', 'Điểm trung bình', 'Xếp loại']

        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                                 filetypes=[("Excel files", "*.xlsx"), ("PDF files", "*.pdf"),
                                                            ("All files", "*.*")])

        if not file_path:
            return

        _, file_extension = os.path.splitext(file_path)

        if file_extension == '.xlsx':
            df = pd.DataFrame(data=data, columns=columns_name)
            df.to_excel(file_path, index=False)
            messagebox.showinfo('Thành công', 'Xuất EXCEL thành công')

        elif file_extension == '.pdf':
            self.create_pdf(file_path, "Danh Sách Học Phần", columns_name, data, cell_width=21, font_size=5)
            messagebox.showinfo('Thành công', 'Xuất PDF thành công')
        else:
            messagebox.showwarning('Lỗi', 'Định dạng không phù hợp')

    def create_pdf(self, file_path, title, columns, data, cell_width=22, font_size=6):
        pdf = FPDF()
        pdf.add_page()
        # You MUST provide a path to a .ttf font file that supports Unicode
        # I'll assume 'DejaVuSans.ttf' is in the same directory.
        try:
            pdf.add_font("DejaVu", "", "DejaVuSans.ttf", uni=True)
            pdf.set_font("DejaVu", size=10)
        except RuntimeError:
            messagebox.showerror("Lỗi Font",
                                 "Không tìm thấy font 'DejaVuSans.ttf'. PDF sẽ không thể hiển thị tiếng Việt.")
            pdf.set_font("Arial", size=10)

        pdf.cell(0, 10, txt=title, ln=True, align="C")
        pdf.ln(10)

        pdf.set_font(pdf.font_family, size=font_size)
        for heading in columns:
            pdf.cell(cell_width, 10, txt=str(heading), border=1, align='C')
        pdf.ln(10)

        for row in data:
            for cell_data in row:
                pdf.cell(cell_width, 10, str(cell_data), border=1, align='C')
            pdf.ln(10)

        pdf.output(file_path)

    def refresh_infor(self, event):
        self.student_view.ent_id.config(state='normal')
        self.student_view.ent_id.delete(0, tk.END)
        self.student_view.ent_name.delete(0, tk.END)
        self.student_view.ent_address.delete(0, tk.END)
        self.student_view.ent_cccd.delete(0, tk.END)
        self.student_view.ent_phone.delete(0, tk.END)
        self.student_view.ent_email.delete(0, tk.END)
        self.student_view.canvas.delete("all")
        self.student_view.student_btn_update.config(state='disable')
        self.student_view.student_btn_delete.config(state='disable')
        self.student_view.student_btn_add.config(state='normal')

    def studentview_back_dashboard(self, event):
        self.show_admin_dashboard_view('<Button-1>')

    def subjectview_back_dashboard(self, event):
        self.show_admin_dashboard_view('<Button-1>')

    def dashboard_logout(self, event):
        self.user_name = None
        self.show_login_view('<Button-1>')

    def sort_heading(self, tree, col, reverse):
        data = [(tree.set(item, col), item) for item in tree.get_children()]
        if data:
            data.sort(reverse=reverse)
            for index, (_, item) in enumerate(data):
                tree.move(item, '', index)
            tree.heading(col, command=lambda: self.sort_heading(tree, col, not reverse))

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def format_birth_to_db(self, old_birth):
        # Converts D/M/Y from tkcalendar to Y-M-D for DB
        if not old_birth:
            return None
        try:
            parts = str(old_birth).split('/')
            if len(parts) == 3:
                return f"{parts[2]}-{parts[1]}-{parts[0]}"
            return old_birth
        except Exception:
            return old_birth


# --- Main application setup (Example) ---
if __name__ == "__main__":
    try:
        # This is just an example of how to run the app
        # You would import your actual views and run this

        # Mocking Views for example to be runnable
        class BaseView(tk.Frame):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                self.configure(bg='white')


        class LoginView(BaseView):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                tk.Label(self, text="Login View", font=("Arial", 24)).pack(pady=50)
                self.ent_us = tk.Entry(self)
                self.ent_us.pack(pady=5)
                self.ent_pw = tk.Entry(self, show="*")
                self.ent_pw.pack(pady=5)
                self.show_pw = tk.BooleanVar()
                self.checkbtn_showpw = tk.Checkbutton(self, text="Show", variable=self.show_pw)
                self.checkbtn_showpw.pack()
                self.btn_login = tk.Button(self, text="Login")
                self.btn_login.pack(pady=20)

                # Mock data for testing
                self.ent_us.insert(0, "admin")
                self.ent_pw.insert(0, "password")


        class AdminDashboardView(BaseView):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                self.lbl_welcome = tk.Label(self, text="Welcome!", font=("Arial", 24))
                self.lbl_welcome.pack(pady=50)
                self.btn_students = tk.Button(self, text="Manage Students")
                self.btn_students.pack(pady=10)
                self.btn_result = tk.Button(self, text="Manage Results")
                self.btn_result.pack(pady=10)
                self.btn_logout = tk.Button(self, text="Logout")
                self.btn_logout.pack(pady=10)


        # Other views would be mocked similarly...
        class StudentView(BaseView):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                tk.Label(self, text="Student View", font=("Arial", 24)).pack()
                self.tree = ttk.Treeview(self,
                                         columns=("stt", "student_id", "name", "gender", "birth", "generation", "major",
                                                  "class", "gpa"), show="headings")
                for col in self.tree['columns']: self.tree.heading(col, text=col)
                self.tree.pack(fill="both", expand=True)

                # Mock UI elements referenced in controller
                self.ent_id = tk.Entry(self)
                self.ent_name = tk.Entry(self)
                self.ent_address = tk.Entry(self)
                self.ent_cccd = tk.Entry(self)
                self.ent_phone = tk.Entry(self)
                self.ent_email = tk.Entry(self)
                from tkcalendar import DateEntry  # Requires tkcalendar
                self.date_birth = DateEntry(self)
                self.gender = tk.StringVar(value="Nam")
                self.combo_gender = ttk.Combobox(self, textvariable=self.gender, values=["Nam", "Nữ", "Khác"])
                self.department = tk.StringVar()
                self.combo_department = ttk.Combobox(self, textvariable=self.department)
                self.major = tk.StringVar()
                self.combo_major = ttk.Combobox(self, textvariable=self.major)
                self.classs = tk.StringVar()
                self.combo_class = ttk.Combobox(self, textvariable=self.classs)
                self.gen = tk.StringVar()
                self.combo_gen = ttk.Combobox(self, textvariable=self.gen, values=[str(y) for y in range(2018, 2025)])
                self.canvas = tk.Canvas(self, width=140, height=220, bg='grey')

                self.btn_showall = tk.Button(self, text="Show All")
                self.btn_select_image = tk.Button(self, text="Select Image")
                self.student_btn_add = tk.Button(self, text="Add")
                self.student_btn_update = tk.Button(self, text="Update", state="disable")
                self.student_btn_delete = tk.Button(self, text="Delete", state="disable")
                self.btn_export = tk.Button(self, text="Export")
                self.student_btn_refresh = tk.Button(self, text="Refresh")
                self.student_btn_back = tk.Button(self, text="Back")
                self.find = tk.StringVar(value="Mã sinh viên")
                self.combo_find = ttk.Combobox(self, textvariable=self.find,
                                               values=["Mã sinh viên", "Tên sinh viên", "Chuyên ngành", "Khóa", "Lớp"])
                self.ent_find = tk.Entry(self)
                self.btn_find = tk.Button(self, text="Find")

                # Simple layout
                self.student_btn_back.pack(side="bottom")
                self.btn_showall.pack(side="bottom")


        class SubjectView(BaseView):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                tk.Label(self, text="Subject View", font=("Arial", 24)).pack()
                self.tree = ttk.Treeview(self,
                                         columns=("stt", "subject_id", "subject_name", "semester", "subject_credit",
                                                  "score_regular", "score_midterm", "score_final", "score_avarage",
                                                  "rating"), show="headings")
                for col in self.tree['columns']: self.tree.heading(col, text=col)
                self.tree.pack(fill="both", expand=True)

                # Mock UI elements
                self.ent_id = tk.Entry(self);
                self.ent_id.pack()
                self.semester = tk.StringVar(value="HK1");
                self.combo_semester = ttk.Combobox(self, textvariable=self.semester, values=["HK1", "HK2"]);
                self.combo_semester.pack()
                self.btn_find = tk.Button(self, text="Find Student Subjects");
                self.btn_find.pack()
                self.ent_student_name = tk.Entry(self, state="disable");
                self.ent_student_name.pack()
                self.btn_add_subject = tk.Button(self, text="Add Subject");
                self.btn_add_subject.pack()
                self.btn_update_subject = tk.Button(self, text="Update Subject", state="disable");
                self.btn_update_subject.pack()
                self.btn_delete_subject = tk.Button(self, text="Delete Subject", state="disable");
                self.btn_delete_subject.pack()
                self.btn_export = tk.Button(self, text="Export");
                self.btn_export.pack()
                self.btn_back = tk.Button(self, text="Back");
                self.btn_back.pack()


        class TopLeveSubjectlView(tk.Toplevel):
            def __init__(self, master, *args, **kwargs):
                super().__init__(master, *args, **kwargs)
                tk.Label(self, text="Add/Edit Subject", font=("Arial", 20)).pack()

                # Mock elements
                self.title1 = tk.Label(self, text="Thêm học phần")
                self.title1.pack()
                self.semester = tk.StringVar()
                self.combo_semester = ttk.Combobox(self, textvariable=self.semester)
                self.combo_semester.pack()
                self.subject_id = tk.StringVar()
                self.combo_subject_id = ttk.Combobox(self, textvariable=self.subject_id)
                self.combo_subject_id.pack()
                self.ent_subject_name = tk.Entry(self, state="readonly")
                self.ent_subject_name.pack()
                self.ent_student_id = tk.Entry(self)
                self.ent_student_id.pack()
                self.ent_student_name = tk.Entry(self, state="readonly")
                self.ent_student_name.pack()
                self.ent_credit = tk.Entry(self, state="readonly")
                self.ent_credit.pack()
                self.ent_score_regular = tk.Entry(self)
                self.ent_score_regular.pack()
                self.ent_score_midterm = tk.Entry(self)
                self.ent_score_midterm.pack()
                self.ent_score_final = tk.Entry(self)
                self.ent_score_final.pack()
                self.btn_add_confirm = tk.Button(self, text="Confirm")
                self.btn_add_confirm.pack()
                self.btn_add_cancel = tk.Button(self, text="Cancel")
                self.btn_add_cancel.pack()


        root = tk.Tk()
        # You must have the DejaVuSans.ttf font file in the same directory as this script
        # or you will get an error on PDF export.
        # You can download it from: https://www.fontsquirrel.com/fonts/dejavu-sans
        app = AppController(root)
        root.mainloop()
    except ImportError as e:
        print(f"Error: Missing package '{e.name}'.")
        print("Please install required packages: pip install tkcalendar pandas fpdf")
