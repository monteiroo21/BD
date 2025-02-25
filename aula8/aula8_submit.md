# BD: Guião 8

## ​8.1. Complete a seguinte tabela

Complete the following table.

| #    | Query                                                                                                      | Rows  | Cost  | Pag. Reads | Time (ms) | Index used | Index Op.            | Discussion |
| :--- | :--------------------------------------------------------------------------------------------------------- | :---- | :---- | :--------- | :-------- | :--------- | :------------------- | :--------- |
| 1    | SELECT * from Production.WorkOrder                                                                         | 72591 | 0.484 | 531        | 1171      |WorkOrderID          | Clustered Index Scan |            |
| 2    | SELECT * from Production.WorkOrder where WorkOrderID=1234                                                  |   1   |    0.00328  |     26      |     125     |     WorkOrderID      |           Clustered Index Seek          |            |
| 3.1  | SELECT * FROM Production.WorkOrder WHERE WorkOrderID between 10000 and 10010                               |    11   |   0.0033   |      26     |      178    |      WorkOrderID      |           Clustered Index Seek           |            |
| 3.2  | SELECT * FROM Production.WorkOrder WHERE WorkOrderID between 1 and 72591                                   |    72591    |  0.488    |      524     |      1720    |      WorkOrderID      |            Clustered Index Seek           |            |
| 4    | SELECT * FROM Production.WorkOrder WHERE StartDate = '2007-06-25'                                          |   72591    |   0.473   |      554     |      345    |       WorkOrderID     |         Clustered Index Scan             |            |
| 5    | SELECT * FROM Production.WorkOrder WHERE ProductID = 757                                                   |   9    |   0.0368    |      1449     |     217     |       ProductID     |         Index Seek (NonClustered)           |            |
| 6.1  | SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 757                              |    9   |   0.033    |      1535      |    91      |      ProductID Covered (StartDate)      |           Index Seek (NonClustered)           |            |
| 6.2  | SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945                              |   1105    |    0.006   |      236      |      46     |      ProductID Covered (StartDate)      |          Index Seek (NonClustered)            |            |
| 6.3  | SELECT WorkOrderID FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04'            |   1    |   0.006    |      421      |      14     |     ProductID Covered (StartDate)      |           Index Seek (NonClustered)           |            |
| 7    | SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04' |    1   |   0.0168    |       2743     |     254     |      ProductID and StartDate      |          Index Seek (NonClustered)            |            |
| 8    | SELECT WorkOrderID, StartDate FROM Production.WorkOrder WHERE ProductID = 945 AND StartDate = '2006-01-04' |    1   |    0.0328   |      1541      |      182     |      Composite (ProductID, StartDate)     |            Index Seek (NonClustered)          |            |

## ​8.2

### a)

```
CREATE TABLE mytemp ( 
    rid BIGINT /*IDENTITY (1, 1)*/ NOT NULL, 
    at1 INT NULL, 
    at2 INT NULL, 
    at3 INT NULL, 
    lixo varchar(100) NULL,

    PRIMARY KEY (rid)
);
```

### b)

```
Fragmentação dos índices: 99,06%
Ocupação das páginas: 68,76%
```

### c)

```
65 -> 03:08
80 -> 03:34
90 -> 03:31
```

### d)

```
65 -> 02:14
80 -> 02:38
90 -> 02:25
```

### e)

```
CREATE INDEX ixAt1 ON mytemp(at1);
CREATE INDEX ixAt2 ON mytemp(at2);
CREATE INDEX ixAt3 ON mytemp(at3);

Com todos os índices criados, o tempo de execução aumenta.
```

## ​8.3

```
i.   (PRIMARY KEY)

ii.  CREATE INDEX ixName ON EMPLOYEE(Fname, Lname)

iii. CREATE INDEX ixDno ON EMPLOYEE(Dno)

iv.  CREATE INDEX ixSsn ON WORKS_ON(Essn, Pno)

v.   (PRIMARY KEY)

vi.  CREATE INDEX ixPnumber ON Project(Dnum)
```
