CREATE DATABASE Prescricao;
GO
USE Prescricao;
GO

CREATE TABLE Medico (
    numSNS INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    especialidade VARCHAR(50),

    PRIMARY KEY(numSNS)
);

CREATE TABLE Paciente (
    numUtente INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    dataNasc DATE NOT NULL,
    endereco VARCHAR(50),

    PRIMARY KEY(numUtente)
);

CREATE TABLE Farmacia (
    nome VARCHAR(50) NOT NULL,
    telefone INT,
    endereco VARCHAR(50),

    PRIMARY KEY(nome)
);

CREATE TABLE Farmaceutica (
    numReg INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    endereco VARCHAR(50),

    PRIMARY KEY(numReg)
);

CREATE TABLE Farmaco (
    numRegFarm INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    formula VARCHAR(50) NOT NULL,

    PRIMARY KEY(numRegFarm, nome),
    FOREIGN KEY(numRegFarm) REFERENCES Farmaceutica(numReg)
);

CREATE TABLE Prescricao (
    numPresc INT NOT NULL,
    numUtente INT NOT NULL,
    numMedico INT NOT NULL,
    farmacia VARCHAR(50),
    dataProc DATE,

    PRIMARY KEY(numPresc),
    FOREIGN KEY(numUtente) REFERENCES Paciente(numUtente),
    FOREIGN KEY(numMedico) REFERENCES Medico(numSNS),
    FOREIGN KEY(farmacia) REFERENCES Farmacia(nome)
);

CREATE TABLE Presc_farmaco (
    numPresc INT NOT NULL,
    numRegFarm INT NOT NULL,
    nomeFarmaco VARCHAR(50) NOT NULL,

    PRIMARY KEY(numPresc, numRegFarm, nomeFarmaco),
    FOREIGN KEY(numPresc) REFERENCES Prescricao(numPresc),
    FOREIGN KEY(numRegFarm, nomeFarmaco) REFERENCES Farmaco(numRegFarm, nome)
);


----------------------------------------
-- INSERT DATA HERE --
----------------------------------------