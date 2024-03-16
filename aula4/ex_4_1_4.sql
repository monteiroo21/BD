CREATE DATABASE MEDICINES;
GO
USE MEDICINES;
GO

CREATE TABLE Medico (
    num_identificacao INT NOT NULL,
    nome VARCHAR NOT NULL,
    especialidade VARCHAR,

    PRIMARY KEY(num_identificacao),
    UNIQUE(nome)
);

CREATE TABLE Paciente (
    medico_num_identificacao INT NOT NULL,
    num_utente INT NOT NULL,
    nome VARCHAR NOT NULL,
    endereco VARCHAR NOT NULL,
    data_nascimento DATE NOT NULL,

    PRIMARY KEY(num_utente),
    FOREIGN KEY(medico_num_identificacao) REFERENCES Medico(num_identificacao),
    UNIQUE(nome, data_nascimento)
);

CREATE TABLE Farmacia (
    nome VARCHAR NOT NULL,
    nif INT NOT NULL,
    endereco VARCHAR,
    telefone INT,

    PRIMARY KEY(nif),
    UNIQUE(nome, endereco)
);

CREATE TABLE Farmaceutica (
    nome VARCHAR NOT NULL,
    num_registo INT NOT NULL,
    endereco VARCHAR,
    telefone INT,

    PRIMARY KEY(num_registo),
    UNIQUE(nome, endereco, telefone)
);

CREATE TABLE Farmaco (
    nome_comercial VARCHAR NOT NULL,
    formula VARCHAR NOT NULL,
    farmaceutica_num_registo INT NOT NULL,

    PRIMARY KEY(nome_comercial, farmaceutica_num_registo),
    FOREIGN KEY(farmaceutica_num_registo) REFERENCES Farmaceutica(num_registo)
);

CREATE TABLE Prescricao (
    num_prescricao INT NOT NULL,
    [data] DATE NOT NULL,
    medico_num_identificacao INT NOT NULL,
    paciente_num_utente INT NOT NULL,
    farmacia_nif INT NOT NULL,

    PRIMARY KEY(num_prescricao),
    FOREIGN KEY(medico_num_identificacao) REFERENCES Medico(num_identificacao),
    FOREIGN KEY(paciente_num_utente) REFERENCES Paciente(num_utente),
    FOREIGN KEY(farmacia_nif) REFERENCES Farmacia(nif)
);

CREATE TABLE Vai (
    num_utente INT NOT NULL,
    farmacia_nif INT NOT NULL,

    PRIMARY KEY(num_utente, farmacia_nif),
    FOREIGN KEY(num_utente) REFERENCES Paciente(num_utente),
    FOREIGN KEY(farmacia_nif) REFERENCES Farmacia(nif)
);

CREATE TABLE Contem (
    num_prescricao INT NOT NULL,
    nome_comercial VARCHAR NOT NULL,
    farmaceutica_num_registo INT NOT NULL,

    PRIMARY KEY(num_prescricao, nome_comercial, farmaceutica_num_registo),
    FOREIGN KEY(num_prescricao) REFERENCES Prescricao(num_prescricao),
    FOREIGN KEY(nome_comercial, farmaceutica_num_registo) REFERENCES Farmaco(nome_comercial, farmaceutica_num_registo)
);

CREATE TABLE Vendidos (
    farmacia_nif INT NOT NULL,
    nome_comercial VARCHAR NOT NULL,
    farmaceutica_num_registo INT NOT NULL,

    PRIMARY KEY(farmacia_nif, nome_comercial, farmaceutica_num_registo),
    FOREIGN KEY(farmacia_nif) REFERENCES Farmacia(nif),
    FOREIGN KEY(nome_comercial, farmaceutica_num_registo) REFERENCES Farmaco(nome_comercial, farmaceutica_num_registo)
);