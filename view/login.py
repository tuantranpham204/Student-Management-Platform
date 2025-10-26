import tkinter as tk

class LoginView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.widgets()

    def widgets(self):

        self.lb_us = tk.Label(self, text='Username:', anchor='w')
        self.lb_us.grid(row=0, column=0, padx=10, pady=10, sticky='w')
        self.ent_us = tk.Entry(self, width=30)
        self.ent_us.grid(row=0, column=1, padx=10, pady=10)

        self.lb_pw = tk.Label(self, text='Password:', anchor='w')
        self.lb_pw.grid(row=1, column=0, padx=10, pady=10, sticky='w')
        self.ent_pw = tk.Entry(self, width=30, show='*')
        self.ent_pw.grid(row=1, column=1, padx=10, pady=10)

        self.show_pw = tk.IntVar(value=0)
        self.checkbtn_showpw = tk.Checkbutton(self, text='Show password', variable=self.show_pw)
        self.checkbtn_showpw.grid(row=2, column=1, pady=5, sticky='w')

        self.btn_login = tk.Button(self, text='Login', width=10, height=2)
        self.btn_login.grid(row=0, column=3, columnspan=1, pady=5)

        self.btn_to_register = tk.Button(self, text='To register', width=10, height=2)
        self.btn_to_register.grid(row=1, column=3, columnspan=1, pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

root = tk.Tk()
login = LoginView(root)
login.pack()
root.mainloop()