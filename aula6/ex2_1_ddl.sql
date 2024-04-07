CREATE DATABASE COMPANY;
GO
USE COMPANY;
GO

CREATE TABLE Employee (
    Fname VARCHAR(16),
    Minit VARCHAR(16),
    Lname VARCHAR(16),
    Ssn INT NOT NULL,
    Bdate DATE,
    [Address] VARCHAR(32),
    Sex VARCHAR(1),
    Salary INT,
    Super_ssn INT,
    Dno INT,

    PRIMARY KEY(Ssn),
    FOREIGN KEY(Super_ssn) REFERENCES Employee(Ssn)
);

CREATE TABLE Department (
    Dname VARCHAR(16),
    Dnumber INT NOT NULL,
    Mgr_ssn INT,
    Mgr_start_date DATE,

    PRIMARY KEY(Dnumber),
    UNIQUE(Dname)
);

CREATE TABLE Dept_locations (
    Dnumber INT NOT NULL,
    Dlocation VARCHAR(16) NOT NULL,

    PRIMARY KEY(Dnumber, Dlocation),
    FOREIGN KEY(Dnumber) REFERENCES Department(Dnumber)
);

CREATE TABLE Project (
    Pname VARCHAR(16) NOT NULL,
    Pnumber INT NOT NULL,
    Plocation VARCHAR(16),
    Dnum INT,

    PRIMARY KEY(Pnumber),
    UNIQUE(Pname),
    FOREIGN KEY(Dnum) REFERENCES Department(Dnumber)
);

CREATE TABLE Works_on (
    Essn INT NOT NULL,
    Pno INT NOT NULL,
    [Hours] INT,

    PRIMARY KEY(Essn, Pno),
    FOREIGN KEY(Essn) REFERENCES Employee(Ssn),
    FOREIGN KEY(Pno) REFERENCES Project(Pnumber)
);

CREATE TABLE Dependent (
    Essn INT NOT NULL,
    Dependent_name VARCHAR(16) NOT NULL,
    Sex VARCHAR(1),
    Bdate DATE,
    Relationship VARCHAR(8),

    PRIMARY KEY(Essn, Dependent_name),
    FOREIGN KEY(Essn) REFERENCES Employee(Ssn)
);

----------------------------------------
-- Insert data here --
----------------------------------------

ALTER TABLE Employee
    ADD CONSTRAINT EMPDEPTFK FOREIGN KEY (Dno) REFERENCES Department(Dnumber);

ALTER TABLE Department
    ADD CONSTRAINT DEPTMGRFK FOREIGN KEY (Mgr_ssn) REFERENCES Employee(Ssn);