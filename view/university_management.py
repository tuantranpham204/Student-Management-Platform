import tkinter.ttk as ttk
import tkinter as tk
from tkinter import messagebox, filedialog
from tkcalendar import DateEntry
import util.util as util


class UniversityManagement(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.widgets()

    def widgets(self):
        self.fr_lst = tk.Frame(self)
        self.fr_mal = tk.Frame(self)
        self.fr_lst.grid(row=0, column=0, padx=10, pady=10)
        self.fr_mal.grid(row=0, column=1, padx=10, pady=10)

        # department
        self.fr_dep = tk.Frame(self.fr_mal)
        self.fr_dep.grid(row=0, column=0, padx=10, pady=10)

        self.lbl_dep_id = tk.Label(self.fr_dep, text='Department ID: ', anchor='w')
        self.lbl_dep_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_dep_id = tk.Entry(self.fr_dep)
        self.ent_dep_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_dep_name = tk.Label(self.fr_dep, text="Department Name: ")
        self.lbl_dep_name.grid(row=1, column=0, padx=10, pady=10)
        self.ent_dep_name = tk.Entry(self.fr_dep)
        self.ent_dep_name.grid(row=1, column=1, padx=10, pady=10)

        self.fr_btn_dep = tk.Frame(self.fr_dep)
        self.fr_btn_dep.grid(row=2, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_dep = tk.Button(self.fr_btn_dep, text="Add Department")
        self.btn_add_dep.grid(row=0, column=0, padx=10, pady=10)
        self.btn_upd_dep = tk.Button(self.fr_btn_dep, text="Update Department")
        self.btn_upd_dep.grid(row=0, column=1, padx=10, pady=10)


        # major
        self.fr_maj = tk.Frame(self.fr_mal)
        self.fr_maj.grid(row=1, column=0, padx=10, pady=10)

        self.lbl_maj_id = tk.Label(self.fr_maj, text='Major ID: ', anchor='w')
        self.lbl_maj_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_maj_id = tk.Entry(self.fr_maj)
        self.ent_maj_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_maj_name = tk.Label(self.fr_maj, text="Major name:")
        self.lbl_maj_name.grid(row=1, column=0, padx=10, pady=10)
        self.ent_maj_name = tk.Entry(self.fr_maj)
        self.ent_maj_name.grid(row=1, column=1, padx=10, pady=10)
        
        self.lbl_maj_dep = tk.Label(self.fr_maj, text="Major Department: ")
        self.lbl_maj_dep.grid(row=2, column=0, padx=10, pady=10)
        self.sel_maj_dep_var = tk.StringVar()
        self.sel_maj_dep = ttk.Combobox(self.fr_maj, textvariable=self.sel_maj_dep_var, state='readonly', width=27)
        self.sel_maj_dep.grid(row=2, column=1, padx=10, pady=10)
        # self.sel_maj_dep.bind("<<ComboboxSelected>>", self.on_department_select)

        self.fr_btn_maj = tk.Frame(self.fr_maj)
        self.fr_btn_maj.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_maj = tk.Button(self.fr_btn_maj, text="Add Major")
        self.btn_add_maj.grid(row=0, column=0, padx=10, pady=10)
        self.btn_upd_maj = tk.Button(self.fr_btn_maj, text="Update Major")
        self.btn_upd_maj.grid(row=0, column=1, padx=10, pady=10)


        # departmental class
        self.fr_dep_cls = tk.Frame(self.fr_mal)
        self.fr_dep_cls.grid(row=2, column=0, padx=10, pady=10)

        self.lbl_dep_cls_id = tk.Label(self.fr_dep_cls, text="Departmental class ID: ")
        self.lbl_dep_cls_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_dep_cls_id = tk.Entry(self.fr_dep_cls)
        self.ent_dep_cls_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_dep_cls_name = tk.Label(self.fr_dep_cls, text="Departmental class name: ")
        self.lbl_dep_cls_name.grid(row=1, column=0, padx=10, pady=10)
        self.ent_dep_cls_name = tk.Entry(self.fr_dep_cls)
        self.ent_dep_cls_name.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_dep_cls_maj = tk.Label(self.fr_dep_cls, text="Departmental class Major: ")
        self.lbl_dep_cls_maj.grid(row=2, column=0, padx=10, pady=10)
        self.sel_dep_cls_maj_var = tk.StringVar()
        self.sel_dep_cls_maj = tk.ttk.Combobox(self.fr_dep_cls, textvariable=self.sel_dep_cls_maj_var, state='readonly', width=27)
        self.sel_dep_cls_maj.grid(row=2, column=1, padx=10, pady=10)

        self.fr_btn_dep_cls = tk.Frame(self.fr_dep_cls)
        self.fr_btn_dep_cls.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_dep_cls = tk.Button(self.fr_btn_dep_cls, text="Add Departmental class")
        self.btn_add_dep_cls.grid(row=0, column=0, padx=10, pady=10)
        self.btn_add_dep_cls = tk.Button(self.fr_btn_dep_cls, text="Update Departmental class")
        self.btn_add_dep_cls.grid(row=0, column=1, padx=10, pady=10)

        # semester
        self.fr_sem = tk.Frame(self.fr_mal)
        self.fr_sem.grid(row=3, column=0, padx=10, pady=10)

        self.lbl_sem_id = tk.Label(self.fr_sem, text="Semester ID: ")
        self.lbl_sem_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_sem_id = tk.Entry(self.fr_sem)
        self.ent_sem_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_sem_year = tk.Label(self.fr_sem, text="Semester: ")
        self.lbl_sem_year.grid(row=1, column=0, padx=10, pady=10)
        self.ent_sem_year = tk.Entry(self.fr_sem)
        self.ent_sem_year.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_sem_term = tk.Label(self.fr_sem, text="Term: ")
        self.lbl_sem_term.grid(row=2, column=0, padx=10, pady=10)
        self.sel_sem_term_var = tk.StringVar()
        self.sel_sem_term = ttk.Combobox(self.fr_sem, textvariable=self.sel_sem_term_var, state='readonly', width=27)
        self.sel_sem_term.grid(row=2, column=1, padx=10, pady=10)

        self.fr_btn_sem = tk.Frame(self.fr_sem)
        self.fr_btn_sem.grid(row=3, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_sem = tk.Button(self.fr_btn_sem, text="Add Semester")
        self.btn_add_sem.grid(row=0, column=0, padx=10, pady=10)
        self.btn_upd_sem = tk.Button(self.fr_btn_sem, text="Update Semester")
        self.btn_upd_sem.grid(row=0, column=1, padx=10, pady=10)

        # subject
        self.fr_subj = tk.Frame(self.fr_mal)
        self.fr_subj.grid(row=0, column=2, padx=10, pady=10, rowspan=2)

        self.lbl_subj_id = tk.Label(self.fr_subj, text="Subject ID: ")
        self.lbl_subj_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_subj_id = tk.Entry(self.fr_subj)
        self.ent_subj_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_subj_name = tk.Label(self.fr_subj, text="Subject name: ")
        self.lbl_subj_name.grid(row=1, column=0, padx=10, pady=10)
        self.ent_subj_name = tk.Entry(self.fr_subj)
        self.ent_subj_name.grid(row=1, column=1, padx=10, pady=10)

            # coefficient fields
        self.lbl_coff_reg1 = tk.Label(self.fr_subj, text="Regular 1 coefficient: ")
        self.lbl_coff_reg1.grid(row=2, column=0, padx=10, pady=10)
        self.ent_coff_reg1 = tk.Entry(self.fr_subj)
        self.ent_coff_reg1.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_coff_reg2 = tk.Label(self.fr_subj, text="Regular 2 coefficient: ")
        self.lbl_coff_reg2.grid(row=3, column=0, padx=10, pady=10)
        self.ent_coff_reg2 = tk.Entry(self.fr_subj)
        self.ent_coff_reg2.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_coff_reg3 = tk.Label(self.fr_subj, text="Regular 3 coefficient: ")
        self.lbl_coff_reg3.grid(row=4, column=0, padx=10, pady=10)
        self.ent_coff_reg3 = tk.Entry(self.fr_subj)
        self.ent_coff_reg3.grid(row=4, column=1, padx=10, pady=10)

        self.lbl_coff_mid = tk.Label(self.fr_subj, text="Midterm coefficient: ")
        self.lbl_coff_mid.grid(row=5, column=0, padx=10, pady=10)
        self.ent_coff_mid = tk.Entry(self.fr_subj)
        self.ent_coff_mid.grid(row=5, column=1, padx=10, pady=10)

        self.lbl_coff_fin = tk.Label(self.fr_subj, text="Final coefficient: ")
        self.lbl_coff_fin.grid(row=6, column=0, padx=10, pady=10)
        self.ent_coff_fin = tk.Entry(self.fr_subj)
        self.ent_coff_fin.grid(row=6, column=1, padx=10, pady=10)

        self.fr_btn_subj = tk.Frame(self.fr_subj)
        self.fr_btn_subj.grid(row=7, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_subj = tk.Button(self.fr_btn_subj, text="Add Subject")
        self.btn_add_subj.grid(row=0, column=0, padx=10, pady=10)
        self.btn_upd_subj = tk.Button(self.fr_btn_subj, text="Update Subject")
        self.btn_upd_subj.grid(row=0, column=1, padx=10, pady=10)


        # sectional class
        self.fr_sec_cls = tk.Frame(self.fr_mal)
        self.fr_sec_cls.grid(row=2, column=2, padx=10, pady=10, rowspan=2)

        self.lbl_sec_cls_id = tk.Label(self.fr_sec_cls, text="Sectional class ID: ")
        self.lbl_sec_cls_id.grid(row=0, column=0, padx=10, pady=10)
        self.ent_sec_cls_id = tk.Entry(self.fr_sec_cls)
        self.ent_sec_cls_id.grid(row=0, column=1, padx=10, pady=10)

        self.lbl_sec_cls_name = tk.Label(self.fr_sec_cls, text="Sectional class name: ")
        self.lbl_sec_cls_name.grid(row=1, column=0, padx=10, pady=10)
        self.ent_sec_cls_name = tk.Entry(self.fr_sec_cls)
        self.ent_sec_cls_name.grid(row=1, column=1, padx=10, pady=10)

        self.lbl_sec_cls_sem = tk.Label(self.fr_sec_cls, text="Sectional class Semester: ")
        self.lbl_sec_cls_sem.grid(row=2, column=0, padx=10, pady=10)
        self.sel_sec_cls_sem_var = tk.StringVar()
        self.sel_sec_cls_sem = ttk.Combobox(self.fr_sec_cls, textvariable=self.sel_sec_cls_sem_var, state='readonly', width=27)
        self.sel_sec_cls_sem.grid(row=2, column=1, padx=10, pady=10)

        self.lbl_sec_cls_subj = tk.Label(self.fr_sec_cls, text="Sectional class Subject: ")
        self.lbl_sec_cls_subj.grid(row=3, column=0, padx=10, pady=10)
        self.sel_sec_cls_subj_var = tk.StringVar()
        self.sel_sec_cls_subj = ttk.Combobox(self.fr_sec_cls, textvariable=self.sel_sec_cls_subj_var ,state='readonly', width=27)
        self.sel_sec_cls_subj.grid(row=3, column=1, padx=10, pady=10)

        self.lbl_sec_cls_maj = tk.Label(self.fr_sec_cls, text="Sectional class Major: ")
        self.lbl_sec_cls_maj.grid(row=4, column=0, padx=10, pady=10)
        self.sel_sec_cls_maj_var = tk.StringVar()
        self.sel_sec_cls_maj = ttk.Combobox(self.fr_sec_cls, textvariable=self.sel_sec_cls_maj_var ,state='readonly', width=27)
        self.sel_sec_cls_maj.grid(row=4, column=1, padx=10, pady=10)

        self.fr_btn_sec_cls = tk.Frame(self.fr_sec_cls)
        self.fr_btn_sec_cls.grid(row=5, column=0, padx=10, pady=10, columnspan=2)
        self.btn_add_sec_cls = tk.Button(self.fr_btn_sec_cls, text="Add Sectional class")
        self.btn_add_sec_cls.grid(row=0, column=0, padx=10, pady=10)
        self.btn_upd_sec_cls = tk.Button(self.fr_btn_sec_cls, text="Update Sectional class")
        self.btn_upd_sec_cls.grid(row=0, column=1, padx=10, pady=10)







if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    management = UniversityManagement(root)
    management.grid(column=0, row=0, sticky='nsew')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()
