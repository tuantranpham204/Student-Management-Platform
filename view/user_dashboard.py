import tkinter as tk
from util.util import default_vals

class UserDashboard(tk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.config(bg=default_vals.DEFAULT_BG_COLOR)
        self.widgets()


    def widgets(self):
        self.lb_welcome = tk.Label(self, font=16, text=f"Welcome {self.username} :3", bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_welcome.grid(row=0, column=0, sticky='we', padx=5, pady=5, columnspan=2)

        self.btn_management = tk.Button(self, text='🎓\n\nStudent\nManagement', bg='#E7CBCB', relief='solid', width=18, height=9, font=16, command=self.to_students_management)
        self.btn_management.grid(row=1, column=0, padx=120, pady=80)

        self.btn_statistics = tk.Button(self, text='📝\n\nStudent\nStatistics', bg='#92DFC8', relief='solid', width=18, height=9, font=16)
        self.btn_statistics.grid(row=1, column=1, padx=120, pady=80)

        self.btn_uni = tk.Button(self, text='📝\n\nUniversity\nManagement', bg='#92DFC8', relief='solid', width=18, height=9, font=16)
        self.btn_uni.grid(row=2, column=1, padx=120, pady=80)

        self.btn_logout = tk.Button(self, text='🔓\n\nLog\nout', bg='#C8EBF3', relief='solid', width=18, height=9, font=16, command=self.log_out)
        self.btn_logout.grid(row=2, column=0, padx=120, pady=80)

        # Đảm bảo các hàng/cột trong main_frame có thể co giãn
        self.grid_rowconfigure(0, weight=10)
        for i in range(1, 3):  # 2 hàng
            self.grid_rowconfigure(i, weight=45)
        for i in range(2):  # 2 cột
            self.grid_columnconfigure(i, weight=50)\

    def log_out(self):
        from view.login import LoginView
        self.grid_forget()
        self.login_view = LoginView(self.parent)
        self.login_view.grid(row=0, column=0)

    def to_students_management(self):
        from view.student_management import StudentManagement
        self.student_management = StudentManagement(self.parent)
        self.student_management.grid(row=0, column=0)
