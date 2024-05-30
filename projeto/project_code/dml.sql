INSERT INTO MusicalGenre (id, [name]) VALUES
    (1, 'Classical'),
    (2, 'Jazz'),
    (3, 'Pop'),
    (4, 'Rock'),
    (5, 'Choral'),
    (6, 'Marching Band'),
    (7, 'Jazz Band'),
    (8, 'Wind Band'),
    (9, 'String Orchestra'),
    (10, 'Ensemble'),
    (11, 'Choir'),
    (12, 'Symphonic'),
    (13, 'Romantic'),
    (14, 'Medieval'),
    (15, 'Baroque'),
    (16, 'Renaissance'),
    (17, 'Contemporary');


INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (1, 'Moonlight Sonata', 1801, 1),
    (2, 'Fur Elise', 1810, 1),
    (3, 'Symphony No. 9', 1824, 13);

-- Classical
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (4, 'Symphony No. 5', 1808, 1),
    (5, 'Four Seasons', 1725, 15),
    (6, 'Canon in D', 1680, 15),
    (7, 'Swan Lake', 1876, 13),
    (8, 'Magic Flute', 1791, 1);

    
-- Jazz
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (9, 'So What', 1959, 2),
    (10, 'Giant Steps', 1960, 2);

-- Pop
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (11, 'Thriller', 1982, 3),
    (12, 'Like a Virgin', 1984, 3);

-- Orchestra
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (13, 'Bolero', 1928, 17),
    (14, 'The Nutcracker Suite', 1892, 13),
    (15, 'Rite of Spring', 1913, 17),
    (16, 'New World Symphony', 1893, 13),
    (17, 'Carmen Suite', 1875, 13);

-- Choir
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (18, 'Carmina Burana', 1936, 11),
    (19, 'Messiah', 1741, 11),
    (20, 'Requiem', 1791, 11);

-- Romantic
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES
    (21, 'Symphonie Fantastique', 1830, 13),
    (22, 'Piano Concerto No. 1', 1830, 13);

-- Contemporary
INSERT INTO Music (music_id, title, [year], musGenre_id) VALUES  
    (23, 'Symphony No. 5', 1902, 17),
    (24, 'The Firebird', 1910, 17),
    (25, 'West Side Story', 1957, 17),
    (26, 'The Planets', 1918, 17);

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
    (10010000, 'alice@example.com', 101001, 910000000, 'Alice Smith'),
    (10020000, 'bob@example.com', 101002, 920000000, 'Bob Johnson'),
    (10030000, 'carol@example.com', 101003, 930000000, 'Carol Williams'),
    (10040000, 'dave@example.com', 101004, 940000000, 'Dave Jones'),
    (10050000, 'eve@example.com', 101005, 950000000, 'Eve Brown'),
    (10060000, 'frank@example.com', 101006, 960000000, 'Frank Davis'),
    (10070000, 'grace@example.com', 101007, 970000000, 'Grace Wilson');


INSERT INTO [Transaction] (transaction_id, [value], [date], customer_CC) VALUES
    (1, 35.50, '2024-01-15', 10010000),
    (2, 15.50, '2024-01-16', 10020000),
    (3, 25.00, '2024-01-17', 10030000),
    (4, 30.00, '2024-01-18', 10040000),
    (5, 18.50, '2024-01-19', 10050000),
    (6, 22.00, '2024-01-20', 10060000),
    (7, 19.99, '2024-01-21', 10070000);


INSERT INTO Writer (id, Fname, Lname, genre, birthYear, deathYear, musGenre_id) VALUES
    (1, 'Ludwig', 'van Beethoven', 'M', '1770', '1827', 1),
    (2, 'Wolfgang', 'Amadeus Mozart', 'M', '1756', '1791', 1),
    (3, 'Johann', 'Sebastian Bach', 'M', '1685', '1750', 15),
    (4, 'Antonio', 'Vivaldi', 'M', '1678', '1741', 15),
    (5, 'Claude', 'Debussy', 'M', '1862', '1918', 13),
    (6, 'Igor', 'Stravinsky', 'M', '1882', '1971', 17),
    (7, 'John', 'Williams', 'M', '1932', NULL, 17),
    (8, 'Duke', 'Ellington', 'M', '1899', '1974', 2),
    (9, 'Miles', 'Davis', 'M', '1926', '1991', 2),
    (10, 'John', 'Coltrane', 'M', '1926', '1967', 2),
    (11, 'Charlie', 'Parker', 'M', '1920', '1955', 2),
    (12, 'Dave', 'Brubeck', 'M', '1920', '2012', 2),
    (13, 'Michael', 'Jackson', 'M', '1958', '2009', 3),
    (14, 'Madonna', 'Ciccone', 'F', '1958', NULL, 3),
    (15, 'Hector', 'Berlioz', 'M', '1803', '1869', 13),
    (16, 'Whitney', 'Houston', 'F', '1963', '2012', 3),
    (17, 'Lady', 'Gaga', 'F', '1986', NULL, 3),
    (18, 'Elvis', 'Presley', 'M', '1935', '1977', 4),
    (19, 'Jimi', 'Hendrix', 'M', '1942', '1970', 4),
    (20, 'Freddie', 'Mercury', 'M', '1946', '1991', 4),
    (21, 'Robert', 'Plant', 'M', '1948', NULL, 4),
    (22, 'John', 'Lennon', 'M', '1940', '1980', 4),
    (24, 'Maurice', 'Ravel', 'M', '1875', '1937', 13),
    (25, 'Pyotr', 'Tchaikovsky', 'M', '1840', '1893', 13),
    (27, 'Georges', 'Bizet', 'M', '1838', '1875', 13),
    (29, 'Johann', 'Sebastian Bach', 'M', '1685', '1750', 15),
    (30, 'Gustav', 'Holst', 'M', '1874', '1934', 13),
    (31, 'Leonard', 'Bernstein', 'M', '1918', '1990', 17),
    (32, 'Johannes', 'Brahms', 'M', '1833', '1897', 13),
    (33, 'Antonín', 'Dvořák', 'M', '1841', '1904', 13),
    (34, 'Carl', 'Orff', 'M', '1895', '1982', 17),
    (35, 'George', 'Gershwin', 'M', '1898', '1937', 17),
    (36, 'Aaron', 'Copland', 'M', '1900', '1990', 17),
    (37, 'Sergei', 'Prokofiev', 'M', '1891', '1953', 17),
    (38, 'Gustav', 'Mahler', 'M', '1860', '1911', 13),
    (39, 'Richard', 'Strauss', 'M', '1864', '1949', 13),
    (40, 'George', 'Handel', 'M', '1685', '1759', 15),
    (41, 'Gioachino', 'Rossini', 'M', '1792', '1868', 1);


INSERT INTO Composer (id) VALUES
    (1),
    (2),
    (4),
    (5),
    (6),
    (9),
    (10),
    (13),
    (14),
    (15),
    (24),
    (25),
    (27),
    (30),
    (31),
    (32),
    (33),
    (34),
    (38),
    (40);



INSERT INTO writes (music_id, composer_id) VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 4),
    (6, 5),
    (7, 25),
    (8, 2),
    (9, 9),
    (10, 10),
    (11, 13),
    (12, 14),
    (13, 24),
    (14, 25),
    (15, 6),
    (16, 33),
    (17, 27),
    (18, 34),
    (19, 40),
    (20, 2),
    (21, 15),
    (22, 25),
    (23, 38),
    (24, 6),
    (25, 31),
    (26, 30);



INSERT INTO Arranger (id) VALUES
    (3),
    (7),
    (35),
    (37),
    (39),
    (41);


INSERT INTO arranges (score_register, arranger_id, [type]) VALUES
    (101, 3, 'Full'),
    (102, 7, 'Partial'),
    (103, 3, 'Adaptation'),
    (104, 35, 'Harmonization'),
    (105, 37, 'Orchestration'),
    (106, 39, 'Reduction'),
    (107, 41, 'Transcription');



INSERT INTO stores (warehouse_id, score_register) VALUES
    (1, 101),
    (2, 102),
    (3, 103),
    (4, 104),
    (5, 105),
    (6, 106),
    (7, 107);


INSERT INTO purchases (costumerCC, score_register) VALUES
    (10010000, 101),
    (10010000, 102),
    (10020000, 102),
    (10030000, 103),
    (10040000, 104),
    (10050000, 105),
    (10060000, 106),
    (10070000, 107);



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
    (102, 1),
    (102, 2),
    (103, 3),
    (104, 4),
    (105, 5),
    (106, 6),
    (107, 7);