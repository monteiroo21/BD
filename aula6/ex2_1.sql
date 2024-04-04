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

-- Insert data --
INSERT INTO Employee VALUES
    ('Paula','A','Sousa',183623612,'2001-08-11','Rua da FRENTE','F',1450,NULL,3),
    ('Carlos','D','Gomes',21312332 ,'2000-01-01','Rua XPTO','M',1200,NULL,1),
    ('Juliana','A','Amaral',321233765,'1980-08-11','Rua BZZZZ','F',1350,NULL,3),
    ('Maria','I','Pereira',342343434,'2001-05-01','Rua JANOTA','F',1250,21312332,2),
    ('Joao','G','Costa',41124234 ,'2001-01-01','Rua YGZ','M',1300,21312332,2),
    ('Ana','L','Silva',12652121 ,'1990-03-03','Rua ZIG ZAG','F',1400,21312332,2);

INSERT INTO Department VALUES
    ('Investigacao',1,21312332 ,'2010-08-02'),
    ('Comercial',2,321233765,'2013-05-16'),
    ('Logistica',3,41124234 ,'2013-05-16'),
    ('Recursos Humanos',4,12652121,'2014-04-02'),
    ('Desporto',5,NULL,NULL);

INSERT INTO Dependent VALUES
    (21312332 ,'Joana Costa','F','2008-04-01', 'Filho'),
    (21312332 ,'Maria Costa','F','1990-10-05', 'Neto'),
    (21312332 ,'Rui Costa','M','2000-08-04','Neto'),
    (321233765,'Filho Lindo','M','2001-02-22','Filho'),
    (342343434,'Rosa Lima','F','2006-03-11','Filho'),
    (41124234 ,'Ana Sousa','F','2007-04-13','Neto'),
    (41124234 ,'Gaspar Pinto','M','2006-02-08','Sobrinho');

INSERT INTO Dept_locations VALUES
    (1,'Aveiro'),
    (2,'Coimbra'),
    (3,'Espinho'),
    (4,'Porto');


INSERT INTO Project VALUES
    ('Aveiro Digital',1,'Aveiro',3),
    ('BD Open Day',2,'Espinho',2),
    ('Dicoogle',3,'Aveiro',3),
    ('GOPACS',4,'Aveiro',3);

INSERT INTO Works_on VALUES
    (183623612,1,20),
    (183623612,3,10),
    (21312332 ,1,20),
    (321233765,1,25),
    (342343434,1,20),
    (342343434,4,25),
    (41124234 ,2,20),
    (41124234 ,3,30);

ALTER TABLE Employee
    ADD CONSTRAINT EMPDEPTFK FOREIGN KEY (Dno) REFERENCES Department(Dnumber);

ALTER TABLE Department
    ADD CONSTRAINT DEPTMGRFK FOREIGN KEY (Mgr_ssn) REFERENCES Employee(Ssn);