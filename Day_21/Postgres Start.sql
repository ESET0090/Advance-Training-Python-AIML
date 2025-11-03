INSERT INTO employeedb (id, name, city)
values (3200, 'Uday', 'Nashik');

Select * from employeedb;

INSERT INTO employeedb (id, name, city)
values (3201, 'Saurabh', 'Vaishali');


INSERT INTO employeedb (id, name, city)
values (3202, 'Abhishek', 'Indore');

UPDATE employeedb
SET city = 'panna'
WHERE name = 'Abhishek';

Delete from employeedb
where id = 3202;

