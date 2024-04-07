CREATE DATABASE GestStock;
GO
USE GestStock;
GO

CREATE TABLE Tipo_fornecedor (
    codigo INT NOT NULL,
    designacao VARCHAR(50) NOT NULL,

    PRIMARY KEY (codigo)
);

CREATE TABLE Fornecedor (
    nif INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    fax INT,
    endereco VARCHAR(50),
    condpag INT NOT NULL,
    tipo INT NOT NULL,

    PRIMARY KEY (nif),
    FOREIGN KEY (tipo) REFERENCES Tipo_fornecedor(codigo)
);

CREATE TABLE Produto (
    codigo INT NOT NULL,
    nome VARCHAR(50) NOT NULL,
    preco DECIMAL(5, 2) NOT NULL,
    iva INT,
    unidades INT,

    PRIMARY KEY (codigo)
);

CREATE TABLE Encomenda (
    numero INT NOT NULL,
    [data] DATE NOT NULL,
    fornecedor INT NOT NULL,

    PRIMARY KEY (numero),
    FOREIGN KEY (fornecedor) REFERENCES Fornecedor(nif)
);

CREATE TABLE Item (
    numEnc INT NOT NULL,
    codProd INT NOT NULL,
    unidades INT,

    PRIMARY KEY (numEnc, codProd),
    FOREIGN KEY (numEnc) REFERENCES Encomenda(numero),
    FOREIGN KEY (codProd) REFERENCES Produto(codigo)
);


--------------------------------------------------
-- INSERT DATA --
--------------------------------------------------