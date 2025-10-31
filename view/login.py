import tkinter as tk
from config.auth import verify_password
from tkinter import messagebox
import service.user as user_service
from util.util import default_vals


class LoginView(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.configure(width=800, height=500, bg=default_vals.DEFAULT_BG_COLOR)
        self.widgets()
        self.ent_us.insert(0, "admin")
        self.ent_pw.insert(0, "admin")


    def widgets(self):
        self.lb_us = tk.Label(self, text='Username:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_us.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ent_us = tk.Entry(self, width=30)
        self.ent_us.grid(row=0, column=1, padx=10, pady=10)

        self.lb_pw = tk.Label(self, text='Password:', anchor='w', bg=default_vals.DEFAULT_BG_COLOR)
        self.lb_pw.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_pw = tk.Entry(self, width=30, show='💀')
        self.ent_pw.grid(row=1, column=1, padx=10, pady=10)

        self.is_pw_shown = tk.IntVar(value=0)
        self.checkbtn_showpw = tk.Checkbutton(self, text='Show password', variable=self.is_pw_shown, command=self.show_pw, bg=default_vals.DEFAULT_BG_COLOR)
        self.checkbtn_showpw.grid(row=2, column=1, pady=5, sticky='w')

        self.btn_login = tk.Button(self, text='Login', width=10, height=2, command=self.verify_user)
        self.btn_login.grid(row=0, column=3, columnspan=1, pady=5)


        self.btn_to_register = tk.Button(self, text='To register', width=10, height=2, command=self.to_register)
        self.btn_to_register.grid(row=1, column=3, columnspan=1, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def show_pw(self):
        if not self.is_pw_shown.get():
            self.ent_pw.config(show='💀')
        else:
            self.ent_pw.config(show='')

    def verify_user(self):  # Added 'event' because you are using .bind()
        username = self.ent_us.get()
        password = self.ent_pw.get()

        if username.strip() == "" or password.strip() == "":
            messagebox.showerror('Error', 'Please enter both username and password')
            return
        user = user_service.get_user_by_username(username)
        if user:
            from view.user_dashboard import UserDashboard
            if verify_password(password, user.password):
                messagebox.showinfo('Success', 'You are now logged in')
                self.grid_forget()
                user_dashboard = UserDashboard(self.parent, user.name)
                user_dashboard.grid(column=0, row=0, padx=10, pady=10)
                return
            else:
                messagebox.showerror('Error', 'Incorrect password')
        else:
            messagebox.showerror('Error', 'User not found')
        return

    def to_register(self):
        from view.register import RegisterView
        self.grid_forget()
        self.register_view = RegisterView(self.parent)
        self.register_view.grid(row=0, column=0)


