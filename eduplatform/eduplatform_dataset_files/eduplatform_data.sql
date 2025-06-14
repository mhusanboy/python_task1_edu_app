CREATE TABLE IF NOT EXISTS Users (
    id INT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    address TEXT
);

CREATE TABLE IF NOT EXISTS Students (
    user_id INT PRIMARY KEY,
    grade VARCHAR(10) NOT NULL,
    subjects TEXT,
    assignments TEXT,
    grades_data TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Teachers (
    user_id INT PRIMARY KEY,
    subjects TEXT,
    classes TEXT,
    workload INT,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Parents (
    user_id INT PRIMARY KEY,
    children_ids TEXT,
    notification_preferences TEXT,
    FOREIGN KEY (user_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Assignments (
    id INT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    deadline VARCHAR(255) NOT NULL,
    subject VARCHAR(100) NOT NULL,
    teacher_id INT NOT NULL,
    class_id VARCHAR(10) NOT NULL,
    difficulty VARCHAR(50) NOT NULL,
    submissions TEXT,
    grades TEXT,
    FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Grades (
    id INT PRIMARY KEY,
    student_id INT NOT NULL,
    subject VARCHAR(100) NOT NULL,
    value INT NOT NULL CHECK (value >= 1 AND value <= 5),
    date VARCHAR(255) NOT NULL,
    teacher_id INT NOT NULL,
    comment TEXT,
    FOREIGN KEY (student_id) REFERENCES Users(id) ON DELETE CASCADE,
    FOREIGN KEY (teacher_id) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Schedules (
    id INT PRIMARY KEY,
    class_id VARCHAR(10) NOT NULL,
    day VARCHAR(20) NOT NULL,
    lessons TEXT
);

CREATE TABLE IF NOT EXISTS Notifications (
    id INT PRIMARY KEY,
    message TEXT NOT NULL,
    recipient_id INT NOT NULL,
    created_at VARCHAR(255) NOT NULL,
    is_read BOOLEAN NOT NULL,
    priority INT NOT NULL,
    FOREIGN KEY (recipient_id) REFERENCES Users(id) ON DELETE CASCADE
);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (1, 'Super Admin', 'admin@edu.com', '713bfda78870bf9d1b261f565286f85e97ee614efe5f0faf7c34e7ca4f65baca', 'Admin', '2025-06-14T12:11:14.987474', NULL, NULL);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (2, 'Husanboy Mansuraliyev', 'mrhusanboy2006pm@gmail.com', '6e0e727325ed6e8770c658a353357fb590287f041fa43bc55e0a8a410ac491c6', 'Teacher', '2025-06-14T12:11:14.987488', '998-94-123-45-67', '123 Tashkent Rd');

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (3, 'Mardon Hazratov', 'mardonbekhazratov@gmail.com', '0c706cd9e9c31663612230ff8d74850ca2efdce103dedc77cdd66bf4cfd192ce', 'Student', '2025-06-14T12:11:14.987495', NULL, NULL);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (4, 'Shahriyor Yuldashev', 'yuldshah@gmail.com', '0c706cd9e9c31663612230ff8d74850ca2efdce103dedc77cdd66bf4cfd192ce', 'Student', '2025-06-14T12:11:14.987501', NULL, NULL);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (5, 'David Johnson', 'david@edu.com', '3f650137fe217270ad38b496da70838695e4595d64298ce28e0c86f2c39c3c1e', 'Parent', '2025-06-14T12:11:14.987506', NULL, NULL);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (6, 'Cristiano Ronaldo', 'CristianoRondaldo@gmail.com', '6ff063e2be77308b0c4782900838183d527fce72cd0b8fe48bb752b4848028f2', 'Student', '2025-06-14T12:11:14.987534', NULL, NULL);

INSERT INTO Users (id, full_name, email, password_hash, role, created_at, phone, address)
VALUES (7, 'Grace Lee', 'grace@edu.com', 'f688efc24c2c7799478078fdc0f6d874467799cbd65bcbb8e2ada33b45a49cf7', 'Student', '2025-06-14T12:11:15.059293', NULL, NULL);

INSERT INTO Students (user_id, full_name, grade, subjects, assignments, grades_data)
VALUES (3, 'Mardon Hazratov', '10-A', '{''Math'': 2, ''Informatics'': 2}', '{1: ''Submitted''}', '{''Math'': [4]}');

INSERT INTO Students (user_id, full_name, grade, subjects, assignments, grades_data)
VALUES (4, 'Shahriyor Yuldashev', '10-A', '{''Math'': 2}', '{}', '{}');

INSERT INTO Students (user_id, full_name, grade, subjects, assignments, grades_data)
VALUES (6, 'Cristiano Ronaldo', '9-B', '{}', '{}', '{}');

INSERT INTO Students (user_id, full_name, grade, subjects, assignments, grades_data)
VALUES (7, 'Grace Lee', '11-B', '{''Informatics'': 2}', '{}', '{}');

INSERT INTO Teachers (user_id, full_name, subjects, classes, workload)
VALUES (2, 'Husanboy Mansuraliyev', 'Math, Informatics', '10-A, 11-B', 0);

INSERT INTO Parents (user_id, full_name, children_ids, notification_preferences)
VALUES (5, 'David Johnson', '3', '{''low_grade_alert'': True, ''new_assignment_alert'': True}');

INSERT INTO Assignments (id, title, description, deadline, subject, teacher_id, class_id, difficulty, submissions, grades)
VALUES (1, 'Algebra Homework 1', 'Solve problems 1-5 from Chapter 3.', '2025-06-21T12:11:14.988041', 'Math', 2, '10-A', 'Medium', '{3: ''My detailed solutions for Algebra HW1.''}', '{3: 4}');

INSERT INTO Assignments (id, title, description, deadline, subject, teacher_id, class_id, difficulty, submissions, grades)
VALUES (2, 'Informatics Lab Report', 'Write a report on the group python project.', '2025-06-28T12:11:15.039179', 'Informatics', 2, '11-B', 'Hard', '{}', '{}');

INSERT INTO Grades (id, student_id, subject, value, date, teacher_id, comment)
VALUES (1, 3, 'Math', 4, '2025-06-14T12:11:15.059321', 2, 'Good effort, check problem 3.');

INSERT INTO Schedules (id, class_id, day, lessons)
VALUES (1, '10-A', 'Monday', '{''09:00'': {''subject'': ''Math'', ''teacher_id'': 2}, ''10:00'': {''subject'': ''Chemistry'', ''teacher_id'': 2}, ''11:00'': {''subject'': ''History'', ''teacher_id'': 999}}');

INSERT INTO Schedules (id, class_id, day, lessons)
VALUES (2, '11-B', 'Monday', '{}');

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority)
VALUES (1, 'New assignment: ''Algebra Homework 1'' for Math. Deadline: 2025-06-21T12:11:14.988041', 3, '2025-06-14T12:11:15.039138', 1, 0);

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority)
VALUES (4, 'You received a grade of 4 for ''Algebra Homework 1'' in Math.', 3, '2025-06-14T12:11:15.068246', 0, 2);

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority)
VALUES (5, 'Don''t forget your upcoming Informatics test!', 3, '2025-06-14T12:11:15.068309', 0, 1);

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority)
VALUES (3, 'New assignment: ''Algebra Homework 1'' for Math. Deadline: 2025-06-21T12:11:14.988041', 4, '2025-06-14T12:11:15.039168', 0, 0);

INSERT INTO Notifications (id, message, recipient_id, created_at, is_read, priority)
VALUES (2, 'Your child, Mardon Hazratov, has a new assignment: ''Algebra Homework 1''.', 5, '2025-06-14T12:11:15.039155', 0, 0);

