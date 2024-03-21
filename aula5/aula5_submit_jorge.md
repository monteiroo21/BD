# BD: Guião 5

## ​Problema 5.1

### *a)*

```
Write here your answer e.g:
π Fname, Lname, Ssn (employee) ⨝ project
(π Pname, Pnumber (project) ⨝ Pno=Pnumber (works_on)) ⨝.... 
```

### *b)*

```
employees = π Fname, Lname, Super_ssn (employee)
carlos_ssn = π Ssn (sigma Fname='Carlos' ∧ Lname='Gomes' (employee))
π Fname, Lname (employees ⨝ Super_ssn=Ssn carlos_ssn)
```

### *c)*

```

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

## ​Problema 5.2

### *a)*

```
... Write here your answer ...
π nome (σ numero = null (fornecedor ⟕ nif = fornecedor (encomenda)))
/*
projetar o nome dos fornecedores que têm o número de encomendas == 0 fazendo um  left outer join.
*/
```

### *b)*

```
... Write here your answer ...
π nome, MediaProd ((γ codProd; avg(unidades) -> MediaProd item) ⨝ codProd = codigo (produto))

/*
o codProd é a primary key do produto
ver também a resolução do zegameiro!!!!
*/
```

### *c)*

```
... Write here your answer ...
 π AverageTable ((γ avg(NumProdEnc) -> AverageTable (γ numEnc; count(codProd) -> NumProdEnc (item))))

```

### *d)*

```
... Write here your answer ...
π produto.nome, NumProdutos (γ codProd, produto.nome; count(codProd) -> NumProdutos (((item ⨝ codProd=codigo (produto)) ⨝ numEnc=numero (encomenda)) ⨝ fornecedor=nif (fornecedor)))
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
