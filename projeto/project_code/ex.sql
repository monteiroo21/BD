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
    [year] INT,
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
    difficultyGrade INT,
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

    PRIMARY KEY(instrument),
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
    numCC INT NOT NULL,
    email_address VARCHAR(80),
    numBankAccount INT NOT NULL,
    cellNumber INT,
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
    genre VARCHAR(1),
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


INSERT INTO MusicalGenre (id, [name]) VALUES
    (1, 'Classical'),
    (2, 'Jazz'),
    (3, 'Pop'),
    (4, 'Rock'),
    (5, 'Orchestra'),
    (6, 'Band'),
    (7, 'Big Band'),
    (8, 'Chamber'),
    (9, 'Choral'),
    (10, 'Concert Band'),
    (11, 'Marching Band'),
    (12, 'Jazz Band'),
    (13, 'Wind Band'),
    (14, 'Brass Band'),
    (15, 'String Orchestra'),
    (16, 'Symphony Orchestra'),
    (17, 'String Quartet'),
    (18, 'Wind Quintet'),
    (19, 'Brass Quintet'),
    (20, 'Percussion Ensemble'),
    (21, 'Choir'),
    (22, 'Children''s Choir'),
    (23, 'Mixed Choir'),
    (24, 'Blues'),
    (25, 'Electronic'),
    (26, 'Symphonic'),
    (27, 'Romantic'),
    (28, 'Medieval'),
    (29, 'Baroque'),
    (30, 'Renaissance'),
    (31, 'Contemporary');


INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (1, 'Moonlight Sonata', 1801, 1),
    (2, 'Fur Elise', 1810, 1),
    (3, 'Symphony No. 9', 1824, 1);

-- Classical
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (4, 'Symphony No. 5', 1808, 1),
    (5, 'Four Seasons', 1725, 29),
    (6, 'Canon in D', 1680, 29),
    (7, 'Swan Lake', 1876, 27),
    (8, 'Magic Flute', 1791, 1);

    
-- Jazz
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (9, 'So What', 1959, 2),
    (10, 'Giant Steps', 1960, 2),
    (11, 'A Love Supreme', 1965, 2),
    (12, 'Freddie Freeloader', 1959, 2),
    (13, 'Blue Rondo à la Turk', 1959, 2);

-- Pop
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (14, 'Thriller', 1982, 3),
    (15, 'Like a Virgin', 1984, 3),
    (16, 'Billie Jean', 1982, 3),
    (17, 'I Wanna Dance with Somebody', 1987, 3),
    (18, 'Poker Face', 2008, 3);

-- Rock
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (19, 'Back In Black', 1980, 4),
    (20, 'Smoke on the Water', 1972, 4),
    (21, 'Hotel California', 1977, 4),
    (22, 'Stairway to Heaven', 1971, 4),
    (23, 'Imagine', 1971, 4);

-- Orchestra
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (25, 'Bolero', 1928, 31),
    (26, 'The Nutcracker Suite', 1892, 27),
    (27, 'Rite of Spring', 1913, 31),
    (28, 'Carmen Suite', 1875, 27);

-- Additional genres with unique and overlapping titles
-- Jazz Band
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (29, 'Birdland', 1977, 12),
    (30, 'Moanin', 1959, 12),
    (31, 'The Chicken', 1980, 12),
    (32, 'Sing, Sing, Sing', 1936, 12),
    (33, 'A Night in Tunisia', 1942, 12);

-- Choir
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (34, 'Carmina Burana', 1936, 21),
    (35, 'Messiah', 1741, 21),
    (36, 'Requiem', 1791, 21),
    (37, 'The Creation', 1798, 21),
    (38, 'A Ceremony of Carols', 1942, 21);

-- Symphonic
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (39, 'New World Symphony', 1893, 27),
    (40, 'Symphony of the Air', 1954, 31),
    (41, 'Enigma Variations', 1899, 27),
    (42, 'Symphony No. 7', 1813, 1);

-- Baroque
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (43, 'Canon in D major', 1690, 29),
    (44, 'Messiah', 1741, 29),
    (45, 'Brandenburg Concerto No. 3', 1721, 29),
    (46, 'Water Music', 1717, 29);

-- Medieval
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (47, 'Palästinalied', 1228, 28),
    (48, 'Cantiga 166', 1270, 28),
    (49, 'Sumer is icumen in', 1260, 28),
    (50, 'Le homme armé', 1450, 28);

--Renaissence
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (51, 'Missa Papae Marcelli', 1562, 30),
    (52, 'Fair Phyllis', 1599, 30),
    (53, 'Flow My Tears', 1600, 30),
    (54, 'Ave Maria', 1599, 30);

-- Romantic
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (55, 'Symphonie Fantastique', 1830, 27),
    (56, 'Piano Concerto No. 1', 1830, 27),
    (57, 'The Flying Dutchman', 1843, 27),
    (58, 'Peer Gynt Suite', 1875, 27);

-- Contemporary
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES  
    (59, 'Symphony No. 5', 1902, 31),
    (60, 'The Firebird', 1910, 31),
    (61, 'West Side Story', 1957, 31),
    (62, 'The Planets', 1918, 31);

INSERT INTO Editor (identifier, [name], [location]) VALUES
    (1, 'Schirmer', 'New York'),
    (2, 'Hal Leonard', 'Milwaukee'),
    (3, 'Boosey & Hawkes', 'London'),
    (4, 'Ricordi', 'Milan'),
    (5, 'Durand', 'Paris'),
    (6, 'Peters', 'Leipzig'),
    (7, 'Universal Edition', 'Vienna');


INSERT INTO Score (register_num, [edition], price, [availability], difficultyGrade, musicId, editorId) VALUES
    (101, 1, 20.00, 5, 3, 1, 1),
    (102, 2, 15.50, 3, 2, 2, 2),
    (103, 1, 25.00, 4, 4, 3, 3),
    (104, 1, 30.00, 2, 5, 4, 4),
    (105, 1, 18.50, 5, 1, 5, 5),
    (106, 1, 22.00, 3, 3, 6, 6),
    (107, 1, 19.99, 4, 2, 7, 7);


INSERT INTO Instrumentation (instrument, quantity, family, [role], scoreNum) VALUES
    ('Violin', 1, 'Strings', 'Solo', 101),
    ('Piano', 1, 'Keyboard', 'Accompaniment', 102),
    ('Guitar', 1, 'Strings', 'Rhythm', 103),
    ('Flute', 1, 'Woodwind', 'Lead', 104),
    ('Drums', 1, 'Percussion', 'Rhythm', 105),
    ('Trumpet', 1, 'Brass', 'Lead', 106),
    ('Cello', 1, 'Strings', 'Bass', 107);


INSERT INTO Warehouse (id, [name], storage, editorId) VALUES
    (1, 'Main Depot', 1000, 1),
    (2, 'North Facility', 800, 2),
    (3, 'South Warehouse', 750, 3),
    (4, 'East Storage', 500, 4),
    (5, 'West Distribution Center', 450, 5),
    (6, 'Central Logistics Hub', 700, 6),
    (7, 'Overseas Shipping Yard', 650, 7);


INSERT INTO Customer (numCC, email_address, numBankAccount, cellNumber, [name]) VALUES
    (1001, 'alice@example.com', 101001, 910000000, 'Alice Smith'),
    (1002, 'bob@example.com', 101002, 920000000, 'Bob Johnson'),
    (1003, 'carol@example.com', 101003, 930000000, 'Carol Williams'),
    (1004, 'dave@example.com', 101004, 940000000, 'Dave Jones'),
    (1005, 'eve@example.com', 101005, 950000000, 'Eve Brown'),
    (1006, 'frank@example.com', 101006, 960000000, 'Frank Davis'),
    (1007, 'grace@example.com', 101007, 970000000, 'Grace Wilson');


INSERT INTO [Transaction] (transaction_id, [value], [date], customer_CC) VALUES
    (1, 100.00, '2024-01-15', 1001),
    (2, 150.00, '2024-01-16', 1002),
    (3, 75.00, '2024-01-17', 1003),
    (4, 200.00, '2024-01-18', 1004),
    (5, 120.00, '2024-01-19', 1005),
    (6, 180.00, '2024-01-20', 1006),
    (7, 130.00, '2024-01-21', 1007);


INSERT INTO Writer (id, Fname, Lname, genre, birthYear, deathYear, musGenre_id) VALUES
    (1, 'Ludwig', 'van Beethoven', 'M', '1770-12-17', '1827-03-26', 1),
    (2, 'Wolfgang', 'Amadeus Mozart', 'M', '1756-01-27', '1791-12-05', 1),
    (3, 'Johann', 'Sebastian Bach', 'M', '1685-03-31', '1750-07-28', 1),
    (4, 'Frédéric', 'Chopin', 'M', '1810-03-01', '1849-10-17', 1),
    (5, 'Claude', 'Debussy', 'M', '1862-08-22', '1918-03-25', 1),
    (6, 'Igor', 'Stravinsky', 'M', '1882-06-17', '1971-04-06', 1),
    (7, 'John', 'Williams', 'M', '1932-02-08', NULL, 5),
    (8, 'Duke', 'Ellington', 'M', '1899-04-29', '1974-05-24', 2),
    (9, 'Miles', 'Davis', 'M', '1926-05-26', '1991-09-28', 2),
    (10, 'John', 'Coltrane', 'M', '1926-09-23', '1967-07-17', 2),
    (11, 'Charlie', 'Parker', 'M', '1920-08-29', '1955-03-12', 2),
    (12, 'Dave', 'Brubeck', 'M', '1920-12-06', '2012-12-05', 2),
    (13, 'Michael', 'Jackson', 'M', '1958-08-29', '2009-06-25', 3),
    (14, 'Madonna', 'Ciccone', 'M', '1958-08-16', NULL, 3),
    (15, 'Prince', NULL, 'M', '1958-06-07', '2016-04-21', 3),
    (16, 'Whitney', 'Houston', 'M', '1963-08-09', '2012-02-11', 3),
    (17, 'Lady', 'Gaga', 'M', '1986-03-28', NULL, 3),
    (18, 'Elvis', 'Presley', 'M', '1935-01-08', '1977-08-16', 4),
    (19, 'Jimi', 'Hendrix', 'M', '1942-11-27', '1970-09-18', 4),
    (20, 'Freddie', 'Mercury', 'M', '1946-09-05', '1991-11-24', 4),
    (21, 'Robert', 'Plant', 'M', '1948-08-20', NULL, 4),
    (22, 'John', 'Lennon', 'M', '1940-10-09', '1980-12-08', 4),
    (23, 'Ludwig', 'van Beethoven', 'M', '1770-12-17', '1827-03-26', 5),
    (24, 'Maurice', 'Ravel', 'M', '1875-03-07', '1937-12-28', 5),
    (25, 'Pyotr', 'Tchaikovsky', 'M', '1840-05-07', '1893-11-06', 5),
    (26, 'Igor', 'Stravinsky', 'M', '1882-06-17', '1971-04-06', 5),
    (27, 'Georges', 'Bizet', 'M', '1838-10-25', '1875-06-03', 5),
    (28, 'John', 'Williams', 'M', '1932-02-08', NULL, 5),
    (29, 'Johann', 'Sebastian Bach', 'M', '1685-03-31', '1750-07-28', 5),
    (30, 'Gustav', 'Holst', 'M', '1874-09-21', '1934-05-25', 31),
    (31, 'Leonard', 'Bernstein', 'M', '1918-08-25', '1990-10-14', 31),
    (32, 'Johannes', 'Brahms', 'M', '1833-05-07', '1897-04-03', 5),
    (33, 'Antonín', 'Dvořák', 'M', '1841-09-08', '1904-05-01', 5),
    (34, 'Carl', 'Orff', 'M', '1895-07-10', '1982-03-29', 5),
    (35, 'George', 'Gershwin', 'M', '1898-09-26', '1937-07-11', 5),
    (36, 'Aaron', 'Copland', 'M', '1900-11-14', '1990-12-02', 5),
    (37, 'Sergei', 'Prokofiev', 'M', '1891-04-23', '1953-03-05', 5),
    (38, 'Gustav', 'Mahler', 'M', '1860-07-07', '1911-05-18', 5),
    (39, 'Richard', 'Strauss', 'M', '1864-06-11', '1949-09-08', 5),
    (40, 'Giacomo', 'Puccini', 'M', '1858-12-22', '1924-11-29', 5),
    (41, 'Gioachino', 'Rossini', 'M', '1792-02-29', '1868-11-13', 5),
    (42, 'Giacomo', 'Puccini', 'M', '1858-12-22', '1924-11-29', 5),
    (43, 'Ludwig', 'van Beethoven', 'M', '1770-12-17', '1827-03-26', 5);


INSERT INTO Composer (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5),
    (6),
    (7),
    (30),
    (31),
    (38);


INSERT INTO writes (music_id, composer_id) VALUES
    (4, 1),
    (5, 2),
    (6, 3),
    (7, 4),
    (8, 5),
    (27, 6),
    (59, 38),
    (60, 6),
    (61, 31),
    (62, 30);


INSERT INTO Arranger (id) VALUES
    (1),
    (2),
    (3),
    (4),
    (5),
    (6),
    (7);


INSERT INTO arranges (score_register, arranger_id, [type]) VALUES
    (101, 1, 'Full'),
    (102, 2, 'Partial'),
    (103, 3, 'Adaptation'),
    (104, 4, 'Harmonization'),
    (105, 5, 'Orchestration'),
    (106, 6, 'Reduction'),
    (107, 7, 'Transcription');



INSERT INTO stores (warehouse_id, score_register) VALUES
    (1, 101),
    (2, 102),
    (3, 103),
    (4, 104),
    (5, 105),
    (6, 106),
    (7, 107);


INSERT INTO purchases (costumerCC, score_register) VALUES
    (1001, 101),
    (1002, 102),
    (1003, 103),
    (1004, 104),
    (1005, 105),
    (1006, 106),
    (1007, 107);



-- Adding unique warehouse locations
INSERT INTO warehouse_location (warehouse_location, warehouse_id) VALUES
    ('101 Main St, New York, NY', 1),
    ('202 Second St, Milwaukee, WI', 2),
    ('303 Third St, London, UK', 3),
    ('404 Fourth St, Milan, IT', 4),
    ('505 Fifth St, Paris, FR', 5),
    ('606 Sixth St, Leipzig, DE', 6),
    ('707 Seventh St, Vienna, AT', 7);



-- Linking transactions and scores
INSERT INTO constitutes (score_register, transaction_id) VALUES
    (101, 1),
    (102, 2),
    (103, 3),
    (104, 4),
    (105, 5),
    (106, 6),
    (107, 7);
