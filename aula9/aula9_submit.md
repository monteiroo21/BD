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
... Write here your answer ...
```

### *d)*

```
... Write here your answer ...
```

### *e)*

```
... Write here your answer ...
```

### *f)*

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

### *g)*

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

### *h)*

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
IF (NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES 
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

-- Create the AFTER DELETE trigger
CREATE TRIGGER trg_AfterDeleteDepartment
ON dbo.DEPARTMENT
AFTER DELETE
AS
BEGIN
    -- Insert the deleted department details into department_deleted
    INSERT INTO dbo.department_deleted (Dname, Dnumber, Mgr_ssn, Mgr_start_date)
    SELECT Dname, Dnumber, Mgr_ssn, Mgr_start_date FROM deleted;
END;
GO
```

### *i)*

```
... Write here your answer ...
```
