CREATE DATABASE Rentacar;
GO
USE Rentacar;
GO
CREATE TABLE Participantes (
    nome                VARCHAR NOT NULL,
    [address]           VARCHAR,
    end_email           VARCHAR,
    data_insc           VARCHAR NOT NULL,
    nome_inst           VARCHAR
);
