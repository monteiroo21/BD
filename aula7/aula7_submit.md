# BD: Guião 7


## ​7.2 
 
### *a)*

```
1FN(Primeira forma normal)
Não pode estar na 2FN, porque existem dependências parciais (Nome_Autor -> Afiliacao_Autor).
Não pode estar na 3FN, porque existem dependências transitivas (Tipo_Livro, NoPaginas -> Preco) e (Editor -> Endereco_Editor).
```

### *b)* 

```
2FN: R1 (Titulo_Livro, Nome_Autor, Editor, Tipo_Livro, NoPaginas, Ano_Publicacao, Preco, Endereco_Editor) 
     R2 (Nome_Autor, Afiliacao_Autor)

3FN: R1 (Titulo_Livro, Nome_Autor, Editor, Tipo_Livro, NoPaginas, Ano_Publicacao) 
     R2 (Nome_Autor, Afiliacao_Autor)
     R3 (Tipo_Livro, NoPaginas, Preco)
     R4 (Editor, Endereco_Editor)
```




## ​7.3
 
### *a)*

```
{A, B}
```


### *b)* 

```
R1 = {A, D, E, I, J}
R2 = {B, F, G, H}
R3 = {A, B, C}
```


### *c)* 

```
R1 = {A, D, E}
R2 = {D, I, J}
R3 = {B, F}
R4 = {F, G, H}
R5 = {A, B, C}
```


## ​7.4
 
### *a)*

```
{A, B}
```


### *b)* 

```
R1 = {A, B, C, D}
R2 = {D, E}
```


### *c)* 

```
R1 = {A, B, D}
R2 = {C, A}
R3 = {D, E}
```



## ​7.5
 
### *a)*

```
{A, B}
```

### *b)* 

```
R1 = {A, C, D}
R2 = {A, B, D, E}
```


### *c)* 

```
R1 = {A, C}
R2 = {C, D}
R2 = {A, B, D, E}
```

### *d)* 

```
R1 = {A, C}
R2 = {C, D}
R2 = {A, B, D, E}
```
