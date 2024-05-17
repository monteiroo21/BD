# BD: Guião 9

## ​9.1

### *a)*

```
GO
ALTER PROC Ex1 @Ssn INT
AS
BEGIN
 DECLARE @ssn_id INT;
 SELECT @ssn_id = Ssn FROM Employee WHERE Ssn = @Ssn;

 DELETE FROM Dependent WHERE Essn = @ssn_id;
 DELETE FROM Works_on WHERE Essn = @ssn_id; 

 UPDATE Employee SET Super_ssn = NULL WHERE Employee.Super_ssn = @ssn_id;
 UPDATE Department SET Mgr_ssn = NULL WHERE Department.Mgr_ssn = @ssn_id;

 DELETE FROM Employee WHERE Ssn = @ssn_id;
END;

---------
GO
USE COMPANY
GO

SELECT * FROM Employee

EXEC Ex1 12652121;

SELECT * FROM Employee

```

### *b)*

```
GO
ALTER PROC Exb @oldSsn INT OUTPUT
AS
BEGIN

 SELECT Employee.Fname, Employee.Minit, Employee.Lname, Employee.Ssn, Employee.Bdate, DATEDIFF(YEAR, Department.Mgr_start_date, GETDATE()) AS oldYears
 FROM Employee JOIN Department ON Department.Mgr_ssn = Employee.Ssn;

 SELECT TOP(1) @oldSsn = Employee.ssn
    FROM Employee JOIN Department ON Employee.Ssn = Department.Mgr_ssn
    ORDER BY Department.Mgr_start_date;

    -- (Opcional) Retornar os dados do gerente mais antigo, se necessário
    SELECT Employee.Fname, Employee.Minit, Employee.Lname, Employee.Ssn, Employee.Bdate, DATEDIFF(YEAR, Department.Mgr_start_date, GETDATE()) AS oldYears
    FROM Employee JOIN Department ON Employee.Ssn = Department.Mgr_ssn
    WHERE Employee.Ssn = @oldSsn;
END;

---------

GO
USE COMPANY
GO

DECLARE @oldSsn INT
EXEC Exb @oldSsn OUTPUT
PRINT @oldSsn
```

### *c)*

```
GO
CREATE TRIGGER Exc ON DEPARTMENT
AFTER INSERT, UPDATE
AS
BEGIN
 SET NOCOUNT ON;

 IF EXISTS (SELECT Mgr_ssn FROM Department WHERE Mgr_ssn IS NOT NULL 
 GROUP BY Mgr_ssn HAVING COUNT(Mgr_ssn) > 1)
 BEGIN
  RAISERROR ('Error: Employee is already manager of another department.', 16, 1);
  ROLLBACK TRANSACTION;
 END
END;


-------

GO
USE COMPANY;
GO

Select * from Department;
Select * from Employee;

INSERT INTO Department VALUES ('Tecnologia', 11, 21312332, '2012-08-02');

```

### *d)*

```
... Write here your answer ...                          Ver mais tarde!!!!!!!
GO 
ALTER TRIGGER Exd ON Employee
AFTER INSERT, UPDATE
AS
BEGIN
 DECLARE @SalaryEmployee INT
 DECLARE @SalaryMan INT
 DECLARE @EmpSsn INT

 SELECT @EmpSsn = I.Ssn, @SalaryEmployee = I.Salary, @SalaryMan = E.Super_ssn 
 FROM inserted AS I
 JOIN Employee AS E ON I.Super_ssn = E.Ssn

 IF (@SalaryEmployee > @SalaryMan)
  BEGIN
   UPDATE Employee SET Salary = @SalaryMan - 1 WHERE Ssn = @EmpSsn
  END
END

```

### *e)*

```
CREATE FUNCTION getProjects ( @ssn INT ) RETURNS TABLE
AS 
	RETURN ( SELECT Pname, Plocation
					FROM Project
					JOIN Works_on ON Project.Pnumber = Works_on.Pno
					JOIN Employee ON Works_on.Essn = Employee.Ssn
					WHERE Employee.Ssn = @ssn);

GO
SELECT * FROM getProjects(321233765)
```

### *f)*

```
CREATE FUNCTION getFunctionaries ( @dno INT ) RETURNS TABLE
AS 
	RETURN ( SELECT *
					FROM Employee
					JOIN Department ON Employee.Dno = Department.Dnumber
					WHERE Department.Dnumber = @dno
					AND Employee.Salary > (SELECT AVG(Salary)
													FROM Employee
													WHERE Employee.Dno = @dno)
	);

GO
SELECT * FROM getFunctionaries(2)
```

### *g)*

```
DROP FUNCTION IF EXISTS dbo.employeeDeptHighAverage
GO
CREATE FUNCTION dbo.employeeDeptHighAverage (@dno INT)
RETURNS @budgetInfo TABLE (
    Pname        VARCHAR(255),
    Pnumber      INT,
    Plocation    VARCHAR(255),
    Dnum         INT,
    Budget       DECIMAL(10,2),
    TotalBudget  DECIMAL(10,2)
)
AS
BEGIN
    DECLARE @Pname VARCHAR(255), @Pnumber INT, @Plocation VARCHAR(255), @Dnum INT, @Budget DECIMAL(10,2), @TotalBudget DECIMAL(10,2) = 0;

    DECLARE budgetCursor CURSOR FOR
        SELECT Pname, Pnumber, Plocation, Dnum
            FROM Project
            WHERE Dnum = @dno;

    OPEN budgetCursor;

    FETCH NEXT FROM budgetCursor INTO @Pname, @Pnumber, @Plocation, @Dnum;
    
    WHILE @@FETCH_STATUS = 0
    BEGIN
        SELECT @Budget = SUM((Salary / 160.0) * Hours * 4) 
            FROM Works_on
            JOIN Employee ON Works_on.Essn = Employee.Ssn
            WHERE Works_on.Pno = @Pnumber;

        SET @TotalBudget = @TotalBudget + ISNULL(@Budget, 0);

        INSERT INTO @budgetInfo(Pname, Pnumber, Plocation, Dnum, Budget, TotalBudget)
        VALUES (@Pname, @Pnumber, @Plocation, @Dnum, ISNULL(@Budget, 0), @TotalBudget);

        FETCH NEXT FROM budgetCursor INTO @Pname, @Pnumber, @Plocation, @Dnum;
    END;

    CLOSE budgetCursor;
    DEALLOCATE budgetCursor;

    RETURN;
END;
GO

SELECT * FROM dbo.employeeDeptHighAverage(3);
```

### *h)*

```
IF (EXISTS (SELECT * 
				FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'department_deleted'))
BEGIN
    CREATE TABLE dbo.department_deleted (
        Dname VARCHAR(255),
        Dnumber INT PRIMARY KEY,
        Mgr_ssn CHAR(9),
        Mgr_start_date DATE
    );
END
GO

ALTER TRIGGER trg_AfterDeleteDepartment
ON dbo.DEPARTMENT
AFTER DELETE
AS
BEGIN
  
    INSERT INTO dbo.department_deleted (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
    SELECT Dname, Dnumber, Mgr_ssn, Mgr_start_date
		FROM deleted;
END;
GO
```

### *h)* 

```
IF (EXISTS (SELECT * 
				FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'department_deleted'))
BEGIN
    CREATE TABLE dbo.department_deleted (
        Dname VARCHAR(255),
        Dnumber INT PRIMARY KEY,
        Mgr_ssn CHAR(9),
        Mgr_start_date DATE
    );
END
GO

CREATE TRIGGER trg_InsteadOfDeleteDepartment
ON dbo.DEPARTMENT
INSTEAD OF DELETE
AS
BEGIN
    INSERT INTO dbo.department_deleted (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
    SELECT Dname, Dnumber, Mgr_ssn, Mgr_start_date 
		FROM deleted;
    
    DELETE 
		FROM dbo.DEPARTMENT
		WHERE Dnumber IN (SELECT Dnumber FROM deleted);
END;
GO
```

### *i)*

```
... Write here your answer ...
```
