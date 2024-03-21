# BD: Guião 5


## ​Problema 5.1
 
### *a)*

```
Write here your answer e.g:
π Fname, Lname, Ssn (employee) ⨝ project
π Pname, Fname, Lname, Ssn (project ⨝ Pnumber=Pno works_on ⨝ employee) 
```


### *b)* 

```
employees = π Fname, Lname, Super_ssn (employee)
carlos_ssn = π Ssn (sigma Fname='Carlos' ∧ Lname='Gomes' (employee))
π Fname, Lname (employees ⨝ Super_ssn=Ssn carlos_ssn)
```


### *c)* 

```
γ Pnumber, Pname; sum(Hours) -> Hours ((project) ⨝ Pnumber=Pno (works_on))
```


### *d)* 

```
π Fname, Lname (σ Dno = 3 ∧ Hours > 20 (employee ⨝ Ssn=Essn works_on))
```


### *e)* 

```
π Fname, Lname (σ Hours=null (employee ⟕ Ssn=Essn works_on))
```


### *f)* 

```
γ Dname; avg(Salary) -> avg_Salary (σ Sex='F' (employee ⨝ Dno=Dnumber department))
```


### *g)* 

```
π Fname, Lname (σ count_Dep > 2 (γ Fname, Lname; count(Essn) -> count_Dep (employee⨝Ssn=Essn dependent)))
```


### *h)* 

```
... Write here your answer ...
```


### *i)* 

```
... Write here your answer ...
```


## ​Problema 5.2

### *a)*

```
... Write here your answer ...
```

### *b)* 

```
... Write here your answer ...
```


### *c)* 

```
... Write here your answer ...
```


### *d)* 

```
... Write here your answer ...
```


## ​Problema 5.3

### *a)*

```
... Write here your answer ...
```

### *b)* 

```
... Write here your answer ...
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
