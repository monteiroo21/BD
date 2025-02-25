# BD: Guião 6

## Problema 6.1

### *a)* Todos os tuplos da tabela autores (authors)

```
SELECT * FROM authors
```

### *b)* O primeiro nome, o último nome e o telefone dos autores

```
SELECT au_fname, au_lname, phone 
    FROM authors
```

### *c)* Consulta definida em b) mas ordenada pelo primeiro nome (ascendente) e depois o último nome (ascendente)

```
SELECT au_fname, au_lname, phone 
    FROM authors 
    ORDER BY au_fname, au_lname ASC
```

### *d)* Consulta definida em c) mas renomeando os atributos para (first_name, last_name, telephone)

```
SELECT au_fname as first_name, au_lname as last_name, phone as telephone 
    FROM authors 
    ORDER BY first_name, last_name ASC
```

### *e)* Consulta definida em d) mas só os autores da Califórnia (CA) cujo último nome é diferente de ‘Ringer’

```
SELECT au_fname as first_name, au_lname as last_name, phone as telephone 
    FROM authors 
    WHERE state = 'CA' AND au_lname != 'Ringer' 
    ORDER BY first_name, last_name ASC
```

### *f)* Todas as editoras (publishers) que tenham ‘Bo’ em qualquer parte do nome

```
SELECT * 
    FROM publishers
    WHERE pub_name LIKE '%Bo%'
```

### *g)* Nome das editoras que têm pelo menos uma publicação do tipo ‘Business’

```
SELECT DISTINCT pub_name FROM publishers 
    JOIN titles ON publishers.pub_id = titles.pub_id 
    WHERE [type] = 'Business'
```

### *h)* Número total de vendas de cada editora

```
SELECT pub_name, COUNT(qty) as sales 
    FROM ((publishers JOIN titles ON titles.pub_id = publishers.pub_id) 
                      JOIN sales ON titles.title_id = sales.title_id) 
    GROUP BY(pub_name)
```

### *i)* Número total de vendas de cada editora agrupado por título

```
SELECT pub_name, title, COUNT(qty) as sales 
    FROM ((publishers JOIN titles ON titles.pub_id = publishers.pub_id)
                      JOIN sales ON titles.title_id = sales.title_id) 
    GROUP BY pub_name, title
```

### *j)* Nome dos títulos vendidos pela loja ‘Bookbeat’

```
SELECT stor_name, title 
    FROM ((stores JOIN sales ON stores.stor_id = sales.stor_id)
                  JOIN titles ON titles.title_id = sales.title_id)
    WHERE stor_name='Bookbeat'
```

### *k)* Nome de autores que tenham publicações de tipos diferentes

```
SELECT au_fname, au_lname, COUNT(type) as num_types 
  FROM (authors JOIN titleauthor ON titleauthor.au_id = authors.au_id)
             JOIN titles ON titles.title_id = titleauthor.title_id 
  GROUP BY au_fname, au_lname
  HAVING COUNT(type) > 1
```

### *l)* Para os títulos, obter o preço médio e o número total de vendas agrupado por tipo (type) e editora (pub_id)

```
SELECT titles.type, publishers.pub_name, avg(price) AS avg_price, COUNT(qty) AS sales 
 FROM ((titles JOIN sales ON titles.title_id = sales.title_id) 
  JOIN publishers ON publishers.pub_id = titles.pub_id)
 GROUP BY titles.type, publishers.pub_name
```

### *m)* Obter o(s) tipo(s) de título(s) para o(s) qual(is) o máximo de dinheiro “à cabeça” (advance) é uma vez e meia superior à média do grupo (tipo)

```
SELECT [type], max(advance) as max_advance, avg(advance) as avg_advance 
    FROM titles
    GROUP BY [type]
    HAVING (max(advance) > 1.5*avg(advance))
```

### *n)* Obter, para cada título, nome dos autores e valor arrecadado por estes com a sua venda

```
SELECT DISTINCT title, au_fname, au_lname, sum(qty)*price*royalty*royaltyper/10000 as sales
FROM titles JOIN sales ON titles.title_id=sales.title_id 
    JOIN titleauthor ON titles.title_id = titleauthor.title_id
     JOIN authors ON titleauthor.au_id = authors.au_id
GROUP BY title, au_fname, au_lname, price, royalty, royaltyper
```

### *o)* Obter uma lista que incluía o número de vendas de um título (ytd_sales), o seu nome, a faturação total, o valor da faturação relativa aos autores e o valor da faturação relativa à editora

```
SELECT title, ytd_sales, 
    price*ytd_sales as total_revenue, 
    price*ytd_sales*(100-royalty)/100 as publisher_revenue,
    price*ytd_sales*royalty/100 as author_revenue
FROM titles 
WHERE ytd_sales IS NOT NULL
```

### *p)* Obter uma lista que incluía o número de vendas de um título (ytd_sales), o seu nome, o nome de cada autor, o valor da faturação de cada autor e o valor da faturação relativa à editora

```
SELECT title, au_fname, au_lname, ytd_sales, 
    price*ytd_sales as total_revenue, 
    price*ytd_sales*(100-royalty)/100 as publisher_revenue,
    (price*ytd_sales*royalty*royaltyper)/10000 as author_revenue
FROM titles JOIN titleauthor ON titles.title_id = titleauthor.title_id
    JOIN authors ON titleauthor.au_id = authors.au_id
WHERE ytd_sales IS NOT NULL
ORDER BY title ASC
```

### *q)* Lista de lojas que venderam pelo menos um exemplar de todos os livros

```
SELECT stor_name
FROM stores JOIN sales ON stores.stor_id=sales.stor_id
   JOIN titles ON sales.title_id=titles.title_id
   GROUP BY stor_name
   HAVING COUNT(title)=(SELECT COUNT(title) FROM titles)
```

### *r)* Lista de lojas que venderam mais livros do que a média de todas as lojas

```
SELECT stor_name, SUM(qty) as num_books, (SELECT AVG(qty) from sales) as avg_books
FROM stores JOIN sales ON stores.stor_id = sales.stor_id
   JOIN titles ON sales.title_id = titles.title_id
   GROUP BY stor_name
   HAVING SUM(qty) > (SELECT AVG(qty) from sales)
```

### *s)* Nome dos títulos que nunca foram vendidos na loja “Bookbeat”

```
SELECT title
FROM titles
WHERE title NOT IN (
  SELECT title
  FROM titles JOIN sales ON titles.title_id = sales.title_id
     JOIN stores ON sales.stor_id = sales.stor_id
   AND stores.stor_name = 'Bookbeat'
)
```

### *t)* Para cada editora, a lista de todas as lojas que nunca venderam títulos dessa editora

```
SELECT publishers.pub_name, stores.stor_name
	FROM stores, publishers
	EXCEPT SELECT pub_name, stor_name
				FROM publishers JOIN 
					(SELECT pub_id, sales.stor_id, stor_name
						FROM titles JOIN sales ON titles.title_id=sales.title_id
									JOIN stores ON sales.stor_id=stores.stor_id) AS T on publishers.pub_id=T.pub_id
```

## Problema 6.2

### ​5.1

#### a) SQL DDL Script

[a) SQL DDL File](ex_6_2_1_ddl.sql "SQLFileQuestion")

#### b) Data Insertion Script

[b) SQL Data Insertion File](ex_6_2_1_data.sql "SQLFileQuestion")

#### c) Queries

##### *a)*

```
SELECT Ssn, Fname, Minit, Lname, Pname FROM Employee Join Works_on ON Employee.Ssn = Works_on.Essn Join Project ON Works_on.Pno = Project.Pnumber;
```

##### *b)*

```
SELECT Employees.Fname, Employees.Lname, Employees.Super_ssn 
FROM Employee AS Employees 
JOIN Employee AS Carlos_ssn ON Employees.Super_ssn = Carlos_ssn.Ssn 
WHERE Carlos_ssn.Fname = 'Carlos' AND Carlos_ssn.Lname = 'Gomes';

```

##### *c)*

```
SELECT Pnumber, Pname, SUM(Hours) AS TotalHours FROM Project
JOIN Works_on ON Project.Pnumber = Works_on.Pno
GROUP BY Pnumber, Pname;
```

##### *d)*

```
SELECT Fname, Lname FROM Employee
JOIN Works_on ON Employee.Ssn = Works_on.Essn
WHERE Dno = 3 AND Hours > 20;
```

##### *e)*

```
SELECT Fname, Lname FROM Employee
LEFT JOIN Works_on ON Employee.Ssn= Works_on.Essn
WHERE Hours IS NULL;
```

##### *f)*

```
SELECT Dname, AVG(Salary) AS SalaryAvg FROM Employee
JOIN Department ON Employee.Dno = Department.Dnumber
WHERE Sex = 'F'
GROUP BY Dname; 
```

##### *g)*

```
SELECT Fname, Lname FROM (
 SELECT Fname, Lname, COUNT(Essn) AS Count_Dep FROM Employee
 JOIN Dependent ON Employee.Ssn = Dependent.Essn
 GROUP BY Fname, Lname
) AS Dep_Counts
WHERE Count_Dep > 2;
```

##### *h)*

```
SELECT Emp_Dept.*, Dependent.*
FROM (
    SELECT Employee.*, Department.*
    FROM Employee
    JOIN Department ON Employee.Ssn = Department.Mgr_ssn
) AS Emp_Dept
LEFT JOIN Dependent ON Emp_Dept.Ssn = Dependent.Essn
WHERE Dependent.Essn IS NULL;

```

##### *i)*

```
SELECT DISTINCT Fname, Lname, Address FROM Employee
JOIN Department ON Employee.Dno = Department.Dnumber
JOIN Dept_locations ON Department.Dnumber = Dept_locations.Dnumber
JOIN Project ON Department.Dnumber = Project.Dnum
WHERE Dlocation != 'Aveiro' AND Plocation = 'Aveiro';
```

### 5.2

#### a) SQL DDL Script

[a) SQL DDL File](ex_6_2_2_ddl.sql "SQLFileQuestion")

#### b) Data Insertion Script

[b) SQL Data Insertion File](ex_6_2_2_data.sql "SQLFileQuestion")

#### c) Queries

##### *a)*

```
SELECT nome
 FROM fornecedor LEFT outer JOIN encomenda ON fornecedor.nif=encomenda.fornecedor
 WHERE numero IS NULL
```

##### *b)*

```
SELECT nome, AVG(I.unidades) AS MediaProd
 FROM item AS I
  JOIN produto ON I.codProd=produto.codigo
 GROUP BY codProd, nome
```

##### *c)*

```
SELECT AVG(I.NumProdEnc) AS AverageTable
 FROM (
  SELECT numEnc, COUNT(codProd) AS NumProdEnc
  FROM item
  GROUP BY numEnc
 ) AS I
```

##### *d)*

```
SELECT produto.nome, COUNT(codProd) AS NumProdutos
 FROM item JOIN produto ON item.codProd=produto.codigo
      JOIN encomenda ON item.numEnc=encomenda.numero
      JOIN fornecedor ON encomenda.fornecedor=fornecedor.nif
 GROUP BY produto.nome
```

### 5.3

#### a) SQL DDL Script

[a) SQL DDL File](ex_6_2_3_ddl.sql "SQLFileQuestion")

#### b) Data Insertion Script

[b) SQL Data Insertion File](ex_6_2_3_data.sql "SQLFileQuestion")

#### c) Queries

##### *a)*

```
SELECT nome, paciente.numUtente
  FROM prescricao RIGHT OUTER JOIN paciente
          ON prescricao.numUtente=paciente.numUtente
  WHERE prescricao.numPresc IS NULL
```

##### *b)*

```
SELECT especialidade, COUNT(numPresc) AS num_presc
  FROM medico JOIN prescricao
        ON medico.numSNS = prescricao.numMedico
  GROUP BY especialidade
```

##### *c)*

```
SELECT nome, endereco, COUNT(numPresc) AS num_presc
  FROM farmacia JOIN prescricao
         ON farmacia.nome = prescricao.farmacia
  GROUP BY nome, endereco
```

##### *d)*

```
SELECT nome
  FROM farmaco 
  WHERE numRegFarm=906 EXCEPT
  SELECT nomeFarmaco
  FROM presc_farmaco
  WHERE numRegFarm=906
```

##### *e)*

```
SELECT farmacia.nome, farmaceutica.nome, COUNT(presc_farmaco.nomeFarmaco) AS numFarmacosVendidos
 FROM presc_farmaco JOIN farmaceutica ON presc_farmaco.numRegFarm=farmaceutica.numReg
           JOIN prescricao ON presc_farmaco.numPresc = prescricao.numPresc
                     JOIN farmacia ON prescricao.farmacia = farmacia.nome
 GROUP BY farmacia.nome, farmaceutica.nome

```

##### *f)*

```
SELECT P.numUtente, nome
 FROM paciente as P
  JOIN (SELECT numUtente, COUNT(numMedico) AS medico_num
     FROM prescricao
     GROUP BY numUtente) AS T
  ON P.numUtente=T.numUtente
 WHERE medico_num > 1
```
