import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from service.student import get_all_students
from util.util import default_vals


class UserDashboard(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.config(bg=default_vals.DEFAULT_BG_COLOR)

        self.students = get_all_students()    # Load dữ liệu 1 lần
        self.filtered_students = self.students
        self.selected_class = None

        self.widgets()

    def widgets(self):
        self.lb_welcome = tk.Label(
            self,
            font=16,
            text=f"Welcome {self.username} :3",
            bg=default_vals.DEFAULT_BG_COLOR
        )
        self.lb_welcome.grid(row=0, column=0, sticky='we', padx=5, pady=5, columnspan=2)

        self.btn_management = tk.Button(
            self, text='🎓\n\nStudent\nManagement',
            bg='#E7CBCB', relief='solid', width=18, height=9, font=16,
            command=self.to_students_management
        )
        self.btn_management.grid(row=1, column=0, padx=120, pady=80)

        self.btn_statistics = tk.Button(
            self, text='📝\n\nStudent\nStatistics',
            bg='#92DFC8', relief='solid', width=18, height=9, font=16,
            command=self.table
        )
        self.btn_statistics.grid(row=1, column=1, padx=120, pady=80)

        self.btn_uni = tk.Button(
            self, text='🏫\n\nUniversity\nManagement',
            bg='#92DFC8', relief='solid', width=18, height=9, font=16
        )
        self.btn_uni.grid(row=2, column=1, padx=120, pady=80)

        self.btn_logout = tk.Button(
            self, text='🔓\n\nLog\nout',
            bg='#C8EBF3', relief='solid', width=18, height=9, font=16,
            command=self.log_out
        )
        self.btn_logout.grid(row=2, column=0, padx=120, pady=80)

        self.grid_rowconfigure(0, weight=10)
        for i in range(1, 3):
            self.grid_rowconfigure(i, weight=45)
        for i in range(2):
            self.grid_columnconfigure(i, weight=50)

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def log_out(self):
        self.grid_forget()
        self.parent.title('Student Management')
        self.parent.geometry("2000x1000")
        self.parent.resizable(True, True)
        self.parent.configure(bg=default_vals.DEFAULT_BG_COLOR)

    def to_students_management(self):
        self.clear_frame()
        self.parent.geometry("2000x1000")
        from view.student_management import StudentManagement
        self.student_management = StudentManagement(self.parent)
        self.student_management.grid(row=0, column=0, padx=10, pady=10)

    def table(self):
        self.clear_frame()
        self.parent.geometry("2000x1000")

        back_btn = tk.Button(
    self,
    text="← Quay lại",
    font=("Arial", 12, "bold"),
    bg="#FFB6B6",
    fg="black",
    relief="raised",
    command=self.go_back_to_dashboard
)
        back_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Combobox chọn lớp trên cùng hàng
        class_label = ttk.Label(self, text="Chọn lớp:", font=("Arial", 12))
        class_label.grid(row=0, column=1, sticky='e', padx=5)

        self.class_combobox = ttk.Combobox(self, state="readonly")
        self.class_combobox.grid(row=0, column=2, sticky='w', padx=5)

        classes = sorted(set(
            s.departmental_class_id for s in self.students
            if getattr(s, "departmental_class_id", None)
        ))
        self.class_combobox['values'] = ["Tất cả"] + classes
        self.class_combobox.current(0)
        self.class_combobox.bind("<<ComboboxSelected>>", self.on_class_selected)


        # Frame chứa biểu đồ
        self.chart_frame = tk.Frame(self)
        self.chart_frame.grid(row=2, column=0, columnspan=5, sticky="nsew")

        self.draw_charts(self.students)

        # Giãn layout
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
        self.grid_rowconfigure(2, weight=1)

    def on_class_selected(self, event):
        selected = self.class_combobox.get()
        self.selected_class = selected

        if selected == "Tất cả":
            self.filtered_students = self.students
        else:
            self.filtered_students = [
                s for s in self.students
                if getattr(s, "departmental_class_id", None) == selected
            ]

        self.draw_charts(self.filtered_students)

    def draw_charts(self, students):
        # Clear old charts
        for widget in self.chart_frame.winfo_children():
            widget.destroy()

        def count_field(field):
            counts = {}
            for s in students:
                val = getattr(s, field, None)
                if val is None:
                    val = "Unknown"
                counts[val] = counts.get(val, 0) + 1
            return counts

        # ============= 1. Gender =============
        gender_counts = count_field("gender")
        gender_labels = {"1": "Nam", "0": "Nữ", 1: "Nam", 0: "Nữ"}
        gender_counts_named = {gender_labels.get(k, str(k)): v for k, v in gender_counts.items()}

        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.pie(gender_counts_named.values(), labels=gender_counts_named.keys(), autopct="%1.1f%%")
        ax1.set_title("Giới tính")
        canvas1 = FigureCanvasTkAgg(fig1, master=self.chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

        # ============= 2. Status =============
        status_counts = count_field("status")
        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.bar(status_counts.keys(), status_counts.values(), color="orange")
        ax2.set_title("Trạng thái sinh viên")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

        # ============= 3. Generation =============
        generation_counts = count_field("generation")
        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.bar(generation_counts.keys(), generation_counts.values(), color="green")
        ax3.set_title("Khóa học")
        canvas3 = FigureCanvasTkAgg(fig3, master=self.chart_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=0, column=2, padx=20, pady=20)

        # ============= 4. Class (chỉ khi "Tất cả") ============
        if self.selected_class in (None, "Tất cả"):
            class_counts = count_field("departmental_class_id")
            fig4, ax4 = plt.subplots(figsize=(4, 3))
            ax4.bar(class_counts.keys(), class_counts.values(), color="blue")
            ax4.set_title("Lớp học")
            canvas4 = FigureCanvasTkAgg(fig4, master=self.chart_frame)
            canvas4.draw()
            canvas4.get_tk_widget().grid(row=0, column=3, padx=20, pady=20)

        # ============= 5. AGE =============
        def calculate_age(dob):
            if dob is None:
                return None
            if hasattr(dob, "year"):
                today = datetime.today()
                return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            possible_formats = ["%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d %H:%M:%S"]
            for fmt in possible_formats:
                try:
                    parsed = datetime.strptime(dob, fmt)
                    today = datetime.today()
                    return today.year - parsed.year - ((today.month, today.day) < (parsed.month, parsed.day))
                except:
                    continue
            return None

        ages = [calculate_age(s.dob) for s in students if getattr(s, "dob", None)]
        ages = [age for age in ages if age is not None]

        age_counts = {}
        for age in ages:
            age_counts[age] = age_counts.get(age, 0) + 1

        labels = [str(age) for age in sorted(age_counts.keys())]
        values = [age_counts[age] for age in sorted(age_counts.keys())]

        fig5, ax5 = plt.subplots(figsize=(5, 4))
        ax5.bar(labels, values, edgecolor='black')
        ax5.set_title("Số lượng sinh viên theo tuổi")
        ax5.set_xlabel("Tuổi")
        ax5.set_ylabel("Số lượng")
        ax5.grid(axis='y', alpha=0.3)

        canvas5 = FigureCanvasTkAgg(fig5, master=self.chart_frame)
        canvas5.draw()
        canvas5.get_tk_widget().grid(row=1, column=0, padx=20, pady=20)

        # Layout columns
        col_count = 4 if self.selected_class in (None, "Tất cả") else 3
        for i in range(col_count):
            self.chart_frame.grid_columnconfigure(i, weight=1)
        self.chart_frame.grid_rowconfigure(0, weight=1)
        self.chart_frame.grid_rowconfigure(1, weight=1)

    def go_back_to_dashboard(self):
        self.clear_frame()
        self.widgets()
