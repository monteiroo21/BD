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
... Write here your answer ...
```

### *g)*

```
... Write here your answer ...
```

### *h)*

```
... Write here your answer ...
```

### *i)*

```
... Write here your answer ...
```
