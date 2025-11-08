from view.login import LoginView
import tkinter as tk
import os
from util.util import default_vals


class App:
   def __init__(self, root: tk.Tk):
      self.root = root
      self.root.title('Student Management')
      self.root.geometry("2000x1000")
      self.root.resizable(True, True)

      self.root.grid_rowconfigure(0, weight=1)
      self.root.grid_columnconfigure(0, weight=1)
      self.root.configure(bg=default_vals.DEFAULT_BG_COLOR)

      self.login_view = LoginView(self.root)
      self.login_view.grid(row=0, column=0)



if __name__ == '__main__':
   root = tk.Tk()
   app = App(root)
   root.mainloop()