CREATE DATABASE MusicScore;
GO
USE MusicScore;
GO

CREATE TABLE MusicalGenre
(
    id INT NOT NULL,
    [name] VARCHAR NOT NULL,

    PRIMARY KEY(id),
    UNIQUE([name])
);

CREATE TABLE Music
(
    music_id INT NOT NULL,
    title VARCHAR NOT NULL,
    [year] INT,
    musGenre_id INT,

    PRIMARY KEY(music_id),
    FOREIGN KEY(musGenre_id) REFERENCES MusicalGenre(id)
);

CREATE TABLE Editor
(
    identifier INT NOT NULL,
    [name] VARCHAR NOT NULL,
    [location] VARCHAR,

    PRIMARY KEY(identifier),
    UNIQUE([location])
);

CREATE TABLE Score
(
    register_num INT NOT NULL,
    [edition] INT,
    price MONEY,
    [availability] INT,
    difficultyGrade INT,
    musicId INT NOT NULL,
    editorId INT,

    PRIMARY KEY(register_num),
    FOREIGN KEY(musicId) REFERENCES Music(music_id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Instrumentation
(
    instrument VARCHAR NOT NULL,
    quantity INT,
    family VARCHAR,
    [role] VARCHAR,
    scoreNum INT NOT NULL,

    PRIMARY KEY(instrument),
    FOREIGN KEY(scoreNum) REFERENCES Score(register_num)
);

CREATE TABLE Warehouse
(
    id INT NOT NULL,
    [name] VARCHAR,
    storage INT,
    editorId INT NOT NULL,

    PRIMARY KEY(id),
    FOREIGN KEY(editorId) REFERENCES Editor(identifier)
);

CREATE TABLE Customer
(
    numCC INT NOT NULL,
    email_address VARCHAR,
    numBankAccount INT NOT NULL,
    cellNumber INT,
    [name] VARCHAR NOT NULL,

    PRIMARY KEY(numCC),
    UNIQUE(numBankAccount)
);

CREATE TABLE [Transaction]
(
    transaction_id INT NOT NULL,
    [value] MONEY NOT NULL,
    [date] DATE,
    customer_CC INT NOT NULL,

    PRIMARY KEY(transaction_id),
    FOREIGN KEY(customer_CC) REFERENCES Customer(numCC)
);

CREATE TABLE Writer
(
    id INT NOT NULL,
    Fname VARCHAR NOT NULL,
    Lname VARCHAR,
    genre CHAR,
    birthYear DATE,
    deathYear DATE,
    musGenre_id INT,

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
    [type] VARCHAR,

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
    warehouse_location VARCHAR NOT NULL,
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


INSERT INTO MusicalGenre (id, [name]) VALUES
    (1, 'Classical'),
    (2, 'Jazz'),
    (3, 'Rock'),
    (4, 'Pop'),
    (5, 'Metal'),
    (6, 'Blues'),
    (7, 'Folk'),
    (8, 'Country'),
    (9, 'Reggae'),
    (10, 'Hip-Hop'),
    (11, 'Electronic'),
    (12, 'Rap'),
    (13, 'R&B'),
    (14, 'Soul'),
    (15, 'Punk'),
    (16, 'Indie'),
    (17, 'Alternative'),
    (18, 'Gospel'),
    (19, 'New Age'),
    (20, 'World'),
    (21, 'Latin'),
    (22, 'Dance'),
    (23, 'Techno'),
    (24, 'House'),
    (25, 'Trance'),
    (26, 'Dubstep'),
    (27, 'Drum and Bass'),
    (28, 'Garage'),
    (29, 'Grime'),
    (30, 'Breakbeat'),
    (31, 'Hardcore'),
    (32, 'Ambient'),
    (33, 'Chillout'),
    (34, 'Downtempo'),
    (35, 'Trip-Hop'),
    (36, 'Jungle'),
    (37, 'Electro'),
    (38, 'Industrial'),
    (39, 'Noise'),
    (40, 'Experimental'),
    (41, 'Acoustic'),
    (42, 'Instrumental'),
    (43, 'Vocal'),
    (44, 'Orchestral'),
    (45, 'Chamber'),
    (46, 'Symphonic'),
    (47, 'Concerto'),
    (48, 'Sonata'),
    (49, 'Suite'),
    (50, 'Opera'),
    (51, 'Operetta'),
    (52, 'Musical'),
    (53, 'Ballet'),
    (54, 'Film'),
    (55, 'TV'),
    (56, 'Video Game'),
    (57, 'Anime'),
    (58, 'Manga'),
    (59, 'Comic'),
    (60, 'Cartoon'),
    (61, 'Children'),
    (62, 'Holiday'),
    (63, 'Christmas'),
    (64, 'Easter'),
    (65, 'Halloween');