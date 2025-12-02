USE student_management;
-- Clear existing data (in reverse order of dependencies)
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE scores;
TRUNCATE TABLE students;
TRUNCATE TABLE sectional_classes;
TRUNCATE TABLE departmental_classes;
TRUNCATE TABLE majors;
TRUNCATE TABLE semesters;
TRUNCATE TABLE users;
TRUNCATE TABLE subjects;
TRUNCATE TABLE departments;
SET FOREIGN_KEY_CHECKS = 1;

-- 1. DEPARTMENTS (Khoa) - 5 khoa

INSERT INTO departments (name) VALUES
('Công nghệ thông tin'),        -- ID 1
('Kinh tế'),                     -- ID 2
('Kỹ thuật'),                    -- ID 3
('Ngoại ngữ'),                   -- ID 4
('Khoa học tự nhiên');           -- ID 5

-- 2. SUBJECTS (Môn học) - 30 môn với các hệ số khác nhau
-- CONFIG: JSON {"reg1": 0.x, "reg2": 0.x, "reg3": 0.x, "mid": 0.x, "fin": 0.x}
-- ============================================================
INSERT INTO subjects (id, name, coff) VALUES
-- Hệ số 1 (Thể chất - 50% Process, 50% Final)
('PE6021', 'Bóng rổ', '{"reg1":0.2,"reg2":0.2,"reg3":0.1,"mid":0.0,"fin":0.5}'),
('PE6022', 'Bóng đá', '{"reg1":0.2,"reg2":0.2,"reg3":0.1,"mid":0.0,"fin":0.5}'),
('PE6023', 'Cầu lông', '{"reg1":0.2,"reg2":0.2,"reg3":0.1,"mid":0.0,"fin":0.5}'),
('PE6024', 'Bơi lội', '{"reg1":0.2,"reg2":0.2,"reg3":0.1,"mid":0.0,"fin":0.5}'),
('PE6025', 'Võ thuật', '{"reg1":0.2,"reg2":0.2,"reg3":0.1,"mid":0.0,"fin":0.5}'),
-- Hệ số 2 (Cơ sở ngành - 10%x3 Process, 20% Mid, 50% Final)
('BM6091', 'Quản lý dự án', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('BM6092', 'Phân tích kinh doanh', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('BM6093', 'Marketing căn bản', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('BM6094', 'Quản trị nhân sự', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('IT6001', 'Nhập môn lập trình', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('IT6002', 'Cấu trúc dữ liệu', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('IT6003', 'Hệ điều hành', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('IT6004', 'Mạng máy tính', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
-- Hệ số 3 (Đại cương - 20% Process, 30% Mid, 50% Final)
('BS6001', 'Đại số tuyến tính', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('BS6002', 'Giải tích', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('BS6003', 'Xác suất thống kê', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('LP6010', 'Triết học Mác-Lênin', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('LP6011', 'Kinh tế chính trị', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('LP6012', 'Chủ nghĩa xã hội khoa học', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('PH6001', 'Vật lý đại cương', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('CH6001', 'Hóa học đại cương', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('BI6001', 'Sinh học đại cương', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
('EN6001', 'Môi trường và phát triển bền vững', '{"reg1":0.1,"reg2":0.1,"reg3":0.0,"mid":0.3,"fin":0.5}'),
-- Hệ số 4 (Chuyên ngành - 20%x2 Process, 0% Mid, 60% Final Project)
('IT6010', 'Trí tuệ nhân tạo', '{"reg1":0.2,"reg2":0.2,"reg3":0.0,"mid":0.0,"fin":0.6}'),
('IT6011', 'Học máy', '{"reg1":0.2,"reg2":0.2,"reg3":0.0,"mid":0.0,"fin":0.6}'),
('IT6012', 'Xử lý ngôn ngữ tự nhiên', '{"reg1":0.2,"reg2":0.2,"reg3":0.0,"mid":0.0,"fin":0.6}'),
('IT6013', 'Thị giác máy tính', '{"reg1":0.2,"reg2":0.2,"reg3":0.0,"mid":0.0,"fin":0.6}'),
-- Hệ số 5 (Ngoại ngữ - 10%x3 Process, 20% Mid, 50% Final)
('FL6085', 'Tiếng Anh CNTT cơ bản 1', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('FL6086', 'Tiếng Anh CNTT cơ bản 2', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}'),
('FL6087', 'Tiếng Anh chuyên ngành', '{"reg1":0.1,"reg2":0.1,"reg3":0.1,"mid":0.2,"fin":0.5}');
-- ============================================================
-- 3. USERS (Người dùng) - 5 users
-- ============================================================
INSERT INTO users (username, password, name, email) VALUES
('admin', '$2b$12$5IY3/C7jMBrYDwiXt.hmvuBhaJ1tmurvt70Omvan1s8JJ/uQD7IUO', 'Administrator', 'admin@mail.com'),
('vinh01', '$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW', 'Lưu Công Vinh', 'vinh01@gmail.com'),
('quan02', '$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW', 'Nguyễn Anh Quân', 'quan02@gmail.com'),
('teacher01', '$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW', 'Nguyễn Văn Giáo', 'teacher01@gmail.com'),
('teacher02', '$2b$12$tZ7sPnpc2w5cq0cbfbKVGewBH4DAXNIJmMJ5Wu3g2AlTrQwm/dxiW', 'Trần Thị Hương', 'teacher02@gmail.com');
-- Default password: 12112004
-- ============================================================
-- 4. SEMESTERS (Học kỳ) - 8 học kỳ
-- ============================================================
INSERT INTO semesters (year, term_order) VALUES
(2022, '1'), -- ID 1
(2022, '2'), -- ID 2
(2023, '1'), -- ID 3
(2023, '2'), -- ID 4
(2024, '1'), -- ID 5
(2024, '2'), -- ID 6
(2025, '1'), -- ID 7
(2025, '2'); -- ID 8
-- ============================================================
-- 5. MAJORS (Ngành) - 12 ngành thuộc 5 khoa
-- ============================================================
INSERT INTO majors (name, department_id) VALUES
-- Khoa Công nghệ thông tin (3 ngành)
('Công nghệ thông tin', 1),           -- ID 1
('Kỹ thuật phần mềm', 1),             -- ID 2
('An toàn thông tin', 1),             -- ID 3
-- Khoa Kinh tế (3 ngành)
('Kinh tế quốc tế', 2),               -- ID 4
('Kinh doanh quốc tế', 2),            -- ID 5
('Tài chính ngân hàng', 2),           -- ID 6
-- Khoa Kỹ thuật (2 ngành)
('Kỹ thuật cơ khí', 3),               -- ID 7
('Kỹ thuật điện tử', 3),              -- ID 8
-- Khoa Ngoại ngữ (2 ngành)
('Ngôn ngữ Anh', 4),                  -- ID 9
('Ngôn ngữ Nhật', 4),                 -- ID 10
-- Khoa Khoa học tự nhiên (2 ngành)
('Vật lý ứng dụng', 5),               -- ID 11
('Hóa học ứng dụng', 5);              -- ID 12
-- ============================================================
-- 6. DEPARTMENTAL CLASSES (Lớp) - 30 lớp
-- ============================================================
INSERT INTO departmental_classes (id, name, major_id) VALUES
-- Công nghệ thông tin (4 lớp)
('2022CNTT01', 'Lớp CNTT 2022-01', 1),
('2022CNTT02', 'Lớp CNTT 2022-02', 1),
('2023CNTT01', 'Lớp CNTT 2023-01', 1),
('2024CNTT01', 'Lớp CNTT 2024-01', 1),
-- Kỹ thuật phần mềm (3 lớp)
('2022KTPM01', 'Lớp KTPM 2022-01', 2),
('2022KTPM02', 'Lớp KTPM 2022-02', 2),
('2023KTPM01', 'Lớp KTPM 2023-01', 2),
-- An toàn thông tin (2 lớp)
('2022ATTT01', 'Lớp ATTT 2022-01', 3),
('2023ATTT01', 'Lớp ATTT 2023-01', 3),
-- Kinh tế quốc tế (3 lớp)
('2022KTQT01', 'Lớp KTQT 2022-01', 4),
('2022KTQT02', 'Lớp KTQT 2022-02', 4),
('2023KTQT01', 'Lớp KTQT 2023-01', 4),
-- Kinh doanh quốc tế (3 lớp)
('2022KDQT01', 'Lớp KDQT 2022-01', 5),
('2022KDQT02', 'Lớp KDQT 2022-02', 5),
('2023KDQT01', 'Lớp KDQT 2023-01', 5),
-- Tài chính ngân hàng (2 lớp)
('2022TCNH01', 'Lớp TCNH 2022-01', 6),
('2023TCNH01', 'Lớp TCNH 2023-01', 6),
-- Kỹ thuật cơ khí (2 lớp)
('2022KTCK01', 'Lớp KTCK 2022-01', 7),
('2023KTCK01', 'Lớp KTCK 2023-01', 7),
-- Kỹ thuật điện tử (2 lớp)
('2022KTDT01', 'Lớp KTĐT 2022-01', 8),
('2023KTDT01', 'Lớp KTĐT 2023-01', 8),
-- Ngôn ngữ Anh (2 lớp)
('2022NNGA01', 'Lớp NN Anh 2022-01', 9),
('2023NNGA01', 'Lớp NN Anh 2023-01', 9),
-- Ngôn ngữ Nhật (2 lớp)
('2022NNNB01', 'Lớp NN Nhật 2022-01', 10),
('2023NNNB01', 'Lớp NN Nhật 2023-01', 10),
-- Vật lý ứng dụng (2 lớp)
('2022VLUD01', 'Lớp VL ứng dụng 2022-01', 11),
('2023VLUD01', 'Lớp VL ứng dụng 2023-01', 11),
-- Hóa học ứng dụng (2 lớp)
('2022HHUD01', 'Lớp HH ứng dụng 2022-01', 12),
('2023HHUD01', 'Lớp HH ứng dụng 2023-01', 12);
-- ============================================================
-- 7. SECTIONAL CLASSES (Lớp học phần) - 60 lớp học phần
-- ============================================================
INSERT INTO sectional_classes (name, semester_id, subject_id, major_id) VALUES
-- Học kỳ 1/2022 (15 lớp)
('PE6021_HK1_L1', 1, 'PE6021', 1),
('PE6022_HK1_L1', 1, 'PE6022', 1),
('BM6091_HK1_L1', 1, 'BM6091', 1),
('BS6002_HK1_L1', 1, 'BS6002', 1),
('FL6085_HK1_L1', 1, 'FL6085', 1),
('IT6001_HK1_L1', 1, 'IT6001', 2),
('IT6002_HK1_L1', 1, 'IT6002', 2),
('BS6001_HK1_L1', 1, 'BS6001', 2),
('BM6091_HK1_L2', 1, 'BM6091', 4),
('BS6002_HK1_L2', 1, 'BS6002', 4),
('LP6010_HK1_L1', 1, 'LP6010', 4),
('BM6092_HK1_L1', 1, 'BM6092', 5),
('BS6003_HK1_L1', 1, 'BS6003', 5),
('PH6001_HK1_L1', 1, 'PH6001', 7),
('CH6001_HK1_L1', 1, 'CH6001', 12),
-- Học kỳ 2/2022 (15 lớp)
('LP6010_HK2_L1', 2, 'LP6010', 1),
('LP6011_HK2_L1', 2, 'LP6011', 1),
('IT6003_HK2_L1', 2, 'IT6003', 1),
('FL6086_HK2_L1', 2, 'FL6086', 1),
('IT6004_HK2_L1', 2, 'IT6004', 2),
('BS6003_HK2_L1', 2, 'BS6003', 2),
('FL6085_HK2_L2', 2, 'FL6085', 4),
('LP6010_HK2_L2', 2, 'LP6010', 4),
('BM6093_HK2_L1', 2, 'BM6093', 5),
('LP6012_HK2_L1', 2, 'LP6012', 5),
('BS6002_HK2_L1', 2, 'BS6002', 7),
('PH6001_HK2_L1', 2, 'PH6001', 8),
('FL6085_HK2_L3', 2, 'FL6085', 9),
('FL6086_HK2_L2', 2, 'FL6086', 9),
('CH6001_HK2_L1', 2, 'CH6001', 12),
-- Học kỳ 1/2023 (15 lớp)
('IT6010_HK3_L1', 3, 'IT6010', 1),
('IT6011_HK3_L1', 3, 'IT6011', 1),
('FL6087_HK3_L1', 3, 'FL6087', 1),
('IT6012_HK3_L1', 3, 'IT6012', 2),
('IT6013_HK3_L1', 3, 'IT6013', 2),
('BM6094_HK3_L1', 3, 'BM6094', 4),
('BS6001_HK3_L1', 3, 'BS6001', 4),
('LP6011_HK3_L1', 3, 'LP6011', 5),
('BM6091_HK3_L1', 3, 'BM6091', 5),
('IT6001_HK3_L1', 3, 'IT6001', 7),
('BS6002_HK3_L1', 3, 'BS6002', 8),
('FL6087_HK3_L2', 3, 'FL6087', 9),
('FL6085_HK3_L1', 3, 'FL6085', 10),
('PH6001_HK3_L1', 3, 'PH6001', 11),
('BI6001_HK3_L1', 3, 'BI6001', 12),
-- Học kỳ 2/2023 (15 lớp)
('PE6023_HK4_L1', 4, 'PE6023', 1),
('PE6024_HK4_L1', 4, 'PE6024', 2),
('PE6025_HK4_L1', 4, 'PE6025', 3),
('LP6012_HK4_L1', 4, 'LP6012', 1),
('EN6001_HK4_L1', 4, 'EN6001', 1),
('BM6092_HK4_L1', 4, 'BM6092', 4),
('BS6003_HK4_L1', 4, 'BS6003', 4),
('BM6093_HK4_L1', 4, 'BM6093', 5),
('LP6010_HK4_L1', 4, 'LP6010', 6),
('BS6001_HK4_L1', 4, 'BS6001', 7),
('IT6002_HK4_L1', 4, 'IT6002', 8),
('FL6086_HK4_L1', 4, 'FL6086', 9),
('FL6087_HK4_L1', 4, 'FL6087', 10),
('PH6001_HK4_L1', 4, 'PH6001', 11),
('CH6001_HK4_L1', 4, 'CH6001', 12);
-- ============================================================
-- 8. STUDENTS (Sinh viên) - 50 sinh viên
-- ============================================================
INSERT INTO students (sid, fname, lname, dob, address, cid, phone, email, gender, generation, status, img, departmental_class_id) VALUES
-- Lớp CNTT 2022 (8 sinh viên)
('2022602800', 'Lưu Công', 'Vinh', '2004-11-12', 'Hà Nội', '001204056492', '0348341246', 'vinh01@gmail.com', 1, 17, '1', NULL, '2022CNTT01'),
('2022602801', 'Nguyễn Văn', 'An', '2004-03-15', 'Hà Nội', '001204056493', '0348341247', 'an01@gmail.com', 1, 17, '1', NULL, '2022CNTT01'),
('2022602802', 'Trần Thị', 'Bình', '2004-07-20', 'Hải Phòng', '001204056494', '0348341248', 'binh01@gmail.com', 0, 17, '1', NULL, '2022CNTT01'),
('2022602803', 'Lê Minh', 'Cường', '2004-09-05', 'Đà Nẵng', '001204056495', '0348341249', 'cuong01@gmail.com', 1, 17, '1', NULL, '2022CNTT02'),
('2022602804', 'Phạm Thu', 'Dung', '2004-12-25', 'Hồ Chí Minh', '001204056496', '0348341250', 'dung01@gmail.com', 0, 17, '1', NULL, '2022CNTT02'),
('2022602805', 'Hoàng Văn', 'Em', '2004-02-14', 'Cần Thơ', '001204056497', '0348341251', 'em01@gmail.com', 1, 17, '1', NULL, '2022CNTT02'),
('2023602806', 'Đỗ Thị', 'Phương', '2005-05-10', 'Hà Nội', '001205056498', '0348341252', 'phuong01@gmail.com', 0, 18, '1', NULL, '2023CNTT01'),
('2024602807', 'Vũ Minh', 'Giang', '2006-08-18', 'Hải Phòng', '001206056499', '0348341253', 'giang01@gmail.com', 0, 19, '1', NULL, '2024CNTT01'),
-- Lớp KTPM 2022 (6 sinh viên)
('2022603001', 'Bùi Văn', 'Hải', '2004-01-22', 'Hà Nội', '001204056500', '0348341254', 'hai01@gmail.com', 1, 17, '1', NULL, '2022KTPM01'),
('2022603002', 'Ngô Thị', 'Hoa', '2004-06-30', 'Đà Nẵng', '001204056501', '0348341255', 'hoa01@gmail.com', 0, 17, '1', NULL, '2022KTPM01'),
('2022603003', 'Đinh Minh', 'Khoa', '2004-10-12', 'Hồ Chí Minh', '001204056502', '0348341256', 'khoa01@gmail.com', 1, 17, '1', NULL, '2022KTPM01'),
('2022603004', 'Trương Thị', 'Lan', '2004-04-08', 'Huế', '001204056503', '0348341257', 'lan01@gmail.com', 0, 17, '1', NULL, '2022KTPM02'),
('2022603005', 'Phan Văn', 'Minh', '2004-11-28', 'Nha Trang', '001204056504', '0348341258', 'minh01@gmail.com', 1, 17, '1', NULL, '2022KTPM02'),
('2023603006', 'Lý Thị', 'Nga', '2005-03-17', 'Hà Nội', '001205056505', '0348341259', 'nga01@gmail.com', 0, 18, '1', NULL, '2023KTPM01'),
-- Lớp ATTT 2022 (4 sinh viên)
('2022604001', 'Mai Văn', 'Oanh', '2004-07-05', 'Hà Nội', '001204056506', '0348341260', 'oanh01@gmail.com', 1, 17, '1', NULL, '2022ATTT01'),
('2022604002', 'Cao Thị', 'Phúc', '2004-09-20', 'Hải Phòng', '001204056507', '0348341261', 'phuc01@gmail.com', 0, 17, '1', NULL, '2022ATTT01'),
('2023604003', 'Đặng Minh', 'Quân', '2005-02-28', 'Đà Nẵng', '001205056508', '0348341262', 'quan01@gmail.com', 1, 18, '1', NULL, '2023ATTT01'),
('2023604004', 'Võ Thị', 'Rạng', '2005-12-15', 'Hồ Chí Minh', '001205056509', '0348341263', 'rang01@gmail.com', 0, 18, '1', NULL, '2023ATTT01'),
-- Lớp KTQT 2022 (6 sinh viên)
('2022605001', 'Nguyễn Anh', 'Quân', '2004-04-25', 'Hà Nội', '001204056510', '0348341264', 'quan02@gmail.com', 0, 17, '1', NULL, '2022KTQT01'),
('2022605002', 'Tô Văn', 'Sơn', '2004-08-10', 'Hải Phòng', '001204056511', '0348341265', 'son01@gmail.com', 1, 17, '1', NULL, '2022KTQT01'),
('2022605003', 'Lương Thị', 'Tâm', '2004-11-03', 'Đà Nẵng', '001204056512', '0348341266', 'tam01@gmail.com', 0, 17, '1', NULL, '2022KTQT01'),
('2022605004', 'Hồ Minh', 'Tuấn', '2004-01-18', 'Hồ Chí Minh', '001204056513', '0348341267', 'tuan01@gmail.com', 1, 17, '1', NULL, '2022KTQT02'),
('2022605005', 'Dương Thị', 'Uyên', '2004-05-22', 'Cần Thơ', '001204056514', '0348341268', 'uyen01@gmail.com', 0, 17, '1', NULL, '2022KTQT02'),
('2023605006', 'Chu Văn', 'Vũ', '2005-09-07', 'Hà Nội', '001205056515', '0348341269', 'vu01@gmail.com', 1, 18, '1', NULL, '2023KTQT01'),
-- Lớp KDQT 2022 (6 sinh viên)
('2022606001', 'Nguyễn Anh', 'Lạc', '2000-04-25', 'Hà Nội', '001200056516', '0348341270', 'lac01@gmail.com', 0, 15, '1', NULL, '2022KDQT01'),
('2022606002', 'Trịnh Văn', 'Xuân', '2004-02-12', 'Hải Phòng', '001204056517', '0348341271', 'xuan01@gmail.com', 1, 17, '1', NULL, '2022KDQT01'),
('2022606003', 'Lâm Thị', 'Yến', '2004-06-28', 'Đà Nẵng', '001204056518', '0348341272', 'yen01@gmail.com', 0, 17, '1', NULL, '2022KDQT01'),
('2022606004', 'Quách Minh', 'Anh', '2004-10-15', 'Hồ Chí Minh', '001204056519', '0348341273', 'anh01@gmail.com', 1, 17, '1', NULL, '2022KDQT02'),
('2022606005', 'Ông Thị', 'Bảo', '2004-12-05', 'Huế', '001204056520', '0348341274', 'bao01@gmail.com', 0, 17, '1', NULL, '2022KDQT02'),
('2023606006', 'Từ Văn', 'Chiến', '2005-03-30', 'Hà Nội', '001205056521', '0348341275', 'chien01@gmail.com', 1, 18, '1', NULL, '2023KDQT01'),
-- Lớp TCNH 2022 (4 sinh viên)
('2022607001', 'Hà Minh', 'Đức', '2004-07-14', 'Hà Nội', '001204056522', '0348341276', 'duc01@gmail.com', 1, 17, '1', NULL, '2022TCNH01'),
('2022607002', 'Thái Thị', 'Hằng', '2004-09-25', 'Hải Phòng', '001204056523', '0348341277', 'hang01@gmail.com', 0, 17, '1', NULL, '2022TCNH01'),
('2023607003', 'Lại Văn', 'Kiên', '2005-01-08', 'Đà Nẵng', '001205056524', '0348341278', 'kien01@gmail.com', 1, 18, '1', NULL, '2023TCNH01'),
('2023607004', 'Ứng Thị', 'Linh', '2005-05-19', 'Hồ Chí Minh', '001205056525', '0348341279', 'linh01@gmail.com', 0, 18, '1', NULL, '2023TCNH01'),
-- Lớp KTCK 2022 (4 sinh viên)
('2022608001', 'Khổng Minh', 'Nam', '2004-11-11', 'Hà Nội', '001204056526', '0348341280', 'nam01@gmail.com', 1, 17, '1', NULL, '2022KTCK01'),
('2022608002', 'Nghiêm Thị', 'Oanh', '2004-03-26', 'Hải Phòng', '001204056527', '0348341281', 'oanh02@gmail.com', 0, 17, '1', NULL, '2022KTCK01'),
('2023608003', 'Tạ Văn', 'Phong', '2005-08-02', 'Đà Nẵng', '001205056528', '0348341282', 'phong01@gmail.com', 1, 18, '1', NULL, '2023KTCK01'),
('2023608004', 'Ân Thị', 'Quỳnh', '2005-12-20', 'Hồ Chí Minh', '001205056529', '0348341283', 'quynh01@gmail.com', 0, 18, '1', NULL, '2023KTCK01'),
-- Lớp KTĐT 2022 (4 sinh viên)
('2022609001', 'Vương Minh', 'Sang', '2004-02-09', 'Hà Nội', '001204056530', '0348341284', 'sang01@gmail.com', 1, 17, '1', NULL, '2022KTDT01'),
('2022609002', 'Đào Thị', 'Thảo', '2004-06-16', 'Hải Phòng', '001204056531', '0348341285', 'thao01@gmail.com', 0, 17, '1', NULL, '2022KTDT01'),
('2023609003', 'Lưu Văn', 'Uy', '2005-10-23', 'Đà Nẵng', '001205056532', '0348341286', 'uy01@gmail.com', 1, 18, '1', NULL, '2023KTDT01'),
('2023609004', 'Hứa Thị', 'Vân', '2005-04-11', 'Hồ Chí Minh', '001205056533', '0348341287', 'van01@gmail.com', 0, 18, '1', NULL, '2023KTDT01'),
-- Lớp NN Anh 2022 (2 sinh viên)
('2022610001', 'Kiều Minh', 'Xuân', '2004-01-05', 'Hà Nội', '001204056534', '0348341288', 'xuan02@gmail.com', 1, 17, '1', NULL, '2022NNGA01'),
('2023610002', 'Bạch Thị', 'Yên', '2005-07-29', 'Hải Phòng', '001205056535', '0348341289', 'yen02@gmail.com', 0, 18, '1', NULL, '2023NNGA01'),
-- Lớp NN Nhật 2022 (2 sinh viên)
('2022611001', 'Diệp Văn', 'Anh', '2004-09-13', 'Hà Nội', '001204056536', '0348341290', 'anh02@gmail.com', 1, 17, '1', NULL, '2022NNNB01'),
('2023611002', 'Đoàn Thị', 'Bích', '2005-11-27', 'Đà Nẵng', '001205056537', '0348341291', 'bich01@gmail.com', 0, 18, '1', NULL, '2023NNNB01'),
-- Lớp VL ứng dụng 2022 (2 sinh viên)
('2022612001', 'Lục Minh', 'Châu', '2004-05-06', 'Hà Nội', '001204056538', '0348341292', 'chau01@gmail.com', 1, 17, '1', NULL, '2022VLUD01'),
('2023612002', 'Gia Thị', 'Duyên', '2005-08-21', 'Hồ Chí Minh', '001205056539', '0348341293', 'duyen01@gmail.com', 0, 18, '1', NULL, '2023VLUD01'),
-- Lớp HH ứng dụng 2022 (2 sinh viên)
('2022613001', 'Hạ Văn', 'Hùng', '2004-03-19', 'Hà Nội', '001204056540', '0348341294', 'hung01@gmail.com', 1, 17, '1', NULL, '2022HHUD01'),
('2023613002', 'Nhữ Thị', 'Khánh', '2005-12-08', 'Hải Phòng', '001205056541', '0348341295', 'khanh01@gmail.com', 0, 18, '1', NULL, '2023HHUD01');
-- ============================================================
-- 9. SCORES (Điểm) - Sample scores cho một số sinh viên
-- ============================================================
INSERT INTO scores (sectional_class_id, student_id, regular1, regular2, regular3, midterm, final) VALUES
-- Điểm cho Lưu Công Vinh (2022602800)
(1, '2022602800', 8.5, 9.0, 8.0, 0.0, 10.0), -- 1 is PE6021 (Midterm 0)
(3, '2022602800', 8.0, 8.5, 9.0, 9.5, 10.0),
(4, '2022602800', 9.0, 9.5, 0.0, 9.5, 10.0), -- 4 is BS6002 (Reg3 0)
(5, '2022602800', 8.5, 8.0, 9.0, 9.5, 10.0),
(16, '2022602800', 8.0, 9.0, 0.0, 9.0, 9.5), -- 16 is LP6010 (Reg3 0)
-- Điểm cho Nguyễn Anh Quân (2022605001)
(9, '2022605001', 8.0, 8.5, 9.0, 9.5, 10.0),
(10, '2022605001', 8.5, 9.0, 0.0, 9.5, 4.0), -- 10 is BS6002 (Reg3 0)
(22, '2022605001', 9.0, 8.5, 9.5, 9.0, 5.5),
(23, '2022605001', 8.0, 8.0, 0.0, 9.5, 10.0), -- 23 is LP6010 (Reg3 0)
-- Điểm cho Nguyễn Anh Lạc (2022606001)
(24, '2022606001', 7.0, 7.5, 8.0, 9.5, 10.0),
(25, '2022606001', 8.5, 8.0, 0.0, 8.0, 8.0), -- 25 is LP6012 (Reg3 0)
(29, '2022606001', 9.0, 9.5, 8.5, 9.5, 9.0),
(54, '2022606001', 8.0, 8.5, 9.0, 9.0, 7.0);