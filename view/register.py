import tkinter as tk
from tkinter import messagebox
from service.user import add_user
from util.util import default_vals

class RegisterView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(width=800, height=500, bg=default_vals.DEFAULT_BG_COLOR)
        self.widgets()


    def widgets(self):
        self.lb_us = tk.Label(self, text='Username:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_us.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ent_us = tk.Entry(self, width=30)
        self.ent_us.grid(row=0, column=1, padx=10, pady=10)

        self.lb_fn = tk.Label(self, text='Full name:',anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_fn.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_fn = tk.Entry(self, width=30)
        self.ent_fn.grid(row=1, column=1, padx=10, pady=10)

        self.lb_e = tk.Label(self, text='Email:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_e.grid(row=2, column=0, padx=10, pady=10, sticky='w')
        self.ent_e = tk.Entry(self, width=30)
        self.ent_e.grid(row=2, column=1, padx=10, pady=10)

        self.lb_pw = tk.Label(self, text='Password:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_pw.grid(row=3, column=0, padx=10, pady=10, sticky='w')
        self.ent_pw = tk.Entry(self, width=30, show='💀')
        self.ent_pw.grid(row=3, column=1, padx=10, pady=10)

        self.lb_cfpw = tk.Label(self, text='Confirm password:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_cfpw.grid(row=4, column=0, padx=10, pady=10, sticky='w')
        self.ent_cfpw = tk.Entry(self, width=30)
        self.ent_cfpw.grid(row=4, column=1, padx=10, pady=10)

        self.btn_register = tk.Button(self, text='Register', width=10, height=2, command=self.register)
        self.btn_register.grid(row=0, column=2, rowspan=2, pady=10)

        self.btn_to_login = tk.Button(self, text='To Login', width=10, height=2, command=self.to_login)
        self.btn_to_login.grid(row=2, column=2, rowspan=2, pady=10)

    def to_login(self):
        from view.login import LoginView
        self.grid_forget()
        self.login_view = LoginView(self.parent)
        self.login_view.grid(row=0, column=0)

    def register(self):
        username = self.ent_us.get()
        fullname = self.ent_fn.get()
        email = self.ent_e.get()
        password = self.ent_pw.get()
        confirm_password = self.ent_cfpw.get()
        if username.strip() == "" or fullname.strip() == "" or email.strip() == "" or password.strip() == "":
            messagebox.showerror("Error", "Please fill all fields")
        if password != confirm_password:
            messagebox.showwarning('Passwords do not match', 'Passwords do not match')
            return
        add_user(username, email, password, fullname)
        messagebox.showinfo('Registered', f'User {fullname} registered successfully :>')
        from view.login import LoginView
        self.grid_forget()
        self.login_view = LoginView(self.parent)
        self.login_view.grid(row=0, column=0)
        return


