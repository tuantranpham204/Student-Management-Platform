import tkinter as tk
from tkinter import ttk, messagebox
import util.util as util
from util.global_exception_handler import handle_exceptions
from types import SimpleNamespace as sn
import json

# Import Services
import service.department as dep_service
import service.major as maj_service
import service.departmental_class as dep_cls_service
import service.semester as sem_service
import service.subject as subj_service
import service.sectional_class as sec_cls_service


class UniversityManagement(tk.Frame):
    def __init__(self, parent, back_callback=None):
        super().__init__(parent)
        self.parent = parent
        self.back_callback = back_callback
        # Check if default_vals exists in util, else fallback
        bg_color = util.default_vals.DEFAULT_BG_COLOR if hasattr(util, 'default_vals') else 'white'
        self.config(bg=bg_color)

        # State
        self.current_entity = 'department'
        self.id_maps = {}

        self.widgets()
        self.setup_treeview()
        self.populate_comboboxes()
        self.load_data('department')

    def widgets(self):
        # Layout Frames
        self.fr_lst = tk.Frame(self)
        self.fr_lst.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.fr_mal = tk.Frame(self)
        self.fr_mal.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # ==================== INPUT FORMS ====================

        # --- 1. Department ---
        self.fr_dep = tk.LabelFrame(self.fr_mal, text="Departments")
        self.fr_dep.grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        tk.Label(self.fr_dep, text='ID:').grid(row=0, column=0, padx=5, pady=2)
        self.ent_dep_id = tk.Entry(self.fr_dep)
        self.ent_dep_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_dep, text="Name:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_dep_name = tk.Entry(self.fr_dep)
        self.ent_dep_name.grid(row=1, column=1, padx=5, pady=2)

        self.create_crud_buttons(self.fr_dep, 'department')

        # --- 2. Major ---
        self.fr_maj = tk.LabelFrame(self.fr_mal, text="Majors")
        self.fr_maj.grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        tk.Label(self.fr_maj, text='ID:').grid(row=0, column=0, padx=5, pady=2)
        self.ent_maj_id = tk.Entry(self.fr_maj)
        self.ent_maj_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_maj, text="Name:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_maj_name = tk.Entry(self.fr_maj)
        self.ent_maj_name.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.fr_maj, text="Dept:").grid(row=2, column=0, padx=5, pady=2)
        self.sel_maj_dep = ttk.Combobox(self.fr_maj, state='readonly')
        self.sel_maj_dep.grid(row=2, column=1, padx=5, pady=2)

        self.create_crud_buttons(self.fr_maj, 'major')

        # --- 3. Departmental Class ---
        self.fr_dep_cls = tk.LabelFrame(self.fr_mal, text="Classes")
        self.fr_dep_cls.grid(row=2, column=0, padx=5, pady=5, sticky='ew')

        tk.Label(self.fr_dep_cls, text="ID:").grid(row=0, column=0, padx=5, pady=2)
        self.ent_dep_cls_id = tk.Entry(self.fr_dep_cls)
        self.ent_dep_cls_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_dep_cls, text="Name:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_dep_cls_name = tk.Entry(self.fr_dep_cls)
        self.ent_dep_cls_name.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.fr_dep_cls, text="Major:").grid(row=2, column=0, padx=5, pady=2)
        self.sel_dep_cls_maj = ttk.Combobox(self.fr_dep_cls, state='readonly')
        self.sel_dep_cls_maj.grid(row=2, column=1, padx=5, pady=2)

        self.create_crud_buttons(self.fr_dep_cls, 'departmental_class')

        # --- 4. Semester ---
        self.fr_sem = tk.LabelFrame(self.fr_mal, text="Semesters")
        self.fr_sem.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        tk.Label(self.fr_sem, text="ID:").grid(row=0, column=0, padx=5, pady=2)
        self.ent_sem_id = tk.Entry(self.fr_sem)
        self.ent_sem_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_sem, text="Year:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_sem_year = tk.Entry(self.fr_sem)
        self.ent_sem_year.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.fr_sem, text="Term:").grid(row=2, column=0, padx=5, pady=2)
        self.sel_sem_term = ttk.Combobox(self.fr_sem, values=['1', '2', '3', '4'], state='readonly')
        self.sel_sem_term.grid(row=2, column=1, padx=5, pady=2)

        self.create_crud_buttons(self.fr_sem, 'semester')

        # --- 5. Subject (Right Column) ---
        self.fr_subj = tk.LabelFrame(self.fr_mal, text="Subjects")
        self.fr_subj.grid(row=0, column=1, padx=5, pady=5, rowspan=2, sticky='nsew')

        tk.Label(self.fr_subj, text="ID:").grid(row=0, column=0, padx=5, pady=2)
        self.ent_subj_id = tk.Entry(self.fr_subj)
        self.ent_subj_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_subj, text="Name:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_subj_name = tk.Entry(self.fr_subj)
        self.ent_subj_name.grid(row=1, column=1, padx=5, pady=2)

        # Coefficients Fields
        tk.Label(self.fr_subj, text="Weight Distribution (Sum=1.0):", fg="blue").grid(row=2, column=0, columnspan=2,
                                                                                      pady=(10, 5))

        self.fr_coffs = tk.Frame(self.fr_subj)
        self.fr_coffs.grid(row=3, column=0, columnspan=2, padx=5)

        tk.Label(self.fr_coffs, text="Regular 1:").grid(row=0, column=0)
        self.ent_coff_reg1 = tk.Entry(self.fr_coffs, width=5)
        self.ent_coff_reg1.grid(row=0, column=1, padx=2)

        tk.Label(self.fr_coffs, text="Regular 2:").grid(row=0, column=2)
        self.ent_coff_reg2 = tk.Entry(self.fr_coffs, width=5)
        self.ent_coff_reg2.grid(row=0, column=3, padx=2)

        tk.Label(self.fr_coffs, text="Regular 3:").grid(row=0, column=4)
        self.ent_coff_reg3 = tk.Entry(self.fr_coffs, width=5)
        self.ent_coff_reg3.grid(row=0, column=5, padx=2)

        tk.Label(self.fr_coffs, text="Midterm:").grid(row=1, column=0, pady=5)
        self.ent_coff_mid = tk.Entry(self.fr_coffs, width=5)
        self.ent_coff_mid.grid(row=1, column=1, padx=2, pady=5)

        tk.Label(self.fr_coffs, text="Final:").grid(row=1, column=2, pady=5)
        self.ent_coff_fin = tk.Entry(self.fr_coffs, width=5)
        self.ent_coff_fin.grid(row=1, column=3, padx=2, pady=5)

        self.create_crud_buttons(self.fr_subj, 'subject', row_start=4)

        # --- 6. Sectional Class (Right Column) ---
        self.fr_sec_cls = tk.LabelFrame(self.fr_mal, text="Sectional Classes")
        self.fr_sec_cls.grid(row=2, column=1, padx=5, pady=5, rowspan=2, sticky='nsew')

        tk.Label(self.fr_sec_cls, text="ID:").grid(row=0, column=0, padx=5, pady=2)
        self.ent_sec_cls_id = tk.Entry(self.fr_sec_cls)
        self.ent_sec_cls_id.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.fr_sec_cls, text="Name:").grid(row=1, column=0, padx=5, pady=2)
        self.ent_sec_cls_name = tk.Entry(self.fr_sec_cls)
        self.ent_sec_cls_name.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(self.fr_sec_cls, text="Semester:").grid(row=2, column=0, padx=5, pady=2)
        self.sel_sec_cls_sem = ttk.Combobox(self.fr_sec_cls, state='readonly', width=17)
        self.sel_sec_cls_sem.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.fr_sec_cls, text="Subject:").grid(row=3, column=0, padx=5, pady=2)
        self.sel_sec_cls_subj = ttk.Combobox(self.fr_sec_cls, state='readonly', width=17)
        self.sel_sec_cls_subj.grid(row=3, column=1, padx=5, pady=2)

        tk.Label(self.fr_sec_cls, text="Major:").grid(row=4, column=0, padx=5, pady=2)
        self.sel_sec_cls_maj = ttk.Combobox(self.fr_sec_cls, state='readonly', width=17)
        self.sel_sec_cls_maj.grid(row=4, column=1, padx=5, pady=2)

        self.create_crud_buttons(self.fr_sec_cls, 'sectional_class', row_start=5)

        # --- GLOBAL CONTROLS ---
        self.fr_global = tk.Frame(self.fr_mal)
        self.fr_global.grid(row=4, column=0, columnspan=2, pady=10, sticky='new')

        tk.Button(self.fr_global, text="⬅ EXIT / BACK TO DASHBOARD", bg="#E74C3C", fg="white",
                  font=("Arial", 10, "bold"), command=self.go_back).pack(fill='x', padx=50)

    def create_crud_buttons(self, parent, entity_type, row_start=3):
        btn_fr = tk.Frame(parent)
        btn_fr.grid(row=row_start, column=0, columnspan=2, pady=5)

        tk.Button(btn_fr, text="Add", width=8, bg="#D5F5E3",
                  command=lambda: self.handle_action('add', entity_type)).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(btn_fr, text="Update", width=8, bg="#FCF3CF",
                  command=lambda: self.handle_action('update', entity_type)).grid(row=0, column=1, padx=2, pady=2)
        tk.Button(btn_fr, text="Delete", width=8, bg="#FADBD8",
                  command=lambda: self.handle_action('delete', entity_type)).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(btn_fr, text="Search", width=8, bg="#D6EAF8",
                  command=lambda: self.handle_action('search', entity_type)).grid(row=1, column=1, padx=2, pady=2)
    def setup_treeview(self):
        self.tree = ttk.Treeview(self.fr_lst, show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')

        ysb = ttk.Scrollbar(self.fr_lst, orient='vertical', command=self.tree.yview)
        ysb.grid(row=0, column=1, sticky='ns')
        xsb = ttk.Scrollbar(self.fr_lst, orient='horizontal', command=self.tree.xview)
        xsb.grid(row=1, column=0, sticky='ew')

        self.tree.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)

        self.fr_lst.grid_rowconfigure(0, weight=1)
        self.fr_lst.grid_columnconfigure(0, weight=1)

        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)

    def go_back(self):
        if self.back_callback:
            self.back_callback()
        else:
            self.parent.quit()

    @handle_exceptions()
    def populate_comboboxes(self):
        self.id_maps = {
            'department': {}, 'major': {}, 'semester': {}, 'subject': {}
        }

        deps = dep_service.get_all_departments()
        self.id_maps['department'] = {d.name: d.id for d in deps}
        self.sel_maj_dep['values'] = list(self.id_maps['department'].keys())

        majs = maj_service.get_all_majors()
        self.id_maps['major'] = {m.name: m.id for m in majs}
        self.sel_dep_cls_maj['values'] = list(self.id_maps['major'].keys())
        self.sel_sec_cls_maj['values'] = list(self.id_maps['major'].keys())

        sems = sem_service.get_all_semesters()
        self.id_maps['semester'] = {f"{s.year} - Term {s.term_order}": s.id for s in sems}
        self.sel_sec_cls_sem['values'] = list(self.id_maps['semester'].keys())

        subs = subj_service.get_all_subjects()
        self.id_maps['subject'] = {s.name: s.id for s in subs}
        self.sel_sec_cls_subj['values'] = list(self.id_maps['subject'].keys())

    def get_service_module(self, entity_type):
        if entity_type == 'department': return dep_service
        if entity_type == 'major': return maj_service
        if entity_type == 'departmental_class': return dep_cls_service
        if entity_type == 'semester': return sem_service
        if entity_type == 'subject': return subj_service
        if entity_type == 'sectional_class': return sec_cls_service
        return None

    def load_data(self, entity_type):
        self.current_entity = entity_type
        self.clear_entries(entity_type)
        self.populate_comboboxes()

        cols = getattr(util.attrs, entity_type)
        headers = getattr(util.headings, entity_type)

        self.tree['columns'] = cols
        for col, head in zip(cols, headers):
            self.tree.heading(col, text=head)
            if col == 'name':
                self.tree.column(col, width=250, anchor='w')
            else:
                self.tree.column(col, width=100, anchor='w')

        service = self.get_service_module(entity_type)
        if hasattr(service, f'get_all_{entity_type}s'):
            data = getattr(service, f'get_all_{entity_type}s')()
        elif hasattr(service, 'get_all_classes'):
            data = service.get_all_classes()
        else:
            data = []

        self.tree.delete(*self.tree.get_children())

        for item in data:
            if entity_type == 'subject':
                # Special handling for Subject to split coefficients
                try:
                    # item.coff is a JSON string. Parse it.
                    if hasattr(item, 'coff') and item.coff:
                        c = json.loads(item.coff)
                        # Inject these values into the item object so generic loop works
                        # attributes in utils are: id, name, reg1, reg2, reg3, mid, fin
                        item.reg1 = c.get('reg1', 0.0)
                        item.reg2 = c.get('reg2', 0.0)
                        item.reg3 = c.get('reg3', 0.0)
                        item.mid = c.get('mid', 0.0)
                        item.fin = c.get('fin', 0.0)
                    else:
                        for f in ['reg1', 'reg2', 'reg3', 'mid', 'fin']: setattr(item, f, 0.0)
                except Exception:
                    for f in ['reg1', 'reg2', 'reg3', 'mid', 'fin']: setattr(item, f, 0.0)

            # Construct values based on attrs definition
            values = [getattr(item, col, '') for col in cols]
            self.tree.insert('', 'end', values=tuple(values))

    def get_entry_data(self, entity_type):
        data = {}
        try:
            if entity_type == 'department':
                data['id'] = self.ent_dep_id.get() or None
                data['name'] = self.ent_dep_name.get()

            elif entity_type == 'major':
                data['id'] = self.ent_maj_id.get() or None
                data['name'] = self.ent_maj_name.get()
                dep_name = self.sel_maj_dep.get()
                data['department_id'] = self.id_maps['department'].get(dep_name)

            elif entity_type == 'departmental_class':
                data['id'] = self.ent_dep_cls_id.get()
                data['name'] = self.ent_dep_cls_name.get()
                maj_name = self.sel_dep_cls_maj.get()
                data['major_id'] = self.id_maps['major'].get(maj_name)

            elif entity_type == 'semester':
                data['id'] = self.ent_sem_id.get() or None
                data['year'] = self.ent_sem_year.get()
                data['term_order'] = self.sel_sem_term.get()

            elif entity_type == 'subject':
                data['id'] = self.ent_subj_id.get()
                data['name'] = self.ent_subj_name.get()
                # Gather coefficients
                try:
                    data['reg1'] = float(self.ent_coff_reg1.get() or 0)
                    data['reg2'] = float(self.ent_coff_reg2.get() or 0)
                    data['reg3'] = float(self.ent_coff_reg3.get() or 0)
                    data['mid'] = float(self.ent_coff_mid.get() or 0)
                    data['fin'] = float(self.ent_coff_fin.get() or 0)
                except ValueError:
                    messagebox.showerror("Error", "Coefficients must be numbers.")
                    return None

            elif entity_type == 'sectional_class':
                data['id'] = self.ent_sec_cls_id.get() or None
                data['name'] = self.ent_sec_cls_name.get()
                sem_name = self.sel_sec_cls_sem.get()
                data['semester_id'] = self.id_maps['semester'].get(sem_name)
                sub_name = self.sel_sec_cls_subj.get()
                data['subject_id'] = self.id_maps['subject'].get(sub_name)
                maj_name = self.sel_sec_cls_maj.get()
                data['major_id'] = self.id_maps['major'].get(maj_name)

        except Exception as e:
            print(f"Error getting data: {e}")
        return data

    @handle_exceptions()
    def handle_action(self, action, entity_type):
        service = self.get_service_module(entity_type)
        data = self.get_entry_data(entity_type)
        if data is None: return

        # --- SEARCH ---
        if action == 'search':
            if hasattr(service, f'get_{entity_type}s_by_params'):
                func = getattr(service, f'get_{entity_type}s_by_params')
            elif hasattr(service, 'get_classes_by_params'):
                func = service.get_classes_by_params
            elif hasattr(service, 'get_sectional_classes_by_params'):
                func = service.get_sectional_classes_by_params
            else:
                return

            clean_data = {k: v for k, v in data.items() if v}
            if entity_type == 'subject':
                # Remove coefficient keys for search
                for k in ['reg1', 'reg2', 'reg3', 'mid', 'fin']:
                    if k in clean_data: del clean_data[k]

            results = func(clean_data)

            self.current_entity = entity_type
            self.tree.delete(*self.tree.get_children())

            # Repopulate using load logic helper
            cols = getattr(util.attrs, entity_type)
            self.tree['columns'] = cols

            for item in results:
                if entity_type == 'subject':
                    try:
                        if hasattr(item, 'coff') and item.coff:
                            c = json.loads(item.coff)
                            item.reg1 = c.get('reg1', 0.0)
                            item.reg2 = c.get('reg2', 0.0)
                            item.reg3 = c.get('reg3', 0.0)
                            item.mid = c.get('mid', 0.0)
                            item.fin = c.get('fin', 0.0)
                        else:
                            for f in ['reg1', 'reg2', 'reg3', 'mid', 'fin']: setattr(item, f, 0.0)
                    except:
                        for f in ['reg1', 'reg2', 'reg3', 'mid', 'fin']: setattr(item, f, 0.0)

                values = [getattr(item, col, '') for col in cols]
                self.tree.insert('', 'end', values=tuple(values))
            return

        # --- DELETE ---
        if action == 'delete':
            pk = data.get('id')
            if not pk:
                messagebox.showerror("Error", "ID is required for deletion.")
                return
            if messagebox.askyesno("Confirm", f"Delete {entity_type} {pk}?"):
                if hasattr(service, f'delete_{entity_type}'):
                    getattr(service, f'delete_{entity_type}')(pk)
                elif hasattr(service, 'delete_class'):
                    service.delete_class(pk)
                messagebox.showinfo("Success", "Deleted successfully.")
                self.load_data(entity_type)
            return

        # --- ADD / UPDATE ---
        if action == 'add':
            if 'id' in data and not data['id']: del data['id']

            if hasattr(service, f'add_{entity_type}'):
                getattr(service, f'add_{entity_type}')(**data)
            elif hasattr(service, 'add_class'):
                service.add_class(**data)
            messagebox.showinfo("Success", "Added successfully.")

        elif action == 'update':
            if not data.get('id'):
                messagebox.showerror("Error", "ID required for update.")
                return

            if hasattr(service, f'update_{entity_type}'):
                getattr(service, f'update_{entity_type}')(data)
            elif hasattr(service, 'update_class'):
                service.update_class(data)
            messagebox.showinfo("Success", "Updated successfully.")

        self.load_data(entity_type)

    def clear_entries(self, entity_type):
        if entity_type == 'department':
            self.ent_dep_id.delete(0, tk.END)
            self.ent_dep_name.delete(0, tk.END)
        elif entity_type == 'major':
            self.ent_maj_id.delete(0, tk.END)
            self.ent_maj_name.delete(0, tk.END)
            self.sel_maj_dep.set('')
        elif entity_type == 'departmental_class':
            self.ent_dep_cls_id.delete(0, tk.END)
            self.ent_dep_cls_name.delete(0, tk.END)
            self.sel_dep_cls_maj.set('')
        elif entity_type == 'semester':
            self.ent_sem_id.delete(0, tk.END)
            self.ent_sem_year.delete(0, tk.END)
            self.sel_sem_term.set('')
        elif entity_type == 'subject':
            self.ent_subj_id.delete(0, tk.END)
            self.ent_subj_name.delete(0, tk.END)
            for ent in [self.ent_coff_reg1, self.ent_coff_reg2, self.ent_coff_reg3, self.ent_coff_mid,
                        self.ent_coff_fin]:
                ent.delete(0, tk.END)
                ent.insert(0, "0")
        elif entity_type == 'sectional_class':
            self.ent_sec_cls_id.delete(0, tk.END)
            self.ent_sec_cls_name.delete(0, tk.END)
            self.sel_sec_cls_sem.set('')
            self.sel_sec_cls_subj.set('')
            self.sel_sec_cls_maj.set('')

    def on_tree_select(self, event):
        sel = self.tree.selection()
        if not sel: return

        vals = self.tree.item(sel[0], 'values')
        if not vals: return

        if self.current_entity == 'department':
            self.ent_dep_id.delete(0, tk.END);
            self.ent_dep_id.insert(0, vals[0])
            self.ent_dep_name.delete(0, tk.END);
            self.ent_dep_name.insert(0, vals[1])

        elif self.current_entity == 'major':
            self.ent_maj_id.delete(0, tk.END);
            self.ent_maj_id.insert(0, vals[0])
            self.ent_maj_name.delete(0, tk.END);
            self.ent_maj_name.insert(0, vals[1])
            dep_id = int(vals[2])
            for name, did in self.id_maps['department'].items():
                if did == dep_id: self.sel_maj_dep.set(name); break

        elif self.current_entity == 'departmental_class':
            self.ent_dep_cls_id.delete(0, tk.END);
            self.ent_dep_cls_id.insert(0, vals[0])
            self.ent_dep_cls_name.delete(0, tk.END);
            self.ent_dep_cls_name.insert(0, vals[1])
            maj_id = int(vals[2])
            for name, mid in self.id_maps['major'].items():
                if mid == maj_id: self.sel_dep_cls_maj.set(name); break

        elif self.current_entity == 'semester':
            self.ent_sem_id.delete(0, tk.END);
            self.ent_sem_id.insert(0, vals[0])
            self.ent_sem_year.delete(0, tk.END);
            self.ent_sem_year.insert(0, vals[1])
            self.sel_sem_term.set(vals[2])

        elif self.current_entity == 'subject':
            # Vals are now split: ID, Name, Reg1, Reg2, Reg3, Mid, Fin
            self.ent_subj_id.delete(0, tk.END);
            self.ent_subj_id.insert(0, vals[0])
            self.ent_subj_name.delete(0, tk.END);
            self.ent_subj_name.insert(0, vals[1])

            # Map vals indices to coefficient fields
            # Indices in vals: 2->Reg1, 3->Reg2, 4->Reg3, 5->Mid, 6->Fin
            coeffs_vals = vals[2:7]
            entries = [self.ent_coff_reg1, self.ent_coff_reg2, self.ent_coff_reg3, self.ent_coff_mid, self.ent_coff_fin]

            for ent, val in zip(entries, coeffs_vals):
                ent.delete(0, tk.END)
                ent.insert(0, val)

        elif self.current_entity == 'sectional_class':
            self.ent_sec_cls_id.delete(0, tk.END);
            self.ent_sec_cls_id.insert(0, vals[0])
            self.ent_sec_cls_name.delete(0, tk.END);
            self.ent_sec_cls_name.insert(0, vals[1])

            sem_id, sub_id, maj_id = int(vals[2]), vals[3], int(vals[4])

            for name, sid in self.id_maps['semester'].items():
                if sid == sem_id: self.sel_sec_cls_sem.set(name); break
            for name, suid in self.id_maps['subject'].items():
                if suid == sub_id: self.sel_sec_cls_subj.set(name); break
            for name, mid in self.id_maps['major'].items():
                if mid == maj_id: self.sel_sec_cls_maj.set(name); break


if __name__ == "__main__":
    root = tk.Tk()
    root.resizable(True, True)
    management = UniversityManagement(root)
    management.grid(column=0, row=0, sticky='nsew')
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.mainloop()