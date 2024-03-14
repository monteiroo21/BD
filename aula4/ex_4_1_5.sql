CREATE DATABASE GestaoConferencias;
GO
USE GestaoConferencias;
GO
CREATE TABLE Instituição (
    nome                VARCHAR NOT NULL,
    [address]           VARCHAR,

    PRIMARY KEY(nome),
    UNIQUE([address])
);

CREATE TABLE Participantes (
    nome                VARCHAR NOT NULL,
    [address]           VARCHAR,
    end_email           VARCHAR,
    data_insc           DATE NOT NULL,
    nome_inst           VARCHAR

    PRIMARY KEY(nome),
    FOREIGN KEY(nome_inst) REFERENCES Instituição(nome)
);

CREATE TABLE Não_Estudante (
    nome                VARCHAR NOT NULL,
    ref_bancária        INT NOT NULL,

    PRIMARY KEY(nome),
    FOREIGN KEY(nome) REFERENCES Participantes(nome)
);

CREATE TABLE Estudante (
    nome                VARCHAR NOT NULL,
    comprovativo        VARCHAR NOT NULL,

    PRIMARY KEY(nome),
    FOREIGN KEY(nome) REFERENCES Participantes(nome)
);

CREATE TABLE Autores (
    nome                VARCHAR NOT NULL,
    end_email           VARCHAR,
    nome_inst           VARCHAR,

    PRIMARY KEY(nome),
    FOREIGN KEY(nome_inst) REFERENCES Instituição(nome)
);

CREATE TABLE Artigos (
    num_registo         INT NOT NULL,
    título              VARCHAR NOT NULL,
    nome_autor          VARCHAR NOT NULL,

    PRIMARY KEY(num_registo),
    FOREIGN KEY(nome_autor) REFERENCES Autores(nome)
);

CREATE TABLE Têm (
    num_registo_artigo  INT NOT NULL,
    nome_autor			VARCHAR NOT NULL,

    PRIMARY KEY(num_registo_artigo, nome_autor),
    FOREIGN KEY(num_registo_artigo) REFERENCES Artigos(num_registo),
    FOREIGN KEY(nome_autor) REFERENCES Autores(nome)
);