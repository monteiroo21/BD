CREATE DATABASE DELIVERYCOMPANY;
GO
USE DELIVERYCOMPANY;
GO

CREATE TABLE TipoFornecedor (
    cod_interno INT NOT NULL,
    designacao VARCHAR NOT NULL,

    PRIMARY KEY(cod_interno)
);

CREATE TABLE Fornecedor (
    nif INT NOT NULL,
    nome VARCHAR NOT NULL,
    endereco VARCHAR,
    fax INT,
    condicoes_pagamento VARCHAR NOT NULL,
    codigo_interno INT NOT NULL,

    PRIMARY KEY(nif),
    FOREIGN KEY(codigo_interno) REFERENCES TipoFornecedor(cod_interno),
    UNIQUE(nome, endereco, fax)
);

CREATE TABLE Encomenda (
    num_encomenda INT NOT NULL,
    data_entrega DATE NOT NULL,
    fornecedor_nif INT NOT NULL,

    PRIMARY KEY(num_encomenda),
    FOREIGN KEY(fornecedor_nif) REFERENCES Fornecedor(nif)
);

CREATE TABLE Produto (
    codigo_produto INT NOT NULL,
    nome VARCHAR NOT NULL,
    preco INT NOT NULL,
    IVA INT,

    PRIMARY KEY(codigo_produto),
    CHECK(IVA >= 0 AND IVA <= 100),
    CHECK(preco > 0)
);

CREATE TABLE Contem (
    num_de_unidades_armazem INT,
    num_encomenda INT NOT NULL,
    codigo_produto INT NOT NULL,

    PRIMARY KEY(num_de_unidades_armazem, num_encomenda, codigo_produto),
    FOREIGN KEY(num_encomenda) REFERENCES Encomenda(num_encomenda),
    FOREIGN KEY(codigo_produto) REFERENCES Produto(codigo_produto)
);

