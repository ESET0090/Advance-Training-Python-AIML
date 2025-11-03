-- Question 1. Implement INNER JOIN, LEFT JOIN, RIGHT JOIN

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    department_id INT
);


Select * from Employees;

INSERT INTO Employees (employee_id, employee_name, department_id)
VALUES
    (1, 'Gaurav', 90),
    (2, 'Uday', 90),
    (3, 'Milan', 100),
    (4, 'Aniket', 110),
    (5, 'Shubham', 120);

CREATE TABLE Departments (
    department_id INT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL
);

Select * from Departments;

INSERT INTO Departments (department_id, department_name)
VALUES
    (100, 'HR'),
    (90, 'IT'),
    (110, 'Finance'),
    (120, 'Marketing');


-- Inner Join

SELECT
    E.employee_name,
    D.department_name
FROM
    Employees AS E
INNER JOIN
    Departments AS D ON E.department_id = D.department_id;


-- Left Join

SELECT
    E.employee_name,
    D.department_name
FROM
    Employees AS E
LEFT JOIN
    Departments AS D ON E.department_id = D.department_id;

-- Right Join

SELECT
    E.employee_name,
    D.department_name
FROM
    Employees AS E
RIGHT JOIN
    Departments AS D ON E.department_id = D.department_id;

-- Question 2 Write simple correlated and non-correlated subqueries

-- non - correlated Subquery

select * from Employees;
select * from Departments;

SELECT employee_name
FROM Employees
WHERE department_id = (
    SELECT department_id
    FROM Departments
    WHERE department_name = 'IT' 
);

-- corrlated subquery

SELECT
    employee_name,
    employee_id
FROM
    Employees AS E1
WHERE
    employee_id = (
        SELECT MAX(employee_id)
        FROM Employees AS E2
        WHERE E2.department_id = E1.department_id
    );

-- Question 3 use EXISTS and IN predicates

-- Exists
SELECT department_id
FROM departments d
WHERE EXISTS (
    SELECT 1
    FROM Employees e
    WHERE e.department_id = d.department_id
);

-- IN
SELECT department_id
FROM Departments
WHERE department_id IN (90, 100);

-- Question 4 UNION and UNION All

-- UNION

SELECT employee_name, department_id FROM Employees WHERE department_id = 90
UNION
SELECT employee_name, department_id FROM Employees WHERE employee_id = 1;

-- UNION ALL

SELECT employee_name, department_id FROM Employees WHERE department_id = 90
UNION ALL
SELECT employee_name, department_id FROM Employees WHERE employee_id = 1;
