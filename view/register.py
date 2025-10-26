import tkinter as tk

class RegisterView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):
        self.lb_us = tk.Label(self, text='Username:')
        self.lb_us.grid(row=0, column=0, padx=10, pady=10, sticky='e')
        self.ent_us = tk.Entry(self, width=30)
        self.ent_us.grid(row=0, column=1, padx=10, pady=10)

        self.lb_e = tk.Label(self, text='Full name:')
        self.lb_e.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.ent_e = tk.Entry(self, width=30)
        self.ent_e.grid(row=1, column=1, padx=10, pady=10)

        self.lb_e = tk.Label(self, text='Email:')
        self.lb_e.grid(row=2, column=0, padx=10, pady=10, sticky='e')
        self.ent_e = tk.Entry(self, width=30)
        self.ent_e.grid(row=2, column=1, padx=10, pady=10)

        self.lb_pw = tk.Label(self, text='Password:')
        self.lb_pw.grid(row=3, column=0, padx=10, pady=10, sticky='e')
        self.ent_pw = tk.Entry(self, width=30)
        self.ent_pw.grid(row=3, column=1, padx=10, pady=10)

        self.lb_cfpw = tk.Label(self, text='Confirm password:')
        self.lb_cfpw.grid(row=4, column=0, padx=10, pady=10, sticky='e')
        self.ent_cfpw = tk.Entry(self, width=30)
        self.ent_cfpw.grid(row=4, column=1, padx=10, pady=10)

        self.btn_register = tk.Button(self, text='Register', width=10, height=2)
        self.btn_register.grid(row=0, column=2, columnspan=2, pady=10)

        self.btn_register = tk.Button(self, text='To Login', width=10, height=2)
        self.btn_register.grid(row=1, column=2, columnspan=2, pady=10)


root = tk.Tk()
login = RegisterView(root)
login.pack()
root.mainloop()