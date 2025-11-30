import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from util.util import default_vals
from service.subject import get_all_subjects
from service.department import get_all_departments
from service.major import get_all_majors
from service.departmental_class import get_all_classes as get_all_departmental_classes
from service.sectional_class import get_all_classes as get_all_sectional_classes
from service.grade_statistics import get_class_statistics
import json


class StudentStatistics(tk.Frame):
    def __init__(self, parent, back_callback):
        super().__init__(parent)
        self.parent = parent
        self.back_callback = back_callback
        # Fallback for background color
        bg_color = default_vals.DEFAULT_BG_COLOR if hasattr(default_vals, 'DEFAULT_BG_COLOR') else 'white'
        self.config(bg=bg_color)

        # Load data
        self.subjects = get_all_subjects()
        self.departments = get_all_departments()
        self.majors = get_all_majors()
        self.departmental_classes = get_all_departmental_classes()
        self.sectional_classes = get_all_sectional_classes()

        self.setup_main_view()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def setup_main_view(self):
        """Displays the main statistics dashboard"""
        self.clear_frame()
        self.parent.geometry("1600x900")

        # Header
        header_frame = tk.Frame(self, bg='#2C3E50', height=80)
        header_frame.grid(row=0, column=0, sticky='ew', columnspan=5)
        header_frame.grid_propagate(False)

        # Back Button
        back_btn = tk.Button(
            header_frame,
            text="← Back to Dashboard",
            font=("Arial", 14, "bold"),
            bg="#E74C3C",
            fg="white",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2",
            command=self.back_callback
        )
        back_btn.pack(side='left', padx=20, pady=15)

        # Title
        title_label = tk.Label(
            header_frame,
            text="📊 UNIVERSITY SYSTEM STATISTICS",
            font=("Arial", 20, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        title_label.pack(side='left', padx=50, pady=15)

        # Stats Container
        stats_container = tk.Frame(self, bg=self["bg"])
        stats_container.grid(row=1, column=0, columnspan=5, sticky='nsew', padx=40, pady=40)

        # Card Data
        stats_data = [
            ("📚", "Total Subjects", len(self.subjects), "#FF6B6B"),
            ("🏢", "Total Departments", len(self.departments), "#4ECDC4"),
            ("🎓", "Total Majors", len(self.majors), "#45B7D1"),
            ("👥", "Total Classes", len(self.departmental_classes), "#FFA07A"),
            ("📖", "Total Sectional Classes", len(self.sectional_classes), "#98D8C8"),
            ("📊", "Grade Statistics", "By Class", "#9B59B6")
        ]

        # Create Cards
        for idx, (icon, label, value, bg_color) in enumerate(stats_data):
            self.create_stat_card(stats_container, idx, icon, label, value, bg_color)

        # Charts Frame
        chart_frame = tk.Frame(self, bg=self["bg"])
        chart_frame.grid(row=2, column=0, columnspan=5, sticky='nsew', padx=40, pady=(0, 40))

        self.draw_analysis_charts(chart_frame)

        # Grid config
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=2)
        self.grid_rowconfigure(2, weight=3)
        for i in range(5):
            self.grid_columnconfigure(i, weight=1)

    def create_stat_card(self, container, idx, icon, label, value, bg_color):
        """Helper to create statistics card"""
        handlers = [
            self.show_all_subjects_detail,
            self.show_all_departments_detail,
            self.show_all_majors_detail,
            self.show_all_departmental_classes_detail,
            self.show_all_sectional_classes_detail,
            self.show_class_grade_statistics_detail
        ]
        handler = handlers[idx]

        card_frame = tk.Frame(container, bg=self["bg"])
        card_frame.grid(row=0, column=idx, padx=15, pady=20, sticky='nsew')

        shadow = tk.Frame(card_frame, bg='#CCCCCC')
        shadow.pack(padx=3, pady=3, fill='both', expand=True)

        card = tk.Frame(shadow, bg=bg_color, cursor='hand2')
        card.pack(fill='both', expand=True)
        card.bind('<Button-1>', lambda e: handler())

        tk.Label(card, text=icon, font=("Segoe UI Emoji", 48), bg=bg_color, fg='white').pack(pady=(25, 10))
        tk.Label(card, text=label, font=("Arial", 13, "bold"), bg=bg_color, fg='white').pack(pady=(0, 5))

        val_frame = tk.Frame(card, bg='white')
        val_frame.pack(pady=(10, 25), padx=20)
        tk.Label(val_frame, text=str(value), font=("Arial", 36, "bold"), bg='white', fg=bg_color, padx=20,
                 pady=5).pack()

        # Bind click event to children
        for widget in card.winfo_children() + [val_frame.winfo_children()[0]]:
            widget.bind('<Button-1>', lambda e: handler())
            widget.configure(cursor='hand2')

        container.grid_columnconfigure(idx, weight=1)

    def draw_analysis_charts(self, parent_frame):
        # 1. Majors by Department
        self.draw_chart_container(parent_frame, 0, "Majors by Department",
                                  self.get_majors_by_dept_data(),
                                  self.show_major_by_dept_detail)

        # 2. Classes by Major
        self.draw_chart_container(parent_frame, 1, "Classes by Major",
                                  self.get_classes_by_major_data(),
                                  self.show_class_by_major_detail, is_barh=True)

        # 3. Subject Weight Distribution
        self.draw_pie_chart(parent_frame, 2)

        for i in range(3):
            parent_frame.grid_columnconfigure(i, weight=1)
        parent_frame.grid_rowconfigure(0, weight=1)

    def get_majors_by_dept_data(self):
        counts = {}
        for m in self.majors:
            counts[m.department_id] = counts.get(m.department_id, 0) + 1
        dept_map = {d.id: d.name for d in self.departments}
        return [dept_map.get(k, f"Dept {k}") for k in counts.keys()], list(counts.values())

    def get_classes_by_major_data(self):
        counts = {}
        for c in self.departmental_classes:
            counts[c.major_id] = counts.get(c.major_id, 0) + 1
        major_map = {m.id: m.name for m in self.majors}
        return [major_map.get(k, f"Major {k}") for k in counts.keys()], list(counts.values())

    def draw_chart_container(self, parent, col, title, data, handler, is_barh=False):
        labels, values = data
        container = tk.Frame(parent, bg='white', relief='solid', bd=2, cursor='hand2')
        container.grid(row=0, column=col, padx=15, pady=10, sticky='nsew')
        container.bind('<Button-1>', lambda e: handler())

        fig, ax = plt.subplots(figsize=(5, 4))
        if is_barh:
            bars = ax.barh(labels, values, color='#FFA07A', edgecolor='#2C3E50')
            ax.bar_label(bars)
        else:
            bars = ax.bar(labels, values, color='#4ECDC4', edgecolor='#2C3E50')
            ax.bar_label(bars)
            ax.tick_params(axis='x', rotation=15)

        ax.set_title(title, fontweight='bold', fontsize=10)
        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=5)
        canvas.get_tk_widget().bind('<Button-1>', lambda e: handler())

    def format_coefficient_string(self, coff_data):
        """Helper to format JSON or string coefficient into readable text"""
        try:
            if isinstance(coff_data, str):
                c = json.loads(coff_data)
            else:
                c = coff_data

            # Format: R:20% M:30% F:50%
            reg = (c.get('reg1', 0) + c.get('reg2', 0) + c.get('reg3', 0)) * 100
            mid = c.get('mid', 0) * 100
            fin = c.get('fin', 0) * 100

            return f"Reg: {int(reg)}%, Mid: {int(mid)}%, Fin: {int(fin)}%"
        except:
            return "Unknown"

    def draw_pie_chart(self, parent, col):
        container = tk.Frame(parent, bg='white', relief='solid', bd=2, cursor='hand2')
        container.grid(row=0, column=col, padx=15, pady=10, sticky='nsew')
        container.bind('<Button-1>', lambda e: self.show_subject_detail())

        counts = {}
        for s in self.subjects:
            # Group by formatted string to handle the JSON logic
            key = self.format_coefficient_string(s.coff)
            counts[key] = counts.get(key, 0) + 1

        fig, ax = plt.subplots(figsize=(5, 4))

        # Determine labels and values
        labels = list(counts.keys())
        values = list(counts.values())

        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, textprops={'fontsize': 8})
        ax.set_title("Subject Weight Distribution", fontweight='bold', fontsize=10)

        canvas = FigureCanvasTkAgg(fig, master=container)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=5, pady=5)
        canvas.get_tk_widget().bind('<Button-1>', lambda e: self.show_subject_detail())

    # ================= DETAIL VIEWS =================

    def create_detail_view(self, title_text, columns, data_provider):
        self.clear_frame()
        self.parent.geometry("1400x800")

        # Header
        header = tk.Frame(self, bg='#2C3E50', height=70)
        header.grid(row=0, column=0, sticky='ew')
        header.grid_propagate(False)

        tk.Button(header, text="← Back", font=("Arial", 12, "bold"),
                  bg="#E74C3C", fg="white", command=self.setup_main_view).pack(side='left', padx=20)

        tk.Label(header, text=title_text, font=("Arial", 18, "bold"),
                 bg="#2C3E50", fg="white").pack(side='left', padx=30)

        # Treeview
        frame = tk.Frame(self, bg='white')
        frame.grid(row=1, column=0, sticky='nsew', padx=30, pady=30)

        tree = ttk.Treeview(frame, columns=list(columns.keys()), show='headings', height=20)
        for col_id, col_name in columns.items():
            tree.heading(col_id, text=col_name)
            tree.column(col_id, width=150)  # Default width

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        data_provider(tree)

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def show_all_subjects_detail(self):
        def provider(tree):
            tree.column('name', width=400)
            tree.column('coff', width=300)
            for s in sorted(self.subjects, key=lambda x: x.id):
                fmt_coff = self.format_coefficient_string(s.coff)
                tree.insert('', 'end', values=(s.id, s.name, fmt_coff))

        self.create_detail_view("LIST OF SUBJECTS",
                                {'id': 'Subject ID', 'name': 'Subject Name', 'coff': 'Weight Config'},
                                provider)

    def show_all_departments_detail(self):
        def provider(tree):
            tree.column('name', width=500)
            for d in sorted(self.departments, key=lambda x: x.id):
                tree.insert('', 'end', values=(d.id, d.name))

        self.create_detail_view("LIST OF DEPARTMENTS",
                                {'id': 'Dept ID', 'name': 'Department Name'}, provider)

    def show_all_majors_detail(self):
        dept_map = {d.id: d.name for d in self.departments}

        def provider(tree):
            tree.column('name', width=400)
            tree.column('dept', width=400)
            for m in sorted(self.majors, key=lambda x: x.id):
                # Ensure department_id attribute name matches service (might be department_id or departmental_id based on previous files)
                # Checking service/major.py -> it returns 'department_id'
                dept_name = dept_map.get(m.department_id, f"Dept {m.department_id}")
                tree.insert('', 'end', values=(m.id, m.name, dept_name))

        self.create_detail_view("LIST OF MAJORS",
                                {'id': 'Major ID', 'name': 'Major Name', 'dept': 'Department'}, provider)

    def show_all_departmental_classes_detail(self):
        major_map = {m.id: m.name for m in self.majors}

        def provider(tree):
            tree.column('name', width=300)
            tree.column('major', width=400)
            for c in sorted(self.departmental_classes, key=lambda x: x.id):
                tree.insert('', 'end', values=(c.id, c.name, major_map.get(c.major_id, f"Major {c.major_id}")))

        self.create_detail_view("LIST OF CLASSES",
                                {'id': 'Class ID', 'name': 'Class Name', 'major': 'Major'}, provider)

    def show_all_sectional_classes_detail(self):
        sub_map = {s.id: s.name for s in self.subjects}
        major_map = {m.id: m.name for m in self.majors}

        def provider(tree):
            tree.column('sub', width=300)
            for c in sorted(self.sectional_classes, key=lambda x: x.id):
                tree.insert('', 'end', values=(
                    c.id, c.name,
                    sub_map.get(c.subject_id, c.subject_id),
                    major_map.get(c.major_id, c.major_id),
                    c.semester_id
                ))

        self.create_detail_view("LIST OF SECTIONAL CLASSES",
                                {'id': 'ID', 'name': 'Section Name', 'sub': 'Subject', 'maj': 'Major',
                                 'sem': 'Semester'},
                                provider)

    def show_major_by_dept_detail(self):
        dept_map = {d.id: d.name for d in self.departments}

        def provider(tree):
            tree.column('list', width=600)
            counts = {}
            for m in self.majors:
                if m.department_id not in counts: counts[m.department_id] = []
                counts[m.department_id].append(m.name)

            for did, mnames in counts.items():
                tree.insert('', 'end', values=(did, dept_map.get(did), len(mnames), ", ".join(mnames)))

        self.create_detail_view("DETAILS: MAJORS BY DEPARTMENT",
                                {'id': 'Dept ID', 'name': 'Department Name', 'count': 'Count', 'list': 'Majors List'},
                                provider)

    def show_class_by_major_detail(self):
        maj_map = {m.id: m.name for m in self.majors}

        def provider(tree):
            tree.column('list', width=600)
            counts = {}
            for c in self.departmental_classes:
                if c.major_id not in counts: counts[c.major_id] = []
                counts[c.major_id].append(c.id)

            for mid, cids in counts.items():
                tree.insert('', 'end', values=(mid, maj_map.get(mid), len(cids), ", ".join(cids)))

        self.create_detail_view("DETAILS: CLASSES BY MAJOR",
                                {'id': 'Major ID', 'name': 'Major Name', 'count': 'Count', 'list': 'Classes List'},
                                provider)

    def show_subject_detail(self):
        # Shows details grouped by weight configuration
        def provider(tree):
            tree.column('name', width=400)
            counts = {}
            for s in self.subjects:
                key = self.format_coefficient_string(s.coff)
                if key not in counts: counts[key] = []
                counts[key].append(s)

            for key, subs in sorted(counts.items()):
                p = tree.insert('', 'end', values=(key, len(subs), '', ''))
                for s in subs:
                    tree.insert(p, 'end', values=(key, '', s.id, s.name))

        self.create_detail_view("DETAILS: SUBJECTS BY WEIGHT CONFIG",
                                {'coff': 'Weight Config', 'cnt': 'Count', 'id': 'Subject ID', 'name': 'Subject Name'},
                                provider)

    def show_class_grade_statistics_detail(self):
        self.clear_frame()
        self.parent.geometry("1600x900")

        # Header
        header = tk.Frame(self, bg='#2C3E50', height=70)
        header.grid(row=0, column=0, sticky='ew')

        tk.Button(header, text="← Back", font=("Arial", 12, "bold"),
                  bg="#E74C3C", fg="white", command=self.setup_main_view).pack(side='left', padx=20)
        tk.Label(header, text="GRADE STATISTICS BY CLASS", font=("Arial", 18, "bold"),
                 bg="#2C3E50", fg="white").pack(side='left', padx=30)

        # Filter
        filter_fr = tk.Frame(self, bg='white')
        filter_fr.grid(row=1, column=0, sticky='ew', padx=30, pady=10)
        tk.Label(filter_fr, text="Select Class:", bg='white').pack(side='left', padx=10)

        class_var = tk.StringVar()
        combo = ttk.Combobox(filter_fr, textvariable=class_var, width=30, state='readonly')
        combo['values'] = [f"{c.id} - {c.name}" for c in sorted(self.departmental_classes, key=lambda x: x.id)]
        combo.pack(side='left', padx=10)

        # Tree
        tree_frame = tk.Frame(self, bg='white')
        tree_frame.grid(row=2, column=0, sticky='nsew', padx=30)

        cols = ['stt', 'id', 'name', 'count', 'avg10', 'avg4', 'grade']
        tree = ttk.Treeview(tree_frame, columns=cols, show='headings', height=20)
        headers = ['No.', 'Student ID', 'Name', 'Subjects', 'Avg (10)', 'GPA (4)', 'Grade']

        for c, h in zip(cols, headers):
            tree.heading(c, text=h)
            tree.column(c, anchor='center' if c != 'name' else 'w')

        scrollbar = ttk.Scrollbar(tree_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        def on_select(event):
            selected = class_var.get()
            if not selected: return
            class_id = selected.split(' - ')[0]

            for i in tree.get_children(): tree.delete(i)

            stats = get_class_statistics(class_id)
            for idx, s in enumerate(stats, 1):
                tree.insert('', 'end', values=(
                    idx, s['student_id'], s['student_name'], s['subject_count'],
                    s['avg_score_10'], s['avg_gpa_4'], s['letter_grade']
                ))

        combo.bind('<<ComboboxSelected>>', on_select)

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)