DROP DATABASE IF EXISTS student_management;

-- 1. Create and select the database
CREATE DATABASE IF NOT EXISTS student_management;
USE student_management;

-- 2. Create tables in order of dependency
-- (Tables with no foreign keys first)
CREATE TABLE IF NOT EXISTS departments(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS subjects(
    id CHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    coff VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS users(
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(30) UNIQUE,
    password VARCHAR(200),
    name VARCHAR(50),
    email VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS semesters(
    id INT AUTO_INCREMENT PRIMARY KEY,
    year INT,
    term_order ENUM ('1','2','3','4')
);

-- Tables that depend on the first group
CREATE TABLE IF NOT EXISTS majors(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS departmental_classes(
    id VARCHAR(20) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    major_id INT NOT NULL,
    FOREIGN KEY (major_id) REFERENCES majors(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- This table represents specific course offerings (e.g., "Math 101, Section A")
CREATE TABLE IF NOT EXISTS sectional_classes(
    id INT AUTO_INCREMENT PRIMARY KEY, -- Added for a simple FK in the 'scores' table
    name VARCHAR(20) UNIQUE,
    semester_id INT NOT NULL,
    subject_id CHAR(10) NOT NULL,
    major_id INT NOT NULL, -- Added column that was missing but referenced
    
    -- Added missing foreign keys
    FOREIGN KEY (semester_id) REFERENCES semesters(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    
    -- Corrected the foreign key that was duplicated and broken
    FOREIGN KEY (major_id) REFERENCES majors(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    
    -- Ensures you can't have the same named section for the same subject/semester
    UNIQUE KEY uk_class_section (semester_id, subject_id, name)
);

-- Tables that depend on the second group
CREATE TABLE IF NOT EXISTS students(
    sid CHAR(10) PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(100) NOT NULL,
    dob DATE NOT NULL,
    address VARCHAR(150),
    cid CHAR(12) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(100) UNIQUE,
    gender BIT,
    generation INT,
    status ENUM('-1', '0','1','2'),
    img VARCHAR(500),
    departmental_class_id VARCHAR(20) NOT NULL, -- CORRECTED: Changed type from INT to VARCHAR(200
    FOREIGN KEY (departmental_class_id) REFERENCES departmental_classes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Junction table (depends on students and sectional_classes)
CREATE TABLE IF NOT EXISTS scores(
    sectional_class_id INT NOT NULL,
    student_id CHAR(10) NOT NULL,
    regular1 FLOAT,
    regular2 FLOAT,
    regular3 FLOAT,
    midterm FLOAT,
    final FLOAT,
    PRIMARY KEY (sectional_class_id, student_id),
    FOREIGN KEY (sectional_class_id) REFERENCES sectional_classes(id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (student_id) REFERENCES students(sid)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


