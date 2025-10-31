USE student_management;

-- Insert data in order of dependency

-- 1. Tables with no foreign keys
INSERT INTO departments (name)
VALUES
('Công nghệ thông tin'),
('Kinh tế');

INSERT INTO subjects (id, name, coff)
VALUES
('PE6021','Bóng rổ', '1'),
('FL6085','Tiếng anh CNTT cơ bản 1','5'),
('BS6002','Giải tích','3'),
('LP6010','Triết học Mác-Lênin','3'),
('BM6091','Quản lý dự án','2');

INSERT INTO users (username, password, name, email)
VALUES
('admin', '$2b$12$5IY3/C7jMBrYDwiXt.hmvuBhaJ1tmurvt70Omvan1s8JJ/uQD7IUO', 'admin', 'admin@mail.com'),
('vinh01','$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW','Lưu Công Vinh', 'vinh01@gmail.com'),
('quan02','$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW','Nguyễn Anh Quân', 'vinh02@gmail.com');
# default password is 12112004

INSERT INTO semesters (year, term_order)
VALUES
(2022, '1'), -- ID 1 (Ref: HK1)
(2022, '2'), -- ID 2 (Ref: HK2)
(2023, '1'), -- ID 3 (Ref: HK3)
(2023, '2'); -- ID 4 (Ref: HK4)

-- 2. Tables that depend on the first group
INSERT INTO majors (name, department_id)
VALUES
('Công nghệ thông tin',1),     -- ID 1
('Kĩ thuật phần mềm',1),     -- ID 2
('Kinh tế quốc tế',2),      -- ID 3
('Kinh doanh quốc tế',2);  -- ID 4

INSERT INTO departmental_classes (id, name, major_id)
VALUES
('2022CNTT01','Lớp CNTT 2022-01',1),
('2022CNTT02','Lớp CNTT 2022-02',1),     -- Ref: Vinh's class (old id 2)
('2022KTPM01','Lớp KTPM 2022-01',2),
('2022KTPM02','Lớp KTPM 2022-02',2),
('2022KTQT01','Lớp KTQT 2022-01',3),     -- Ref: Quân's class (old id 5)
('2022KTQT02','Lớp KTQT 2022-02',3),
('2022KDQT01','Lớp KDQT 2022-01',4),
('2022KDQT02','Lớp KDQT 2022-02',4);     -- Ref: Lạc's class (old id 8)

-- 3. Sectional classes (linking subjects, semesters, and majors)
INSERT INTO sectional_classes (name, semester_id, subject_id, major_id)
VALUES
('BM6091_HK1_L1', 1, 'BM6091', 1), -- ID 1 (Vinh)
('BS6002_HK1_L1', 1, 'BS6002', 1), -- ID 2 (Vinh)
('FL6085_HK1_L1', 1, 'FL6085', 1), -- ID 3 (Vinh)
('LP6010_HK2_L1', 2, 'LP6010', 1), -- ID 4 (Vinh)
('BM6091_HK1_L2', 1, 'BM6091', 3), -- ID 5 (Quân)
('BS6002_HK1_L2', 1, 'BS6002', 3), -- ID 6 (Quân)
('FL6085_HK2_L1', 2, 'FL6085', 3), -- ID 7 (Quân)
('LP6010_HK2_L2', 2, 'LP6010', 3), -- ID 8 (Quân)
('LP6010_HK2_L3', 2, 'LP6010', 4), -- ID 9 (Lạc)
('BS6002_HK2_L1', 2, 'BS6002', 4), -- ID 10 (Lạc)
('FL6085_HK3_L1', 3, 'FL6085', 4), -- ID 11 (Lạc)
('LP6010_HK4_L1', 4, 'LP6010', 4); -- ID 12 (Lạc)

-- 4. Students (depends on majors)
-- Note: Mapped student_name -> fname, lname. Mapped gender -> BIT (1=Nam, 0=Nữ/Khác). Mapped generation -> INT.
INSERT INTO students (sid, fname, lname, dob, address, cid, phone, email, gender, generation, status,img, departmental_class_id)
VALUES
('2022602800','Lưu Công','Vinh','2004-11-12','Hà Nội','001204056492','0348341246','vinh01@gmail.com',1,17, '1', 'D:/hoc/images/Luu Cong Vinh.jpg','2022CNTT02'),
('2022602801','Nguyễn Anh','Quân','2004-04-25','Hà Nội','001204056493','0348341247','vinh02@gmail.com',0,17, '1','D:/hoc/images/Nguyen Anh Quan.jpg','2022KTQT01'),
('2022602802','Nguyễn Anh','Lạc','2000-04-25','Hà Nội','001204056494','0348341248','vinh03@gmail.com',0,15,'1','D:/hoc/images/Nguyen Anh Lac.jpg','2022KDQT02');

-- 5. Scores (depends on students and sectional_classes)
-- Note: Mapped score_regular -> regular1
INSERT INTO scores (sectional_class_id, student_id, regular1, regular2, regular3, midterm, final)
VALUES
(1, '2022602800', 8.5, NULL, NULL, 9, 10),    -- BM6091, Vinh
(2, '2022602800', 8, NULL, NULL, 9.5, 10),   -- BS6002, Vinh
(3, '2022602800', 9, NULL, NULL, 9.5, 10),   -- FL6085, Vinh
(4, '2022602800', 8.5, NULL, NULL, 9.5, 10),  -- LP6010, Vinh
(5, '2022602801', 8, NULL, NULL, 9.5, 10),    -- BM6091, Quân
(6, '2022602801', 8.5, NULL, NULL, 9.5, 4),   -- BS6002, Quân
(7, '2022602801', 9, NULL, NULL, 9, 5.5),  -- FL6085, Quân (CORRECTED: Removed 'Z' from student_id)
(8, '2022602801', 8, NULL, NULL, 9.5, 10),   -- LP6010, Quân
(9, '2022602802', 7, NULL, NULL, 9.5, 10),   -- LP6010, Lạc
(10, '2022602802', 8.5, NULL, NULL, 8, 8),   -- BS6002, Lạc
(11, '2022602802', 9, NULL, NULL, 9.5, 9),  -- FL6085, Lạc
(12, '2022602802', 8, NULL, NULL, 9, 7);   -- LP6010, Lạc