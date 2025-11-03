CREATE TABLE AIML_Database (
   ID INT,
   name VARCHAR(50),
   city VARCHAR(100),
   Salary INT
);

Select * from AIML_Database;

INSERT INTO AIML_Database (id, name, city, Salary)
values (1, 'Gaurav', 'Nashik', 50000),
       (2, 'Milan', 'Udaipur', 55000),
	   (3, 'Uday', 'Surat', 60000),
	   (4, 'Saurabh', 'Vaishali', 70000),
	   (5, 'Shubham', 'Mumbai', 750000),
	   (6, 'Abhishek', 'Panna', 80000),
	   (7, 'Gopal', 'Bhavnagar', 85000),
	   (8, 'Aniket', 'Siliguri', 90000),
	   (9, 'Rutu', 'Guwahati', 95000);

-- Question Practice

-- Question 1

-- Already Done

-- Question 2

-- Modifying the table

CREATE TABLE AIML_Database_new (
   ID INT PRIMARY KEY,
   name VARCHAR(50) NOT NULL,
   city VARCHAR(100) UNIQUE,
   Salary INT
);

Select * from AIML_Database_new;

INSERT INTO AIML_Database_new (id, name, city, Salary)
values (1, 'Gaurav', 'Nashik', 50000),
       (2, 'Milan', 'Udaipur', 55000),
	   (3, 'Uday', 'Surat', 60000),
	   (4, 'Saurabh', 'Vaishali', 70000),
	   (5, 'Shubham', 'Mumbai', 750000),
	   (6, 'Abhishek', 'Panna', 80000),
	   (7, 'Gopal', 'Bhavnagar', 85000),
	   (8, 'Aniket', 'Siliguri', 90000),
	   (9, 'Rutu', 'Guwahati', 95000);

-- Q3. Define the Default values and check constraints

ALTER TABLE AIML_Database_new
ADD COLUMN last_name VARCHAR(50) DEFAULT 'ABC';

-- Q4. Understand and use SERIAL and UUID types
ALTER TABLE AIML_Database_new
ADD COLUMN serial_id SERIAL;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

ALTER TABLE AIML_Database_new
ADD COLUMN unique_uuid UUID DEFAULT uuid_generate_v4();


-- Q5. Alter tables to add/drop columns and constraints

INSERT INTO AIML_Database_new (id, name, city, Salary)
values (10, 'ABC', 'XYZ', 50000);

DELETE FROM AIML_Database_new
WHERE city = 'XYZ';



