CREATE DATABASE Rentacar;
GO
USE Rentacar;
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
    data_insc           VARCHAR NOT NULL,
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