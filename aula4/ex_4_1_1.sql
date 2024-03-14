CREATE DATABASE Rentacar;
GO
USE Rentacar;
GO
CREATE TABLE Cliente (
    nif             INT NOT NULL,
    nome            VARCHAR NOT NULL,
    endereço        VARCHAR,
    num_carta       INT NOT NULL,

    PRIMARY KEY(nif),
    UNIQUE(num_carta)
);

CREATE TABLE Balcão (
    numero          INT NOT NULL,
    nome            VARCHAR NOT NULL,
    endereco        VARCHAR,

    PRIMARY KEY(numero)
);

CREATE TABLE Veículo (
    matrícula       VARCHAR NOT NULL,
    marca           VARCHAR,
    ano             INT NOT NULL

    PRIMARY KEY(matrícula)
);

CREATE TABLE Aluguer (
    numero              INT NOT NULL,
    duração             INT NOT NULL,
    [data]              VARCHAR(10) NOT NULL,
    nif_cliente         INT NOT NULL,
    num_balcão          INT NOT NULL,
    matricula_veiculo   VARCHAR NOT NULL,

    PRIMARY KEY(numero),
    FOREIGN KEY(nif_cliente) REFERENCES Cliente(nif),
    FOREIGN KEY(num_balcão) REFERENCES Balcão(numero),
    FOREIGN KEY(matricula_veiculo) REFERENCES Veículo(matrícula)
);

CREATE TABLE Tipo_Veículo (
    código              VARCHAR NOT NULL,
    designação          VARCHAR,
    ar_condicionado     BIT,

    PRIMARY KEY(código)
);

CREATE TABLE Similaridade (
    cod_veic_1          VARCHAR NOT NULL,
    cod_veic_2          VARCHAR NOT NULL,

    PRIMARY KEY(cod_veic_1,cod_veic_2),
    FOREIGN KEY(cod_veic_1) REFERENCES Tipo_Veículo(código),
    FOREIGN KEY(cod_veic_2) REFERENCES Tipo_Veículo(código)
);

CREATE TABLE Ligeiro (
    cod_veic            VARCHAR NOT NULL,
    combustível         VARCHAR,
    portas              INT,
    numLugares          INT,

    PRIMARY KEY(cod_veic),
    FOREIGN KEY(cod_veic) REFERENCES Tipo_Veículo(código)
);

CREATE TABLE Pesado (
    cod_veic            VARCHAR NOT NULL,
    peso                INT,
    passageiros         INT,

    PRIMARY KEY(cod_veic),
    FOREIGN KEY(cod_veic) REFERENCES Tipo_Veículo(código)
);