# BD: Trabalho Prático APF-T

**Grupo**: PXGY

- Jorge Domingues, MEC: 113278
- João Monteiro, MEC: 114547

# Instructions - TO REMOVE

Este template é flexível.
É sugerido seguir a estrutura, links de ficheiros e imagens, mas adicione ou remova conteúdo sempre que achar necessário.

---

This template is flexible.
It is suggested to follow the structure, file links and images but add more content where necessary.

The files should be organized with the following nomenclature:

- sql\01_ddl.sql: mandatory for DDL
- sql\02_sp_functions.sql: mandatory for Store Procedure, Functions,...
- sql\03_triggers.sql: mandatory for triggers
- sql\04_db_init.sql: scripts to init the database (i.e. inserts etc.)
- sql\05_any_other_matter.sql: any other scripts.

Por favor remova esta secção antes de submeter.

Please remove this section before submitting.

## Introdução / Introduction

Escreva uma pequena introdução sobre o trabalho.
Write a simple introduction about your project.
O trabalho é sobre um sistema de gestão e compra de partituras, onde podem adicionadas, editadas e eliminadas músicas publicadas por escritores.

## ​Análise de Requisitos / Requirements

## DER - Diagrama Entidade Relacionamento/Entity Relationship Diagram

### Versão final/Final version

![DER Diagram!](der.jpg "AnImage")

### APFE

Descreva sumariamente as melhorias sobre a primeira entrega.
Describe briefly the improvements made since the first delivery.
Inicialmente, nós não fizemos uma relação entre a partitura e o arranjador, assim como também entre a instrumentação, que antes estava realcionada com a música original e não com a partitura em si. Também tinhamos associado o escritor à música original, o que depois foi alterado para apenas o compositor original ser relacionado apenas à música original. O que também foi alterado foi a relação do género musical que antes estava associado apenas ao compositor, o que foi alterado para o escritor pois o arranjador também pode ser associado a um genero tambem.

## ER - Esquema Relacional/Relational Schema

### Versão final/Final Version

![ER Diagram!](er.jpg "AnImage")

### APFE

Descreva sumariamente as melhorias sobre a primeira entrega.
Describe briefly the improvements made since the first delivery.

As alterações perante a primeira entrega estão relacionadas com as alterações feitas no DER.

## ​SQL DDL - Data Definition Language

[SQL DDL File](sql/01_ddl.sql "SQLFileQuestion")

## SQL DML - Data Manipulation Language

Uma secção por formulário.
A section for each form.

### Formulario exemplo/Example Form

![Exemplo Screenshot!](screenshots/screenshot_1.jpg "AnImage")

```sql
-- Show data on the form
SELECT * FROM MY_TABLE ....;

-- Insert new element
INSERT INTO MY_TABLE ....;
```

...

## Normalização/Normalization

Descreva os passos utilizados para minimizar a duplicação de dados / redução de espaço.
Justifique as opções tomadas.
Describe the steps used to minimize data duplication / space reduction.
Justify the choices made.

## Índices/Indexes

Descreva os indices criados. Junte uma cópia do SQL de criação do indice.
Describe the indexes created. Attach a copy of the SQL to create the index.

```sql
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_musGenre_id' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_musGenre_id ON Music (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_writes_music_id' AND object_id = OBJECT_ID('writes'))
CREATE INDEX idx_writes_music_id ON writes (music_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_writes_composer_id' AND object_id = OBJECT_ID('writes'))
CREATE INDEX idx_writes_composer_id ON writes (composer_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Composer_id' AND object_id = OBJECT_ID('Composer'))
CREATE INDEX idx_Composer_id ON Composer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Editor_name' AND object_id = OBJECT_ID('Editor'))
CREATE INDEX idx_Editor_name ON Editor ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Editor_identifier' AND object_id = OBJECT_ID('Editor'))
CREATE INDEX idx_Editor_identifier ON Editor (identifier);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Warehouse_editorId' AND object_id = OBJECT_ID('Warehouse'))
CREATE INDEX idx_Warehouse_editorId ON Warehouse (editorId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Warehouse_name' AND object_id = OBJECT_ID('Warehouse'))
CREATE INDEX idx_Warehouse_name ON Warehouse ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Score_musicId' AND object_id = OBJECT_ID('Score'))
CREATE INDEX idx_Score_musicId ON Score (musicId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Score_editorId' AND object_id = OBJECT_ID('Score'))
CREATE INDEX idx_Score_editorId ON Score (editorId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_id' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_id ON Music (music_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_title' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_title ON Music (title);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Composer_id' AND object_id = OBJECT_ID('Composer'))
CREATE INDEX idx_Composer_id ON Composer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_musGenre_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_musGenre_id ON Writer (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Arranger_id' AND object_id = OBJECT_ID('Arranger'))
CREATE INDEX idx_Arranger_id ON Arranger (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_musGenre_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_musGenre_id ON Writer (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);

```

## SQL Programming: Stored Procedures, Triggers, UDF

[SQL SPs and Functions File](sql/02_sp_functions.sql "SQLFileQuestion")

[SQL Triggers File](sql/03_triggers.sql "SQLFileQuestion")

## Outras notas/Other notes

### Dados iniciais da dabase de dados/Database init data

Não sei o que é para colocar aqui!!!!!!!
[Indexes File](sql/01_ddl.sql "SQLFileQuestion")

### Apresentação

[Slides](slides.pdf "Sildes")

[Video](Video.mp4)
