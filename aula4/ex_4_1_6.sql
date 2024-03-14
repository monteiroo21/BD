CREATE DATABASE GestaoATL;
GO
USE GestaoATL;
GO
CREATE TABLE Pessoa (
    num_CC              INT NOT NULL,
    nome                VARCHAR NOT NULL,
    num_telefone        INT,
    end_email           VARCHAR,
    data_nasc           DATE,
    morada              VARCHAR,

    PRIMARY KEY(num_CC)
);

CREATE TABLE Encarregado_Educação (
    num_CC              INT NOT NULL,
    relação             VARCHAR,

    PRIMARY KEY(num_CC),
    FOREIGN KEY(num_CC) REFERENCES Pessoa(num_CC),
    UNIQUE(relação)
);

CREATE TABLE Responsável (
    num_CC              INT NOT NULL,
    relação             VARCHAR,

    PRIMARY KEY(num_CC),
    FOREIGN KEY(num_CC) REFERENCES Pessoa(num_CC),
    UNIQUE(relação)
);

CREATE TABLE Professor (
    num_CC              INT NOT NULL,
    num_funcionario     INT NOT NULL,

    PRIMARY KEY(num_CC),
    FOREIGN KEY(num_CC) REFERENCES Pessoa(num_CC),
    UNIQUE(num_funcionario)
);

CREATE TABLE Turma (
    identificador       INT NOT NULL,
    num_max_alunos      INT NOT NULL,
    designação          VARCHAR,
    ano_letivo          INT NOT NULL,
    num_CCprof          INT NOT NULL,

    PRIMARY KEY(identificador),
    FOREIGN KEY(num_CCprof) REFERENCES Professor(num_CC)
);

CREATE TABLE Atividades (
    identificação       INT NOT NULL,
    custo               MONEY NOT NULL,
    designação          VARCHAR, 

    PRIMARY KEY(identificação),
)

CREATE TABLE Aluno (
    num_CC              INT NOT NULL,
    data_nasc           DATE,
    nome                VARCHAR NOT NULL,
    morada              VARCHAR,
    id_turma            INT NOT NULL,
    numCC_EE            INT NOT NULL,

    PRIMARY KEY(num_CC),
    FOREIGN KEY(id_turma) REFERENCES Turma(identificador),
    FOREIGN KEY(numCC_EE) REFERENCES Encarregado_Educação(num_CC)
);

CREATE TABLE Participa_TA (
    id_turma            INT NOT NULL,
    id_atividades       INT NOT NULL,

    PRIMARY KEY(id_turma, id_atividades),
    FOREIGN KEY(id_turma) REFERENCES Turma(identificador),
    FOREIGN KEY(id_atividades) REFERENCES Atividades(identificação)
);

CREATE TABLE Participa_AA (
    id_atividades            INT NOT NULL,
    num_CCalunos             INT NOT NULL,

    PRIMARY KEY(num_CCalunos, id_atividades),
    FOREIGN KEY(num_CCalunos) REFERENCES Aluno(num_CC),
    FOREIGN KEY(id_atividades) REFERENCES Atividades(identificação)
);