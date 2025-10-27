import tkinter as tk
import tkinter.ttk as ttk
from tkcalendar import DateEntry

class StudentManagement(tk.Frame):
    def __init__(self, parent):
        self.parent = parent
        super().__init__(parent)
        self.widgets()

    def widgets(self):
        self.info_frame = tk.Frame(self)
        self.info_frame.grid_propagate(False)
        self.list_frame = tk.Frame(self)

        # self.info_frame.config(width=100, height=100)
        # self.list_frame.config(width=100, height=100)

        self.info_frame.grid(row=0, column=0, padx=10, pady=10)
        self.list_frame.grid(row=0, column=1, padx=10, pady=10)


        # process student profile pic
        self.pro5_pic = tk.Canvas(self.info_frame, width=140, height=220)
        self.pro5_pic.grid(row=1, column=0, rowspan=6)

        self.btn_pro5_pic = tk.Button(self.info_frame, text='Select student profile picture')
        self.btn_pro5_pic.grid(row=2, column=0, padx=5, pady=5)



    # def widgets(self):
    #     # self.btn1 = tk.Button(self,text='hihi',bg='red')
    #     # self.btn1.grid(row=0,column=1)
    #     self.frame1 = tk.Frame(self, bg='#D5F0D4', borderwidth=1.5, relief='solid')
    #     self.frame1.grid(row=0, column=0, sticky='nsew')
    #     # Ngăn không cho frame1 mở rộng
    #     self.frame1.grid_propagate(False)
    #
    #     # self.btn = tk.Button(self.frame1,text='xx')
    #     # self.btn.grid(row=0,column=0)
    #     self.frame2 = tk.Frame(self, bg='#83CAFF', borderwidth=1.5, relief='solid')
    #     self.frame2.grid(row=0, column=2, sticky='nsew')
    #     # Ngăn không cho frame2 mở rộng
    #     self.frame2.grid_propagate(False)
    #     # self.btn2 = tk.Button(self.frame2,text='yy')
    #     # self.btn2.grid(row=0,column=0)
    #     self.grid_rowconfigure(0, weight=1)
    #     self.grid_columnconfigure(0, weight=45)
    #     self.grid_columnconfigure(1, weight=1)
    #     self.grid_columnconfigure(2, weight=54)
    #
    #
    #     # Widgets in frame1
    #     # Frame1_1
    #     self.frame1_1 = tk.Frame(self.frame1)
    #     self.frame1_1.grid(row=0, column=0, sticky='nsew')
    #     self.frame1_1.grid_propagate(False)
    #
    #     # Frame1_2
    #     self.frame1_2 = tk.Frame(self.frame1)
    #     self.frame1_2.grid(row=1, column=0, sticky='nsew')
    #     self.frame1_2.grid_propagate(False)
    #
    #     # Frame1_3
    #     self.frame1_3 = tk.Frame(self.frame1)
    #     self.frame1_3.grid(row=2, column=0, sticky='nsew')
    #     self.frame1_3.grid_propagate(False)
    #
    #     self.frame1.grid_columnconfigure(0, weight=1)
    #     self.frame1.grid_rowconfigure(0, weight=50)
    #     self.frame1.grid_rowconfigure(1, weight=40)
    #     self.frame1.grid_rowconfigure(2, weight=10)
    #
    #     # Widgets in frame1_1
    #     # Title
    #     self.title1_1 = tk.Label(self.frame1_1, text="Thông tin cá nhân")
    #     self.title1_1.grid(row=0, column=0, columnspan=5, pady=10, sticky='we')
    #     # Content
    #
    #     # Xử lý ảnh
    #     self.canvas = tk.Canvas(self.frame1_1, width=140, height=220)
    #     self.canvas.grid(row=1, column=0, rowspan=6)
    #
    #     self.btn_select_image = tk.Button(self.frame1_1, text='Chọn ảnh')
    #     self.btn_select_image.grid(row=7, column=0, padx=5, pady=5)
    #
    #     self.lbl_id = tk.Label(self.frame1_1, text='Mã sinh viên')
    #     self.lbl_id.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    #
    #     self.ent_id = tk.Entry(self.frame1_1)
    #     self.ent_id.grid(row=1, column=2, padx=5, pady=5)
    #
    #     self.lbl_name = tk.Label(self.frame1_1, text='Họ và tên')
    #     self.lbl_name.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    #
    #     self.ent_name = tk.Entry(self.frame1_1)
    #     self.ent_name.grid(row=2, column=2, padx=5, pady=5)
    #
    #     self.lbl_birth = tk.Label(self.frame1_1, text='Ngày sinh')
    #     self.lbl_birth.grid(row=3, column=1, padx=5, pady=5, sticky='w')
    #
    #     # Vấn đề
    #     self.date_birth = DateEntry(self.frame1_1, date_pattern="dd/mm/yyyy")
    #     self.date_birth.grid(row=3, column=2, padx=5, pady=5, sticky='w')
    #
    #     self.lbl_address = tk.Label(self.frame1_1, text='Địa chỉ')
    #     self.lbl_address.grid(row=4, column=1, padx=5, pady=5, sticky='w')
    #
    #     self.ent_address = tk.Entry(self.frame1_1)
    #     self.ent_address.grid(row=4, column=2, padx=5, pady=5)
    #
    #     self.lbl_cccd = tk.Label(self.frame1_1, text='CCCD')
    #     self.lbl_cccd.grid(row=5, column=1, padx=5, pady=5, sticky='w')
    #
    #     self.ent_cccd = tk.Entry(self.frame1_1)
    #     self.ent_cccd.grid(row=5, column=2, padx=5, pady=5)
    #
    #     self.lbl_phone = tk.Label(self.frame1_1, text='Số điện thoại')
    #     self.lbl_phone.grid(row=6, column=1, padx=5, pady=5, sticky='w')
    #
    #     self.ent_phone = tk.Entry(self.frame1_1)
    #     self.ent_phone.grid(row=6, column=2, padx=5, pady=5)
    #
    #     self.lbl_email = tk.Label(self.frame1_1, text='Email')
    #     self.lbl_email.grid(row=1, column=3, padx=5, pady=5, sticky='w')
    #
    #     self.ent_email = tk.Entry(self.frame1_1)
    #     self.ent_email.grid(row=1, column=4, padx=5, pady=5)
    #
    #     self.lbl_gender = tk.Label(self.frame1_1, text='Giới tính')
    #     self.lbl_gender.grid(row=2, column=3, padx=5, pady=5, sticky='w')
    #
    #     self.gender = tk.StringVar()  # Biến lưu giá trị được chọn
    #     self.combo_gender = ttk.Combobox(self.frame1_1, textvariable=self.gender, state='readonly')
    #     self.combo_gender['values'] = ['Nam', 'Nữ']
    #     self.combo_gender.current(0)
    #     self.combo_gender.grid(row=2, column=4, padx=5, pady=5, sticky='w')
    #
    #     self.frame1_1.grid_columnconfigure(0, weight=40)
    #     self.frame1_1.grid_columnconfigure(1, weight=15)
    #     self.frame1_1.grid_columnconfigure(2, weight=15)
    #     self.frame1_1.grid_columnconfigure(3, weight=15)
    #     self.frame1_1.grid_columnconfigure(4, weight=15)
    #
    #     # Widgets in frame1_2
    #     self.frame1_2.grid_columnconfigure(0, weight=25)
    #     self.frame1_2.grid_columnconfigure(1, weight=25)
    #     self.frame1_2.grid_columnconfigure(2, weight=25)
    #     self.frame1_2.grid_columnconfigure(3, weight=25)
    #
    #     self.title1_2 = tk.Label(self.frame1_2, text='Thông tin học tập')
    #     self.title1_2.grid(row=0, column=0, columnspan=4, padx=5, pady=5)
    #
    #     # Department
    #     self.lbl_department = tk.Label(self.frame1_2, text='Khoa')
    #     self.lbl_department.grid(row=1, column=0, padx=5, pady=5, sticky='w')
    #
    #     self.department = tk.StringVar()
    #     self.combo_department = ttk.Combobox(self.frame1_2, textvariable=self.department, state='readonly')
    #     self.combo_department.grid(row=1, column=1, padx=5, pady=5, sticky='w')
    #
    #     # Major
    #     self.lbl_major = tk.Label(self.frame1_2, text='Chuyên ngành')
    #     self.lbl_major.grid(row=2, column=0, padx=5, pady=5, sticky='w')
    #
    #     self.major = tk.StringVar()
    #     self.combo_major = ttk.Combobox(self.frame1_2, textvariable=self.major, state='readonly')
    #     self.combo_major.grid(row=2, column=1, padx=5, pady=5, sticky='w')
    #
    #     # Class
    #     self.lbl_class = tk.Label(self.frame1_2, text='Lớp')
    #     self.lbl_class.grid(row=1, column=2, padx=5, pady=5, sticky='w')
    #
    #     self.classs = tk.StringVar()
    #     self.combo_class = ttk.Combobox(self.frame1_2, textvariable=self.classs, state='readonly')
    #     self.combo_class.grid(row=1, column=3, padx=5, pady=5, sticky='w')
    #
    #     # Generation
    #     self.lbl_gen = tk.Label(self.frame1_2, text='Khóa')
    #     self.lbl_gen.grid(row=2, column=2, padx=5, pady=5, sticky='w')
    #
    #     self.gen = tk.StringVar()
    #     self.combo_gen = ttk.Combobox(self.frame1_2, textvariable=self.gen, state='readonly')
    #     self.combo_gen.grid(row=2, column=3, padx=5, pady=5, sticky='w')
    #     self.combo_gen['values'] = ['K14', 'K15', 'K16', 'K17', 'K18', 'K19']
    #     self.combo_gen.current(0)
    #
    #     # Widgets in frame1_3
    #     self.frame1_3.grid_columnconfigure(0, weight=25)
    #     self.frame1_3.grid_columnconfigure(1, weight=25)
    #     self.frame1_3.grid_columnconfigure(2, weight=25)
    #     self.frame1_3.grid_columnconfigure(3, weight=25)
    #
    #     self.student_btn_add = tk.Button(self.frame1_3, text='Thêm', width=15)
    #     self.student_btn_add.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    #
    #     self.student_btn_update = tk.Button(self.frame1_3, text='Sửa', width=15, state='disabled')
    #     self.student_btn_update.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
    #
    #     self.student_btn_delete = tk.Button(self.frame1_3, text='Xóa', width=15, state='disabled')
    #     self.student_btn_delete.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
    #
    #     self.student_btn_refresh = tk.Button(self.frame1_3, text='Làm mới', width=15)
    #     self.student_btn_refresh.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
    #
    #     self.student_btn_back = tk.Button(self.frame1_3, text='Quay lại', width=15)
    #     self.student_btn_back.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
    #
    #     # Widgets in frame2
    #     self.frame2_1 = tk.Frame(self.frame2)
    #     self.frame2_1.grid(row=0, column=0, sticky='nsew')
    #     self.frame2_1.grid_propagate(False)
    #
    #     self.frame2_2 = tk.Frame(self.frame2)
    #     self.frame2_2.grid(row=1, column=0, sticky='nsew')
    #     self.frame2_2.grid_propagate(False)
    #
    #     self.frame2.grid_columnconfigure(0, weight=1)
    #     self.frame2.grid_rowconfigure(0, weight=10)
    #     self.frame2.grid_rowconfigure(1, weight=90)
    #
    #     # Widgets in frame2_1
    #     self.lbl_find = tk.Label(self.frame2_1, text='Tìm kiếm theo')
    #     self.lbl_find.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
    #
    #     self.find = tk.StringVar()
    #     self.combo_find = ttk.Combobox(self.frame2_1, textvariable=self.find, state='readonly')
    #     self.combo_find['values'] = ['Mã sinh viên', 'Tên sinh viên', 'Chuyên ngành', 'Khóa', 'Lớp']
    #     self.combo_find.current(0)
    #     self.combo_find.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
    #
    #     self.ent_find = tk.Entry(self.frame2_1)
    #     self.ent_find.grid(row=0, column=2, padx=5, pady=5, sticky='nsew')
    #
    #     self.btn_find = tk.Button(self.frame2_1, text='Tìm kiếm')
    #     self.btn_find.grid(row=0, column=3, padx=5, pady=5, sticky='nsew')
    #
    #     self.btn_showall = tk.Button(self.frame2_1, text='Xem tất cả')
    #     self.btn_showall.grid(row=0, column=4, padx=5, pady=5, sticky='nsew')
    #
    #     self.btn_export = tk.Button(self.frame2_1, text='Xuất danh sách')
    #     self.btn_export.grid(row=0, column=5, padx=5, pady=5, sticky='nsew')
    #
    #     # self.frame2_1.grid_rowconfigure(0,weight=1)
    #     for i in range(6):
    #         self.frame2_1.grid_columnconfigure(i, weight=16)
    #
    #     # Widgets in frame2_2
    #     self.frame2_2.grid_columnconfigure(0, weight=1)
    #     self.frame2_2.grid_rowconfigure(0, weight=1)
    #
    #     columns = ('stt', 'student_id', 'name', 'gender', 'birth', 'generation', 'major', 'class', 'gpa')
    #     self.tree = ttk.Treeview(self.frame2_2, columns=columns, show='headings')
    #     self.tree.grid(row=0, column=0, sticky='nsew')
    #
    #     self.tree.heading('stt', text='STT')
    #     self.tree.heading('student_id', text='Mã sinh viên')
    #     self.tree.heading('name', text='Họ và tên')
    #     self.tree.heading('gender', text='Giới tính')
    #     self.tree.heading('birth', text='Ngày sinh')
    #     self.tree.heading('generation', text='Khóa')
    #     self.tree.heading('major', text='Chuyên ngành')
    #     self.tree.heading('class', text='Lớp')
    #     self.tree.heading('gpa', text='GPA')
    #
    #     # Điều chỉnh width các cột
    #     total_width = self.frame2_2.winfo_width()  # Lấy chiều rộng khung cha (frame2_2)
    #     num_cols = len(self.tree["columns"])  # Số lượng cột
    #     col_width = total_width // num_cols  # Chia đều cho các cột
    #
    #     for col in self.tree["columns"]:
    #         self.tree.column(col, width=col_width, stretch=True)
    #
    #     # self.tree.column('stt',width=20,stretch=True,anchor='center')
    #     # self.tree.column('student_id',width=80,stretch=True,anchor='center')
    #     # self.tree.column('name',width=100,stretch=True,anchor='w')
    #     # self.tree.column('gender',width=50,stretch=True,anchor='center')
    #     # self.tree.column('birth',width=60,stretch=True,anchor='center')
    #     # self.tree.column('generation',width=25,stretch=True,anchor='center')
    #     # self.tree.column('major',width=95,stretch=True,anchor='w')
    #     # self.tree.column('class',width=60,stretch=True,anchor='center')
    #
    #     # Thêm scroll bar
    #     self.scrollbar_x = ttk.Scrollbar(self.frame2_2, orient="horizontal", command=self.tree.xview)
    #     self.scrollbar_y = ttk.Scrollbar(self.frame2_2, orient="vertical", command=self.tree.yview)
    #
    #     self.tree.configure(xscrollcommand=self.scrollbar_x.set, yscrollcommand=self.scrollbar_y.set)
    #
    #     self.scrollbar_x.pack(side="bottom", fill="x")
    #     self.scrollbar_y.pack(side="right", fill="y")


root = tk.Tk()
management = StudentManagement(root)
management.pack()
root.mainloop()
