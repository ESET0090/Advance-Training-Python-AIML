CREATE TABLE Employee1 (
   ID INT,
   name VARCHAR(50),
   city VARCHAR(100),
   Salary INT
);

select * from Employee1;

INSERT INTO Employee1 (id, name, city, Salary)
values (1, 'Gaurav', 'Nashik', 50000),
       (2, 'Milan', 'Udaipur', 55000),
	   (3, 'Uday', 'Surat', 60000);

-- Question 1. Write SELECT statements with filtering (WHERE)

select name from Employee1
where id = 2;

-- Question 2. Use ORDER BY and LIMIT clauses

SELECT *
FROM Employee1
ORDER BY salary ASC
LIMIT 2;

-- Question 3. Insert, update, and delete data

-- Insert Data

INSERT INTO Employee1 (id, name, city, salary)
VALUES (4, 'Rahul', 'Pune', 65000);

-- Update Data

UPDATE Employee1
SET salary = 52000
WHERE name = 'Gaurav';

-- Delete Data

DELETE FROM Employee1
WHERE id = 4;


-- Question 4. Use DISTINCT and aggregate functions (COUNT, SUM, AVG)

SELECT DISTINCT city
FROM Employee1;

SELECT COUNT(id) AS total_employees
FROM Employee1;

-- Question 5. Basic string and date/time functions

SELECT UPPER(name) AS uppercase_name
FROM Employee1;

SELECT name, LENGTH(name) AS name_length
FROM Employee1;


SELECT CURRENT_DATE AS today;