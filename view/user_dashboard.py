import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from util.util import default_vals
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from service.student import get_all_students


class UserDashboard(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.config(bg=default_vals.DEFAULT_BG_COLOR)
        self.widgets()

    def widgets(self):
        """Trang chính của Dashboard"""
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

        # Cho layout co giãn
        self.grid_rowconfigure(0, weight=10)
        for i in range(1, 3):
            self.grid_rowconfigure(i, weight=45)
        for i in range(2):
            self.grid_columnconfigure(i, weight=50)

    def clear_frame(self):
        """Chỉ xóa widget con, không xóa chính frame"""
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
        """Hiển thị trang thống kê sinh viên (3 biểu đồ cùng trang)"""
        self.clear_frame()
        self.parent.geometry("2000x1000")

        # ===== Nút quay lại (góc trái trên, dùng place không gây xung đột) =====
        back_btn = tk.Button(
            self,
            text="← Quay lại",
            font=("Arial", 12, "bold"),
            bg="#FFB6B6",
            fg="black",
            relief="raised",
            command=self.go_back_to_dashboard
        )
        back_btn.place(x=10, y=10)

        # ===== Tiêu đề =====
        title = ttk.Label(self, text="📊 Thống kê sinh viên", font=("Arial", 18, "bold"))
        title.grid(row=0, column=0, columnspan=3, pady=50)

        # Frame chứa biểu đồ
        self.chart_frame = tk.Frame(self)
        self.chart_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Lấy dữ liệu sinh viên
        students = get_all_students()

        # ===== 1. Giới tính =====
        gender_counts = {"Nam": 0, "Nữ": 0}
        for s in students:
            gender_counts["Nam" if s.gender == 1 else "Nữ"] += 1

        fig1, ax1 = plt.subplots(figsize=(4, 3))
        ax1.pie(gender_counts.values(), labels=gender_counts.keys(), autopct="%1.1f%%")
        ax1.set_title("Giới tính")
        canvas1 = FigureCanvasTkAgg(fig1, master=self.chart_frame)
        canvas1.draw()
        canvas1.get_tk_widget().grid(row=0, column=0, padx=20, pady=20)

        # ===== 2. Trạng thái =====
        status_counts = {}
        for s in students:
            st = str(s.status)
            status_counts[st] = status_counts.get(st, 0) + 1

        fig2, ax2 = plt.subplots(figsize=(4, 3))
        ax2.bar(status_counts.keys(), status_counts.values(), color="orange")
        ax2.set_title("Trạng thái sinh viên")
        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=0, column=1, padx=20, pady=20)

        # ===== 3. Lớp học =====
        class_counts = {}
        for s in students:
            cls = str(s.departmental_class_id)
            class_counts[cls] = class_counts.get(cls, 0) + 1

        fig3, ax3 = plt.subplots(figsize=(4, 3))
        ax3.bar(class_counts.keys(), class_counts.values(), color="green")
        ax3.set_title("Lớp học")
        canvas3 = FigureCanvasTkAgg(fig3, master=self.chart_frame)
        canvas3.draw()
        canvas3.get_tk_widget().grid(row=0, column=2, padx=20, pady=20)

        # Giãn layout
        self.chart_frame.grid_columnconfigure(0, weight=1)
        self.chart_frame.grid_columnconfigure(1, weight=1)
        self.chart_frame.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)
    def go_back_to_dashboard(self):
        self.clear_frame()
        self.widgets()




