CREATE DATABASE MusicScore;
GO
USE MusicScore;
GO
CREATE TABLE Instrumentation (
    instrument      VARCHAR NOT NULL,
    quantity        INT,
    family          VARCHAR,
    [role]          VARCHAR,

    PRIMARY KEY(instrument),
);

CREATE TABLE MusicalGenre (
    id              INT NOT NULL,
    [name]          VARCHAR NOT NULL,

    PRIMARY KEY(id),
    UNIQUE([name])
);

CREATE TABLE Music (
    music_id        INT NOT NULL,
    title           VARCHAR NOT NULL,
    [year]          INT,
    musGenre_id     INT NOT NULL,
    instrumentation VARCHAR NOT NULL,

    PRIMARY KEY(music_id),
    FOREIGN KEY(musGenre_id) REFERENCES MusicalGenre(id),
    FOREIGN KEY(instrumentation) REFERENCES Instrumentation(instrument)
);

CREATE TABLE Editor (
    identifier          INT NOT NULL,
    [name]              VARCHAR NOT NULL,
    [location]          VARCHAR,

    PRIMARY KEY(identifier),
    UNIQUE([location])
);

CREATE TABLE Score (
    register_num        INT NOT NULL,
    [edition]           INT,
    price               MONEY NOT NULL,
    [availability]      INT NOT NULL,
    difficultyGrade     INT,
    musicId             INT NOT NULL,
    editorId            INT NOT NULL,

    PRIMARY KEY(register_num),
    FOREIGN KEY(musicId) REFERENCES Music(music_id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Warehouse (
    id          INT NOT NULL,
    [name]      VARCHAR,
    storage     INT,
    editorId    INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Customer (
    numCC               INT NOT NULL,
    email_address       VARCHAR,
    numBankAccount      INT NOT NULL,
    cellNumber          INT,
    [name]              VARCHAR NOT NULL,

    PRIMARY KEY(numCC)
);

CREATE TABLE StaffPersonel (
    numCC               INT NOT NULL,
    email_address       VARCHAR NOT NULL,
    employeeId          INT NOT NULL,
    cellNumber          INT,
    [name]              VARCHAR NOT NULL,

    PRIMARY KEY(employeeId),
    UNIQUE(numCC)
);

CREATE TABLE [Transaction] (
    transcation_id          INT NOT NULL,
    [value]                 MONEY NOT NULL,
    [date]                  DATE,
    customer_CC             INT NOT NULL,
    employee_id             INT NOT NULL,

    PRIMARY KEY(transcation_id),
    FOREIGN KEY(customer_CC) REFERENCES Customer(numCC),
    FOREIGN KEY(employee_id) REFERENCES StaffPersonel(employeeId)
);

CREATE TABLE Writer (
    id              INT NOT NULL,
    Fname           VARCHAR NOT NULL,
    Lname           VARCHAR,
    genre           CHAR,
    birthYear       DATE,
    deathYear       DATE,

    PRIMARY KEY(id)
);

CREATE TABLE Arranger (
    id            INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES Writer(id)
);

CREATE TABLE Composer (
    id              INT NOT NULL,
    musGenre_id     INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES Writer(id),
    FOREIGN KEY(musGenre_id) REFERENCES MusicalGenre(id)
);

CREATE TABLE writes (
    music_id            INT NOT NULL,
    writer_id           INT NOT NULL,

    PRIMARY KEY(music_id, writer_id),
    FOREIGN KEY(music_id) REFERENCES Music(music_id),
    FOREIGN KEY(writer_id) REFERENCES Writer(id)
);

CREATE TABLE stores (
    warehouse_id        INT NOT NULL,
    score_register      INT NOT NULL,

    PRIMARY KEY(warehouse_id, score_register),
    FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id),
    FOREIGN KEY(score_register) REFERENCES Score(register_num)
);

CREATE TABLE purchases (
    costumerCC          INT NOT NULL,
    score_register      INT NOT NULL,

    PRIMARY KEY(costumerCC, score_register),
    FOREIGN KEY(costumerCC) REFERENCES Customer(numCC),
    FOREIGN KEY(score_register) REFERENCES Score(register_num)
);

CREATE TABLE warehouse_location (
    warehouse_location  VARCHAR NOT NULL,
    warehouse_id        INT NOT NULL,

    PRIMARY KEY(warehouse_location, warehouse_id),
    FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id)
);