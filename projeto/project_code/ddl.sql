DROP DATABASE IF EXISTS MusicScore;
GO
CREATE DATABASE MusicScore;
GO
USE MusicScore;
GO

CREATE TABLE MusicalGenre
(
    id INT NOT NULL,
    [name] VARCHAR(50) NOT NULL,

    PRIMARY KEY(id),
    UNIQUE([name])
);

CREATE TABLE Music
(
    music_id INT NOT NULL,
    title VARCHAR(80) NOT NULL,
    [year] INT					CHECK([year] > 0 and [year] < 2025),
    musGenre_id INT,

    PRIMARY KEY(music_id),
    FOREIGN KEY(musGenre_id) REFERENCES MusicalGenre(id)
);

CREATE TABLE Editor
(
    identifier INT NOT NULL,
    [name] VARCHAR(50) NOT NULL,
    [location] VARCHAR(50),

    PRIMARY KEY(identifier),
    UNIQUE([location])
);

CREATE TABLE Score
(
    register_num INT NOT NULL,
    [edition] INT,
    price DECIMAL(10, 2),
    [availability] INT,
    difficultyGrade INT		CHECK(difficultyGrade > 0 and difficultyGrade < 6),
    musicId INT NOT NULL,
    editorId INT NOT NULL,

    PRIMARY KEY(register_num),
    FOREIGN KEY(musicId) REFERENCES Music(music_id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Instrumentation
(
    instrument VARCHAR(60) NOT NULL,
    quantity INT,
    family VARCHAR(50),
    [role] VARCHAR(50),
    scoreNum INT NOT NULL,

    PRIMARY KEY(instrument, scoreNum),
    FOREIGN KEY(scoreNum) REFERENCES Score(register_num)
);

CREATE TABLE Warehouse
(
    id INT NOT NULL,
    [name] VARCHAR(80),
    storage INT,
    editorId INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Customer
(
    numCC INT NOT NULL			CHECK(len(numCC) = 8),
    email_address VARCHAR(80),
    numBankAccount INT NOT NULL,
    cellNumber INT				CHECK(len(cellNumber) = 9),
    [name] VARCHAR(60) NOT NULL,

    PRIMARY KEY(numCC),
    UNIQUE(numBankAccount)
);

CREATE TABLE [Transaction]
(
    transaction_id INT NOT NULL,
    [value] DECIMAL(10, 2) NOT NULL,
    [date] DATE,
    customer_CC INT NOT NULL,

    PRIMARY KEY(transaction_id),
    FOREIGN KEY(customer_CC) REFERENCES Customer(numCC)
);

CREATE TABLE Writer
(
    id INT NOT NULL,
    Fname VARCHAR(60) NOT NULL,
    Lname VARCHAR(60),
    genre VARCHAR(1)	CHECK(genre = 'F' or genre = 'M'),
    birthYear INT NOT NULL		CHECK(birthYear > 0 and birthYear < 2025),
    deathYear INT		        CHECK(deathYear IS NULL OR (deathYear > 0 and deathYear < 2025)),
    musGenre_id INT,

	CHECK(deathYear IS NULL OR deathYear > birthYear),
    PRIMARY KEY(id),
    FOREIGN KEY(musGenre_id) REFERENCES MusicalGenre(id)
);

CREATE TABLE Arranger
(
    id INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES Writer(id)
);

CREATE TABLE Composer
(
    id INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(id) REFERENCES Writer(id)
);

CREATE TABLE writes
(
    music_id INT NOT NULL,
    composer_id INT NOT NULL,

    PRIMARY KEY(music_id, composer_id),
    FOREIGN KEY(music_id) REFERENCES Music(music_id),
    FOREIGN KEY(composer_id) REFERENCES Composer(id)
);

CREATE TABLE arranges
(
    score_register INT NOT NULL,
    arranger_id INT NOT NULL,
    [type] VARCHAR(60),

    PRIMARY KEY(score_register, arranger_id),
    FOREIGN KEY(score_register) REFERENCES Score(register_num),
    FOREIGN KEY(arranger_id) REFERENCES Arranger(id)
)

CREATE TABLE stores
(
    warehouse_id INT NOT NULL,
    score_register INT NOT NULL,

    PRIMARY KEY(warehouse_id, score_register),
    FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id),
    FOREIGN KEY(score_register) REFERENCES Score(register_num)
);

CREATE TABLE purchases
(
    costumerCC INT NOT NULL,
    score_register INT NOT NULL,

    PRIMARY KEY(costumerCC, score_register),
    FOREIGN KEY(costumerCC) REFERENCES Customer(numCC),
    FOREIGN KEY(score_register) REFERENCES Score(register_num)
);

CREATE TABLE warehouse_location
(
    warehouse_location VARCHAR(80) NOT NULL,
    warehouse_id INT NOT NULL,

    PRIMARY KEY(warehouse_location, warehouse_id),
    FOREIGN KEY(warehouse_id) REFERENCES Warehouse(id)
);

CREATE TABLE constitutes
(
    score_register INT NOT NULL,
    transaction_id INT NOT NULL,

    PRIMARY KEY(score_register, transaction_id),
    FOREIGN KEY(score_register) REFERENCES Score(register_num),
    FOREIGN KEY(transaction_id) REFERENCES [Transaction](transaction_id)
)