# BD: Guião 6

## Problema 6.1

### *a)* Todos os tuplos da tabela autores (authors);

```
SELECT * FROM authors
```

### *b)* O primeiro nome, o último nome e o telefone dos autores;

```
SELECT au_fname, au_lname, phone FROM authors
```

### *c)* Consulta definida em b) mas ordenada pelo primeiro nome (ascendente) e depois o último nome (ascendente); 

```
SELECT au_fname, au_lname, phone FROM authors ORDER BY au_fname, au_lname ASC
```

### *d)* Consulta definida em c) mas renomeando os atributos para (first_name, last_name, telephone); 

```
SELECT au_fname as first_name, au_lname as last_name, phone as telephone FROM authors ORDER BY first_name, last_name ASC
```

### *e)* Consulta definida em d) mas só os autores da Califórnia (CA) cujo último nome é diferente de ‘Ringer’; 

```
SELECT au_fname as first_name, au_lname as last_name, phone as telephone FROM authors WHERE state = 'CA' AND au_lname != 'Ringer' ORDER BY first_name, last_name ASC
```

### *f)* Todas as editoras (publishers) que tenham ‘Bo’ em qualquer parte do nome; 

```
SELECT * FROM publishers WHERE pub_name LIKE '%Bo%'
```

### *g)* Nome das editoras que têm pelo menos uma publicação do tipo ‘Business’; 

```
SELECT DISTINCT pub_name FROM publishers INNER JOIN titles ON publishers.pub_id = titles.pub_id WHERE [type] = 'business'
```

### *h)* Número total de vendas de cada editora; 

```
SELECT pub_name, COUNT(qty) as sales FROM ((publishers INNER JOIN titles ON titles.pub_id = publishers.pub_id) INNER JOIN sales
	ON titles.title_id = sales.title_id) GROUP BY(pub_name)
```

### *i)* Número total de vendas de cada editora agrupado por título; 

```
SELECT pub_name, title, COUNT(qty) as sales FROM ((publishers INNER JOIN titles ON titles.pub_id = publishers.pub_id) INNER JOIN sales
	ON titles.title_id = sales.title_id) GROUP BY pub_name, title
```

### *j)* Nome dos títulos vendidos pela loja ‘Bookbeat’; 

```
SELECT stor_name, title FROM ((stores INNER JOIN sales ON stores.stor_id = sales.stor_id) INNER JOIN titles
	ON titles.title_id = sales.title_id) WHERE stor_name='Bookbeat'
```

### *k)* Nome de autores que tenham publicações de tipos diferentes; 

```
SELECT au_fname, au_lname, COUNT(type) as num_types 
		FROM (authors JOIN titleauthor ON titleauthor.au_id = authors.au_id)
			JOIN titles ON titles.title_id = titleauthor.title_id 
		GROUP BY au_fname, au_lname
		HAVING COUNT(type) > 1
```

### *l)* Para os títulos, obter o preço médio e o número total de vendas agrupado por tipo (type) e editora (pub_id);

```
SELECT titles.type, publishers.pub_name, avg(price) AS avg_price, COUNT(qty) AS sales 
	FROM ((titles JOIN sales ON titles.title_id = sales.title_id) 
		JOIN publishers ON publishers.pub_id = titles.pub_id)
	GROUP BY titles.type, publishers.pub_name
```

### *m)* Obter o(s) tipo(s) de título(s) para o(s) qual(is) o máximo de dinheiro “à cabeça” (advance) é uma vez e meia superior à média do grupo (tipo);

```
SELECT [type], max(advance) as max_advance, avg(advance) as avg_advance 
FROM titles
GROUP BY [type]
HAVING (max(advance) > 1.5*avg(advance))
```

### *n)* Obter, para cada título, nome dos autores e valor arrecadado por estes com a sua venda;

```
SELECT DISTINCT title, au_fname, au_lname, sum(qty)*price as sales
FROM titles JOIN sales ON titles.title_id=sales.title_id 
				JOIN titleauthor ON titles.title_id = titleauthor.title_id
					JOIN authors ON titleauthor.au_id = authors.au_id
GROUP BY title, au_fname, au_lname, price
```

### *o)* Obter uma lista que incluía o número de vendas de um título (ytd_sales), o seu nome, a faturação total, o valor da faturação relativa aos autores e o valor da faturação relativa à editora;

```
SELECT title, ytd_sales, 
    price*ytd_sales as total_revenue, 
    price*ytd_sales*(100-royalty)/100 as publisher_revenue,
    price*ytd_sales*royalty/100 as author_revenue
FROM titles 
WHERE ytd_sales IS NOT NULL
```

### *p)* Obter uma lista que incluía o número de vendas de um título (ytd_sales), o seu nome, o nome de cada autor, o valor da faturação de cada autor e o valor da faturação relativa à editora;

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

### *q)* Lista de lojas que venderam pelo menos um exemplar de todos os livros;

```
... Write here your answer ...
```

### *r)* Lista de lojas que venderam mais livros do que a média de todas as lojas;

```
SELECT stor_name, SUM(qty) as num_books, (SELECT AVG(qty) from sales) as avg_books
FROM stores JOIN sales ON stores.stor_id = sales.stor_id
			JOIN titles ON sales.title_id = titles.title_id
			GROUP BY stor_name
			HAVING SUM(qty) > (SELECT AVG(qty) from sales)
```

### *s)* Nome dos títulos que nunca foram vendidos na loja “Bookbeat”;

```
SELECT title
FROM titles
WHERE title NOT IN (
		SELECT title
		FROM titles JOIN sales ON titles.title_id = sales.title_id
					JOIN stores ON sales.stor_id = sales.stor_id
			AND stores.stor_name = 'Bookbeat'
);
```

### *t)* Para cada editora, a lista de todas as lojas que nunca venderam títulos dessa editora; 

```
... Write here your answer ...
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
... Write here your answer ...
```

##### *b)* 

```
... Write here your answer ...
```

##### *c)* 

```
... Write here your answer ...
```

##### *d)* 

```
... Write here your answer ...
```

##### *e)* 

```
... Write here your answer ...
```

##### *f)* 

```
... Write here your answer ...
```

##### *g)* 

```
... Write here your answer ...
```

##### *h)* 

```
... Write here your answer ...
```

##### *i)* 

```
... Write here your answer ...
```

### 5.2

#### a) SQL DDL Script
 
[a) SQL DDL File](ex_6_2_2_ddl.sql "SQLFileQuestion")

#### b) Data Insertion Script

[b) SQL Data Insertion File](ex_6_2_2_data.sql "SQLFileQuestion")

#### c) Queries

##### *a)*

```
... Write here your answer ...
```

##### *b)* 

```
... Write here your answer ...
```


##### *c)* 

```
... Write here your answer ...
```


##### *d)* 

```
... Write here your answer ...
```

### 5.3

#### a) SQL DDL Script
 
[a) SQL DDL File](ex_6_2_3_ddl.sql "SQLFileQuestion")

#### b) Data Insertion Script

[b) SQL Data Insertion File](ex_6_2_3_data.sql "SQLFileQuestion")

#### c) Queries

##### *a)*

```
... Write here your answer ...
```

##### *b)* 

```
... Write here your answer ...
```


##### *c)* 

```
... Write here your answer ...
```


##### *d)* 

```
... Write here your answer ...
```

##### *e)* 

```
... Write here your answer ...
```

##### *f)* 

```
... Write here your answer ...
```
