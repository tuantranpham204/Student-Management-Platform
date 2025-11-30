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
        # Re-draw the dashboard widgets
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
            self, text='📊\n\nUniversity\nStatistics',
            bg='#92DFC8', relief='solid', width=18, height=9, font=16,
            command=self.show_statistics
        )
        self.btn_statistics.grid(row=1, column=1, padx=120, pady=80)

        self.btn_uni = tk.Button(
            self, text='🏫\n\nUniversity\nManagement',
            bg='#92DFC8', relief='solid', width=18, height=9, font=16,
            command=self.to_university_management
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
        self.student_management = StudentManagement(self.parent, back_callback=self.restore_from_students)
        self.student_management.grid(row=0, column=0, sticky='nsew')

    def show_statistics(self):
        self.clear_frame()
        from view.student_statistics import StudentStatistics

        self.stats_view = StudentStatistics(self.parent, self.restore_dashboard)
        self.stats_view.grid(row=0, column=0, sticky='nsew')

    def restore_dashboard(self):
        if hasattr(self, 'stats_view'):
            self.stats_view.destroy()
        self.parent.geometry("2000x1000")
        self.clear_frame()  # Ensure clean slate
        self.widgets()

    def to_university_management(self):
        self.clear_frame()
        self.parent.geometry("2000x1000")
        from view.university_management import UniversityManagement
        self.student_management = UniversityManagement(self.parent, back_callback=self.restore_from_university_management)
        self.student_management.grid(row=0, column=0, sticky='nsew')

    def restore_from_students(self):
        if hasattr(self, 'student_management'):
            self.student_management.destroy()
        self.parent.geometry("2000x1000")
        self.clear_frame()
        self.widgets()

    def restore_from_university_management(self):
        if hasattr(self, 'university_management'):
            self.university_management.destroy()
        self.parent.geometry("2000x1000")
        self.clear_frame()
        self.widgets()