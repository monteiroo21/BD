# BD: Guião 5


## ​Problema 5.1
 
### *a)*

```
π Ssn, Fname, Minit, Lname, Pname (((employee) ⨝ Ssn=Essn (works_on)) ⨝ Pno = Pnumber (project))  
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
σ Essn=null ((employee ⨝ Ssn=Mgr_ssn department) ⟕ Ssn = Essn dependent)
```


### *i)* 

```
π Fname, Lname (σ Dlocation!='Aveiro' ∧ Plocation='Aveiro' (((employee ⨝ Dno=Dnumber department) ⨝ department.Dnumber=dept_location.Dnumber dept_location) ⨝ department.Dnumber=Dnum project))
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
π nome, numUtente (σ numPresc = null (prescricao ⟖ paciente))
```

### *b)* 

```
γ especialidade; count(numPresc) -> presc (medico ⨝ numSNS = numMedico prescricao)
```


### *c)* 

```
γ nome, endereco; count(numPresc) -> presc (farmacia ⨝ nome=farmacia prescricao)
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
π paciente.numUtente, nome (σ medico_num > 1 (γ paciente.numUtente, nome; count(numMedico)->medico_num (paciente ⨝ paciente.numUtente=prescricao.numUtente prescricao)))
```
