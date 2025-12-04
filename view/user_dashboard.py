import sys
import os
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from service.student import get_all_students
from util.util import default_vals
from service.subject import get_all_subjects
from service.department import get_all_departments
from service.major import get_all_majors
from service.departmental_class import get_all_classes as get_all_departmental_classes
from service.sectional_class import get_all_classes as get_all_sectional_classes
from service.grade_statistics import get_coefficient_name
from service.grade_statistics import calculate_subject_average, convert_to_gpa_4
class UserDashboard(tk.Frame):
    def __init__(self, parent, username):
        self.subjects = get_all_subjects()
        self.departments = get_all_departments()
        self.majors = get_all_majors()
        self.departmental_classes = get_all_departmental_classes()
        self.sectional_classes = get_all_sectional_classes()
        super().__init__(parent)
        
        # Load dữ liệu thống kê
        self.subjects = get_all_subjects()
        self.departments = get_all_departments()
        self.majors = get_all_majors()
        self.departmental_classes = get_all_departmental_classes()
        self.sectional_classes = get_all_sectional_classes()
        
        self.parent = parent
        self.username = username
        self.config(bg=default_vals.DEFAULT_BG_COLOR)
        self.students = get_all_students()
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
        # Ẩn dashboard
        self.grid_forget()
        
        # Hiển thị lại màn hình login
        from view.login import LoginView
        login_view = LoginView(self.parent)
        login_view.grid(row=0, column=0)
        
        # Reset lại cấu hình cửa sổ
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
        if hasattr(self, 'student_management'):
            self.student_management.destroy()
        # Khôi phục kích thước bình thường
        self.parent.state('normal')
        self.parent.geometry("2000x1000")
        self.clear_frame()
        self.widgets()
    
    def show_statistics(self):
        """Hiển thị trang thống kê mới"""
        self.clear_frame()
        self.parent.geometry("1600x900")
        
        # Header với nút quay lại
        header_frame = tk.Frame(self, bg='#2C3E50', height=80)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=5)
        header_frame.grid_propagate(False)

        # Nút quay lại
        back_btn = tk.Button(
            header_frame,
            text="← Quay lại Dashboard",
            font=("Arial", 14, "bold"),
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.go_back_to_dashboard
        )
        back_btn.pack(side='left', padx=20, pady=15)
        
        # Tiêu đề
        title_label = tk.Label(
            header_frame,
            text="📊 THỐNG KÊ TỔNG QUAN HỆ THỐNG",
            font=("Arial", 20, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(side='left', padx=50, pady=15)
        
        # Frame chứa các card thống kê
        stats_container = tk.Frame(self, bg=default_vals.DEFAULT_BG_COLOR)
        stats_container.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=40, pady=40)
        
        # Tính toán các số liệu
        total_subjects = len(self.subjects)
        total_departments = len(self.departments)
        total_majors = len(self.majors)
        total_departmental_classes = len(self.departmental_classes)
        total_sectional_classes = len(self.sectional_classes)
        
        # Dữ liệu cho các card
        stats_data = [
            ("📚", "Tổng số môn học", total_subjects, "#FF6B6B", "#FF8E8E"),
            ("🏢", "Tổng số khoa", total_departments, "#4ECDC4", "#6FD9CF"),
            ("🎓", "Tổng số ngành", total_majors, "#45B7D1", "#67C5DD"),
            ("👥", "Tổng số lớp", total_departmental_classes, "#FFA07A", "#FFB399"),
            ("📖", "Tổng số lớp học phần", total_sectional_classes, "#98D8C8", "#ADE0D3"),
            ("📊", "Thống kê điểm", "Theo lớp", "#9B59B6", "#AF7AC5")  # CARD MỚI
        ]
        
        # Helper function để tạo click handler
        def make_click_handler(index):
            handlers = [
                self.show_all_subjects_detail,
                self.show_all_departments_detail,
                self.show_all_majors_detail,
                self.show_all_departmental_classes_detail,
                self.show_all_sectional_classes_detail,
                self.show_class_grade_statistics_detail  # HANDLER MỚI
            ]
            return lambda e: handlers[index]()
        
        # Tạo các card với thiết kế đẹp hơn và tính năng click
        for idx, (icon, label, value, bg_color, hover_color) in enumerate(stats_data):
            card_frame = tk.Frame(stats_container, bg=default_vals.DEFAULT_BG_COLOR)
            card_frame.grid(row=0, column=idx, padx=15, pady=20, sticky='nsew')
            
            shadow_frame = tk.Frame(card_frame, bg='#CCCCCC', relief='flat')
            shadow_frame.pack(padx=3, pady=3, fill='both', expand=True)
            
            card = tk.Frame(shadow_frame, bg=bg_color, relief='raised', bd=0, cursor='hand2')
            card.pack(fill='both', expand=True)
            card.bind('<Button-1>', make_click_handler(idx))
            
            icon_label = tk.Label(card, text=icon, font=("Segoe UI Emoji", 48), bg=bg_color, fg='white', cursor='hand2')
            icon_label.pack(pady=(25, 10))
            icon_label.bind('<Button-1>', make_click_handler(idx))
            
            text_label = tk.Label(card, text=label, font=("Arial", 13, "bold"), bg=bg_color, fg='white', wraplength=200, cursor='hand2')
            text_label.pack(pady=(0, 5))
            text_label.bind('<Button-1>', make_click_handler(idx))
            
            value_frame = tk.Frame(card, bg='white', relief='flat', bd=0, cursor='hand2')
            value_frame.pack(pady=(10, 25), padx=20)
            value_frame.bind('<Button-1>', make_click_handler(idx))
            
            value_label = tk.Label(value_frame, text=str(value), font=("Arial", 36, "bold"), bg='white', fg=bg_color, padx=20, pady=5, cursor='hand2')
            value_label.pack()
            value_label.bind('<Button-1>', make_click_handler(idx))
            
            stats_container.grid_columnconfigure(idx, weight=1)
        
        # Frame chứa biểu đồ phân tích
        chart_frame = tk.Frame(self, bg=default_vals.DEFAULT_BG_COLOR)
        chart_frame.grid(row=2, column=0, columnspan=5, sticky='nsew', padx=40, pady=(0, 40))
        
        self.draw_analysis_charts(chart_frame)
        
        # Cấu hình grid cho layout responsive
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=3)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)
    
    def draw_analysis_charts(self, parent_frame):
        """Vẽ các biểu đồ phân tích chi tiết"""
        
        # ============= 1. Biểu đồ số lượng ngành theo khoa =============
        container1 = tk.Frame(parent_frame, bg='white', relief='solid', bd=2, cursor='hand2')
        container1.grid(row=0, column=0, padx=15, pady=10, sticky='nsew')
        container1.bind('<Button-1>', lambda e: self.show_major_by_dept_detail())
        
        major_by_dept = {}
        for major in self.majors:
            dept_id = major.department_id
            major_by_dept[dept_id] = major_by_dept.get(dept_id, 0) + 1
        
        dept_names = {}
        for dept in self.departments:
            dept_names[dept.id] = dept.name
        
        dept_labels = [dept_names.get(dept_id, f"Khoa {dept_id}") for dept_id in major_by_dept.keys()]
        dept_values = list(major_by_dept.values())
        
        fig1, ax1 = plt.subplots(figsize=(5, 4))
        bars1 = ax1.bar(dept_labels, dept_values, color='#4ECDC4', edgecolor='#2C3E50', linewidth=1.5)
        ax1.set_title("Số lượng ngành theo khoa)", fontsize=12, fontweight='bold', pad=10)
        ax1.set_xlabel("Khoa", fontsize=10, fontweight='bold')
        ax1.set_ylabel("Số lượng ngành", fontsize=10, fontweight='bold')
        ax1.tick_params(axis='x', rotation=15, labelsize=8)
        ax1.grid(axis='y', alpha=0.3, linestyle='--')
        
        for bar in bars1:
            height = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2., height, f'{int(height)}',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)
        
        plt.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=container1)
        canvas1.draw()
        canvas1_widget = canvas1.get_tk_widget()
        canvas1_widget.pack(padx=5, pady=5)
        canvas1_widget.bind('<Button-1>', lambda e: self.show_major_by_dept_detail())
        
        # ============= 2. Biểu đồ số lượng lớp theo ngành =============
        container2 = tk.Frame(parent_frame, bg='white', relief='solid', bd=2, cursor='hand2')
        container2.grid(row=0, column=1, padx=15, pady=10, sticky='nsew')
        container2.bind('<Button-1>', lambda e: self.show_class_by_major_detail())
        
        class_by_major = {}
        for cls in self.departmental_classes:
            major_id = cls.major_id
            class_by_major[major_id] = class_by_major.get(major_id, 0) + 1
        
        major_names = {}
        for major in self.majors:
            major_names[major.id] = major.name
        
        major_labels = [major_names.get(major_id, f"Ngành {major_id}") for major_id in class_by_major.keys()]
        major_values = list(class_by_major.values())
        
        fig2, ax2 = plt.subplots(figsize=(5, 4))
        bars2 = ax2.barh(major_labels, major_values, color='#FFA07A', edgecolor='#2C3E50', linewidth=1.5)
        ax2.set_title("Số lượng lớp theo ngành)", fontsize=12, fontweight='bold', pad=10)
        ax2.set_xlabel("Số lượng lớp", fontsize=10, fontweight='bold')
        ax2.set_ylabel("Ngành", fontsize=10, fontweight='bold')
        ax2.tick_params(labelsize=8)
        ax2.grid(axis='x', alpha=0.3, linestyle='--')
        
        for bar in bars2:
            width = bar.get_width()
            ax2.text(width, bar.get_y() + bar.get_height()/2., f'{int(width)}',
                    ha='left', va='center', fontweight='bold', fontsize=9,
                    bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray', alpha=0.8))
        
        plt.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=container2)
        canvas2.draw()
        canvas2_widget = canvas2.get_tk_widget()
        canvas2_widget.pack(padx=5, pady=5)
        canvas2_widget.bind('<Button-1>', lambda e: self.show_class_by_major_detail())
        
        # ============= 3. Biểu đồ tròn phân bố môn học =============
        container3 = tk.Frame(parent_frame, bg='white', relief='solid', bd=2, cursor='hand2')
        container3.grid(row=0, column=2, padx=15, pady=10, sticky='nsew')
        container3.bind('<Button-1>', lambda e: self.show_subject_detail())
        
        fig3, ax3 = plt.subplots(figsize=(5, 4))
        
        coff_groups = {}
        for subject in self.subjects:
            coff = subject.coff
            coff_groups[coff] = coff_groups.get(coff, 0) + 1
        
        colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#FFA07A', '#98D8C8', '#F7DC6F', '#BB8FCE']
        wedges, texts, autotexts = ax3.pie(
            coff_groups.values(), 
            labels=[f"Hệ số {i}" for i, (key, value) in enumerate(coff_groups.items())], 
            autopct='%1.1f%%', 
            startangle=90,
            colors=colors[:len(coff_groups)],
            textprops={'fontsize': 9, 'fontweight': 'bold'},
            wedgeprops={'edgecolor': 'white', 'linewidth': 2}
        )
        
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')
        
        ax3.set_title("Phân bố môn học theo hệ số)", fontsize=12, fontweight='bold', pad=10)
        
        canvas3 = FigureCanvasTkAgg(fig3, master=container3)
        canvas3.draw()
        canvas3_widget = canvas3.get_tk_widget()
        canvas3_widget.pack(padx=5, pady=5)
        canvas3_widget.bind('<Button-1>', lambda e: self.show_subject_detail())
        
        # Cấu hình grid
        for i in range(3):
            parent_frame.grid_columnconfigure(i, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)
    
    # ==================== CHI TIẾT CARDS: DANH SÁCH TẤT CẢ ====================
    
    def show_all_subjects_detail(self):
        """Hiển thị chi tiết tất cả môn học"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📚 CHI TIẾT: DANH SÁCH TẤT CẢ MÔN HỌC",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        tree = ttk.Treeview(tree_frame, columns=('subject_id', 'subject_name', 'coff'),
                           show='headings', height=20)
        tree.heading('subject_id', text='Mã môn học')
        tree.heading('subject_name', text='Tên môn học')
        tree.heading('coff', text='Hệ số')
        
        tree.column('subject_id', width=200, anchor='center')
        tree.column('subject_name', width=600, anchor='w')
        tree.column('coff', width=150, anchor='center')
        
        # Insert dữ liệu
        for subject in sorted(self.subjects, key=lambda x: x.id):
            tree.insert('', 'end', values=(subject.id, subject.name, subject.coff))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_all_departments_detail(self):
        """Hiển thị chi tiết tất cả khoa"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="🏢 CHI TIẾT: DANH SÁCH TẤT CẢ KHOA",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        tree = ttk.Treeview(tree_frame, columns=('dept_id', 'dept_name'),
                           show='headings', height=20)
        tree.heading('dept_id', text='Mã Khoa')
        tree.heading('dept_name', text='Tên Khoa')
        
        tree.column('dept_id', width=200, anchor='center')
        tree.column('dept_name', width=750, anchor='w')
        
        # Insert dữ liệu
        for dept in sorted(self.departments, key=lambda x: x.id):
            tree.insert('', 'end', values=(dept.id, dept.name))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_all_majors_detail(self):
        """Hiển thị chi tiết tất cả ngành"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="🎓 CHI TIẾT: DANH SÁCH TẤT CẢ NGÀNH",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        # Tạo dict để map dept_id -> dept_name
        dept_names = {dept.id: dept.name for dept in self.departments}
        
        tree = ttk.Treeview(tree_frame, columns=('major_id', 'major_name', 'dept_name'),
                           show='headings', height=20)
        tree.heading('major_id', text='Mã Ngành')
        tree.heading('major_name', text='Tên Ngành')
        tree.heading('dept_name', text='Thuộc Khoa')
        
        tree.column('major_id', width=150, anchor='center')
        tree.column('major_name', width=400, anchor='w')
        tree.column('dept_name', width=400, anchor='w')
        
        # Insert dữ liệu
        for major in sorted(self.majors, key=lambda x: x.id):
            dept_name = dept_names.get(major.department_id, f"Khoa {major.department_id}")
            tree.insert('', 'end', values=(major.id, major.name, dept_name))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    def show_class_grade_statistics_detail(self):
        """Hiển thị thống kê điểm theo lớp"""
        self.clear_frame()
        self.parent.geometry("1600x900")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê",
                            font=("Arial", 12, "bold"), bg="#E74C3C", fg="white",
                            relief="flat", padx=15, pady=8, cursor="hand2",
                            command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📊 THỐNG KÊ ĐIỂM THEO LỚP",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Frame chọn lớp
        filter_frame = tk.Frame(self, bg='white', relief='solid', bd=1)
        filter_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(30, 10))
        
        tk.Label(filter_frame, text="Chọn lớp:", font=("Arial", 12, "bold"),
                bg='white').pack(side='left', padx=10, pady=10)
        
        class_var = tk.StringVar()
        class_combo = ttk.Combobox(filter_frame, textvariable=class_var,
                                width=30, state='readonly')
        class_combo['values'] = [f"{cls.id} - {cls.name}" 
                                for cls in sorted(self.departmental_classes, 
                                                key=lambda x: x.id)]
        class_combo.pack(side='left', padx=10, pady=10)
        
        # Treeview hiển thị kết quả
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=2, column=0, sticky='nsew', padx=30, pady=10)
        
        tree = ttk.Treeview(tree_frame, columns=(
            'stt', 'student_id', 'student_name', 'subject_count',
            'avg_10', 'avg_4', 'letter_grade'
        ), show='headings', height=20)
        
        tree.heading('stt', text='STT')
        tree.heading('student_id', text='MSSV')
        tree.heading('student_name', text='Họ và tên')
        tree.heading('subject_count', text='Số môn')
        tree.heading('avg_10', text='ĐTB (Thang 10)')
        tree.heading('avg_4', text='GPA (Thang 4)')
        tree.heading('letter_grade', text='Xếp loại')
        
        tree.column('stt', width=50, anchor='center')
        tree.column('student_id', width=120, anchor='center')
        tree.column('student_name', width=250, anchor='w')
        tree.column('subject_count', width=100, anchor='center')
        tree.column('avg_10', width=150, anchor='center')
        tree.column('avg_4', width=150, anchor='center')
        tree.column('letter_grade', width=120, anchor='center')
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        tree.bind('<Double-Button-1>', lambda e: self.on_student_double_click(tree))
        scrollbar.pack(side='right', fill='y')
        
        def on_class_select(event):
            """Xử lý khi chọn lớp"""
            selected = class_var.get()
            if not selected:
                return
            
            class_id = selected.split(' - ')[0]
            
            # Xóa dữ liệu cũ
            for item in tree.get_children():
                tree.delete(item)
            
            # Lấy và hiển thị thống kê
            from service.grade_statistics import get_class_statistics
            stats = get_class_statistics(class_id)
            
            for idx, stat in enumerate(stats, 1):
                # Tô màu theo xếp loại
                grade = stat['letter_grade']
                if grade == 'A':
                    tag = 'excellent'
                elif grade in ['B+', 'B']:
                    tag = 'good'
                elif grade in ['C+', 'C']:
                    tag = 'average'
                elif grade in ['D+', 'D']:
                    tag = 'poor'
                else:
                    tag = 'fail'
                
                tree.insert('', 'end', values=(
                    idx,
                    stat['student_id'],
                    stat['student_name'],
                    stat['subject_count'],
                    stat['avg_score_10'],
                    stat['avg_gpa_4'],
                    stat['letter_grade']
                ), tags=(tag,))
            
            # Cấu hình màu sắc
            tree.tag_configure('excellent', background='#D4EDDA')
            tree.tag_configure('good', background='#D1ECF1')
            tree.tag_configure('average', background='#FFF3CD')
            tree.tag_configure('poor', background='#F8D7DA')
            tree.tag_configure('fail', background='#F5C6CB')
        
        class_combo.bind('<<ComboboxSelected>>', on_class_select)
        
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def on_student_double_click(self, tree):
        """Xử lý khi double-click vào sinh viên trong danh sách"""
        import tkinter as tk
        from tkinter import messagebox
        
        # Lấy item được chọn
        selected_item = tree.selection()
        if not selected_item:
            return
        
        # Lấy giá trị của dòng được chọn
        values = tree.item(selected_item[0], 'values')
        if not values or len(values) < 2:
            return
        
        # values[1] là MSSV (student_id)
        student_id = values[1]
        
        # Hiển thị chi tiết điểm
        self.show_student_score_detail(student_id)
        
    def show_all_departmental_classes_detail(self):
        """Hiển thị chi tiết tất cả lớp"""
        self.clear_frame()
        self.parent.geometry("1400x800")
            
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="👥 CHI TIẾT: DANH SÁCH TẤT CẢ LỚP",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        # Tạo dict để map major_id -> major_name
        major_names = {major.id: major.name for major in self.majors}
        
        tree = ttk.Treeview(tree_frame, columns=('class_id', 'class_name', 'major_name'),
                           show='headings', height=20)
        tree.heading('class_id', text='Mã Lớp')
        tree.heading('class_name', text='Tên Lớp')
        tree.heading('major_name', text='Thuộc Ngành')
        
        tree.column('class_id', width=200, anchor='center')
        tree.column('class_name', width=350, anchor='w')
        tree.column('major_name', width=400, anchor='w')
        
        # Insert dữ liệu
        for cls in sorted(self.departmental_classes, key=lambda x: x.id):
            major_name = major_names.get(cls.major_id, f"Ngành {cls.major_id}")
            tree.insert('', 'end', values=(cls.id, cls.name, major_name))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        tree.bind('<Double-Button-1>', lambda e: self.on_student_double_click(tree))

        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_all_sectional_classes_detail(self):
        """Hiển thị chi tiết tất cả lớp học phần"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📖 CHI TIẾT: DANH SÁCH TẤT CẢ LỚP HỌC PHẦN",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        # Tạo dict để map subject_id -> subject_name và major_id -> major_name
        subject_names = {subject.id: subject.name for subject in self.subjects}
        major_names = {major.id: major.name for major in self.majors}
        
        tree = ttk.Treeview(tree_frame, columns=('class_id', 'class_name', 'subject_name', 'major_name', 'semester_id'),
                           show='headings', height=20)
        tree.heading('class_id', text='Mã Lớp HP')
        tree.heading('class_name', text='Tên Lớp HP')
        tree.heading('subject_name', text='Môn học')
        tree.heading('major_name', text='Ngành')
        tree.heading('semester_id', text='Học kỳ')
        
        tree.column('class_id', width=100, anchor='center')
        tree.column('class_name', width=200, anchor='w')
        tree.column('subject_name', width=300, anchor='w')
        tree.column('major_name', width=250, anchor='w')
        tree.column('semester_id', width=100, anchor='center')
        
        # Insert dữ liệu
        for cls in sorted(self.sectional_classes, key=lambda x: x.id):
            subject_name = subject_names.get(cls.subject_id, f"Môn {cls.subject_id}")
            major_name = major_names.get(cls.major_id, f"Ngành {cls.major_id}")
            tree.insert('', 'end', values=(cls.id, cls.name, subject_name, major_name, cls.semester_id))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    # ==================== CHI TIẾT BIỂU ĐỒ 1: NGÀNH THEO KHOA ====================
    
    def show_major_by_dept_detail(self):
        """Hiển thị chi tiết ngành theo khoa"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📊 CHI TIẾT: SỐ LƯỢNG NGÀNH THEO KHOA",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Tính toán dữ liệu
        major_by_dept = {}
        dept_names = {dept.id: dept.name for dept in self.departments}
        
        for major in self.majors:
            dept_id = major.department_id
            if dept_id not in major_by_dept:
                major_by_dept[dept_id] = []
            major_by_dept[dept_id].append(major)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        tree = ttk.Treeview(tree_frame, columns=('dept_id', 'dept_name', 'major_count', 'majors'),
                           show='headings', height=20)
        tree.heading('dept_id', text='Mã Khoa')
        tree.heading('dept_name', text='Tên Khoa')
        tree.heading('major_count', text='Số lượng Ngành')
        tree.heading('majors', text='Danh sách Ngành')
        
        tree.column('dept_id', width=100, anchor='center')
        tree.column('dept_name', width=250, anchor='w')
        tree.column('major_count', width=150, anchor='center')
        tree.column('majors', width=600, anchor='w')
        
        for dept_id, majors_list in sorted(major_by_dept.items()):
            dept_name = dept_names.get(dept_id, f"Khoa {dept_id}")
            major_names = ", ".join([m.name for m in majors_list])
            tree.insert('', 'end', values=(dept_id, dept_name, len(majors_list), major_names))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    # ==================== CHI TIẾT BIỂU ĐỒ 2: LỚP THEO NGÀNH ====================
    
    def show_class_by_major_detail(self):
        """Hiển thị chi tiết lớp theo ngành"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📊 CHI TIẾT: SỐ LƯỢNG LỚP THEO NGÀNH",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Tính toán dữ liệu
        class_by_major = {}
        major_names = {major.id: major.name for major in self.majors}
        
        for cls in self.departmental_classes:
            major_id = cls.major_id
            if major_id not in class_by_major:
                class_by_major[major_id] = []
            class_by_major[major_id].append(cls)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        tree = ttk.Treeview(tree_frame, columns=('major_id', 'major_name', 'class_count', 'classes'),
                           show='headings', height=20)
        tree.heading('major_id', text='Mã Ngành')
        tree.heading('major_name', text='Tên Ngành')
        tree.heading('class_count', text='Số lượng Lớp')
        tree.heading('classes', text='Danh sách Lớp')
        
        tree.column('major_id', width=100, anchor='center')
        tree.column('major_name', width=250, anchor='w')
        tree.column('class_count', width=150, anchor='center')
        tree.column('classes', width=600, anchor='w')
        
        for major_id, classes_list in sorted(class_by_major.items()):
            major_name = major_names.get(major_id, f"Ngành {major_id}")
            class_names = ", ".join([c.id for c in classes_list])
            tree.insert('', 'end', values=(major_id, major_name, len(classes_list), class_names))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    # ==================== CHI TIẾT BIỂU ĐỒ 3: MÔN HỌC THEO HỆ SỐ ====================
    
    def show_subject_detail(self):
        """Hiển thị chi tiết môn học theo hệ số"""
        self.clear_frame()
        self.parent.geometry("1400x800")
        
        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(header_frame, text="← Quay lại Thống kê", font=("Arial", 12, "bold"),
                            bg="#E74C3C", fg="white", relief="flat", padx=15, pady=8,
                            cursor="hand2", command=self.show_statistics)
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(header_frame, text="📊 CHI TIẾT: DANH SÁCH MÔN HỌC THEO HỆ SỐ",
                        font=("Arial", 18, "bold"), bg="#2C3E50", fg="white")
        title.pack(side='left', padx=30, pady=15)
        
        # Tính toán dữ liệu
        subjects_by_coff = {}
        for subject in self.subjects:
            coff = subject.coff
            if coff not in subjects_by_coff:
                subjects_by_coff[coff] = []
            subjects_by_coff[coff].append(subject)
        
        # Treeview
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)
        
        tree = ttk.Treeview(tree_frame, columns=('coff', 'subject_count', 'subject_id', 'subject_name'),
                           show='headings', height=20)
        tree.heading('coff', text='Hệ số')
        tree.heading('subject_count', text='Số lượng')
        tree.heading('subject_id', text='Mã môn học')
        tree.heading('subject_name', text='Tên môn học')
        
        tree.column('coff', width=100, anchor='center')
        tree.column('subject_count', width=100, anchor='center')
        tree.column('subject_id', width=150, anchor='center')
        tree.column('subject_name', width=500, anchor='w')
        
        for coff, subjects_list in sorted(subjects_by_coff.items()):
            # Insert parent row
            parent = tree.insert('', 'end', values=(f"Hệ số {coff}", len(subjects_list), '', ''),
                               tags=('parent',))
            # Insert children
            for subject in subjects_list:
                tree.insert(parent, 'end', values=(coff, '', subject.id, subject.name))
        
        tree.tag_configure('parent', background='#E8F4F8', font=('Arial', 10, 'bold'))
        
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def show_student_score_detail(self, student_id):
        """Hiển thị chi tiết điểm của sinh viên"""
        import tkinter as tk
        from tkinter import ttk
        from service.grade_statistics import get_student_detailed_scores, get_letter_grade
        
        # Lấy dữ liệu
        data = get_student_detailed_scores(student_id)
        if not data:
            from tkinter import messagebox
            messagebox.showerror("Lỗi", "Không tìm thấy thông tin sinh viên!")
            return
        
        # Xóa frame hiện tại
        self.clear_frame()
        self.parent.geometry("1600x900")
        
        # ========== HEADER ==========
        header_frame = tk.Frame(self, bg='#2C3E50', height=70)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=2)
        header_frame.grid_propagate(False)
        
        back_btn = tk.Button(
            header_frame, 
            text="← Quay lại Thống kê điểm",
            font=("Arial", 12, "bold"), 
            bg="#E74C3C", 
            fg="white",
            relief="flat", 
            padx=15, 
            pady=8, 
            cursor="hand2",
            command=self.show_class_grade_statistics_detail
        )
        back_btn.pack(side='left', padx=20, pady=15)
        
        title = tk.Label(
            header_frame, 
            text=f"📊 CHI TIẾT ĐIỂM: {data['student_name']}",
            font=("Arial", 18, "bold"), 
            bg="#2C3E50", 
            fg="white"
        )
        title.pack(side='left', padx=30, pady=15)
        
        # ========== THÔNG TIN SINH VIÊN ==========
        info_frame = tk.Frame(self, bg='white', relief='solid', bd=2)
        info_frame.grid(row=1, column=0, sticky='ew', padx=30, pady=(30, 10))
        
        tk.Label(
            info_frame, 
            text="THÔNG TIN SINH VIÊN", 
            font=("Arial", 14, "bold"), 
            bg='#3498DB', 
            fg='white',
            padx=10, 
            pady=5
        ).pack(fill='x')
        
        info_content = tk.Frame(info_frame, bg='white')
        info_content.pack(fill='x', padx=20, pady=10)
        
        # Hiển thị thông tin
        info_labels = [
            ("MSSV:", data['student_id']),
            ("Họ và tên:", data['student_name']),
            ("Ngày sinh:", data['student_dob']),
            ("Giới tính:", data['student_gender']),
            ("Lớp:", data['student_class'])
        ]
        
        for i, (label, value) in enumerate(info_labels):
            row_frame = tk.Frame(info_content, bg='white')
            row_frame.pack(fill='x', pady=2)
            
            tk.Label(
                row_frame, 
                text=label, 
                font=("Arial", 11, "bold"),
                bg='white', 
                width=15, 
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row_frame, 
                text=str(value), 
                font=("Arial", 11),
                bg='white', 
                anchor='w'
            ).pack(side='left', padx=10)
        
        # ========== BẢNG ĐIỂM CHI TIẾT ==========
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=2, column=0, sticky='nsew', padx=30, pady=10)
        
        # Tạo Treeview
        columns = (
            'stt', 'subject_id', 'subject_name', 'coff',
            'regular1', 'regular2', 'regular3', 'midterm', 
            'final', 'average', 'gpa_4', 'letter_grade'
        )
        
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=15)
        
        # Định nghĩa headers
        headers = {
            'stt': 'STT',
            'subject_id': 'Mã MH',
            'subject_name': 'Tên môn học',
            'coff': 'Hệ số',
            'regular1': 'Regular 1',
            'regular2': 'Regular 2',
            'regular3': 'Regular 3',
            'midterm': 'Midterm',
            'final': 'Final',
            'average': 'TB (10)',
            'gpa_4': 'GPA (4)',
            'letter_grade': 'Xếp loại'
        }
        
        # Định nghĩa độ rộng cột
        widths = {
            'stt': 50, 
            'subject_id': 80, 
            'subject_name': 250, 
            'coff': 60,
            'regular1': 80, 
            'regular2': 80, 
            'regular3': 80,
            'midterm': 80, 
            'final': 80, 
            'average': 80,
            'gpa_4': 80, 
            'letter_grade': 80
        }
        
        for col in columns:
            tree.heading(col, text=headers[col])
            tree.column(col, width=widths[col], anchor='center')
        
        tree.column('subject_name', anchor='w')  # Tên môn căn trái
        
        # Insert dữ liệu
        for idx, score in enumerate(data['scores'], 1):
            # Tô màu theo xếp loại
            grade = score['letter_grade']
            if grade == 'A':
                tag = 'excellent'
            elif grade in ['B+', 'B']:
                tag = 'good'
            elif grade in ['C+', 'C']:
                tag = 'average'
            elif grade in ['D+', 'D']:
                tag = 'poor'
            else:
                tag = 'fail'
            
            tree.insert('', 'end', values=(
                idx,
                score['subject_id'],
                score['subject_name'],
                get_coefficient_name(score['subject_coff']),
                score['regular1'],
                score['regular2'],
                score['regular3'],
                score['midterm'],
                score['final'],
                score['average'],
                score['gpa_4'],
                score['letter_grade']
            ), tags=(tag,))
        
        # Cấu hình màu sắc
        tree.tag_configure('excellent', background='#D4EDDA')
        tree.tag_configure('good', background='#D1ECF1')
        tree.tag_configure('average', background='#FFF3CD')
        tree.tag_configure('poor', background='#F8D7DA')
        tree.tag_configure('fail', background='#F5C6CB')
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ========== TỔNG KẾT ==========
        summary_frame = tk.Frame(self, bg='white', relief='solid', bd=2)
        summary_frame.grid(row=3, column=0, sticky='ew', padx=30, pady=(10, 30))
        
        # Tính tổng kết
        total_subjects = len(data['scores'])

        if total_subjects > 0:
            # Import các hàm cần thiết
            from service.grade_statistics import calculate_subject_average, convert_to_gpa_4
            from types import SimpleNamespace
            import json
            
            # Tính lại điểm cho từng môn với hệ số đúng
            total_avg_10 = 0
            total_gpa_4 = 0
            
            for score_data in data['scores']:
                # Parse hệ số từ JSON string
                if isinstance(score_data['subject_coff'], str):
                    coff_dict = json.loads(score_data['subject_coff'].replace("'", '"'))
                else:
                    coff_dict = score_data['subject_coff']
                
                # Tạo object score để truyền vào hàm
                score_obj = SimpleNamespace(
                    regular1=score_data['regular1'],
                    regular2=score_data['regular2'],
                    regular3=score_data['regular3'],
                    midterm=score_data['midterm'],
                    final=score_data['final']
                )
                
                # Tính điểm trung bình môn với hệ số đúng
                avg = calculate_subject_average(score_obj, coff_dict)
                total_avg_10 += avg
                total_gpa_4 += convert_to_gpa_4(avg)
            
            # Tính trung bình tổng
            total_avg_10 = round(total_avg_10 / total_subjects, 2)
            total_gpa_4 = round(total_gpa_4 / total_subjects, 2)
            overall_grade = get_letter_grade(total_avg_10)
        else:
            total_avg_10 = 0
            total_gpa_4 = 0
            overall_grade = 'N/A'
        
        tk.Label(
            summary_frame, 
            text="TỔNG KẾT", 
            font=("Arial", 14, "bold"), 
            bg='#27AE60', 
            fg='white',
            padx=10, 
            pady=5
        ).pack(fill='x')
        
        summary_content = tk.Frame(summary_frame, bg='white')
        summary_content.pack(fill='x', padx=20, pady=10)
        
        summary_labels = [
            ("Tổng số môn:", total_subjects),
            ("Điểm TB (Thang 10):", f"{total_avg_10:.2f}"),
            ("GPA (Thang 4):", f"{total_gpa_4:.2f}"),
            ("Xếp loại tổng kết:", overall_grade)
        ]
        
        for label, value in summary_labels:
            row_frame = tk.Frame(summary_content, bg='white')
            row_frame.pack(fill='x', pady=2)
            
            tk.Label(
                row_frame, 
                text=label, 
                font=("Arial", 12, "bold"),
                bg='white', 
                width=20, 
                anchor='w'
            ).pack(side='left')
            
            tk.Label(
                row_frame, 
                text=str(value), 
                font=("Arial", 12),
                bg='white', 
                fg='#E74C3C', 
                anchor='w'
            ).pack(side='left', padx=10)
        
        # Cấu hình grid
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)
    def go_back_to_dashboard(self):
        """Quay lại dashboard chính"""

        self.clear_frame()
        self.widgets()
