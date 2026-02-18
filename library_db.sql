
DROP DATABASE IF EXISTS library_db;
CREATE DATABASE library_db;
USE library_db;
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL   -- admin or student
);

CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    author VARCHAR(200) NOT NULL,
    cover VARCHAR(300)
);
CREATE TABLE issued_books (
    id INT AUTO_INCREMENT PRIMARY KEY,
    book_id INT NOT NULL,
    student_id INT NOT NULL,
    issue_date DATE NOT NULL,
    return_date DATE,
    fine INT DEFAULT 0,

    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,
    FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE
);
INSERT INTO users (username, password, role)
VALUES 
('admin', 'admin123', 'admin'),
('student', 'student123', 'student');
INSERT INTO books (title, author, cover)
VALUES
('Database Management System', 'Korth', ''),
('Python Programming', 'Guido van Rossum', ''),
('Data Structures', 'Seymour Lipschutz', '');