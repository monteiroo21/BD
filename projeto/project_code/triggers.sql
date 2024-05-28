CREATE TABLE DeletedMusic
(
    music_id INT,
    title VARCHAR(80),
    year INT,
    musGenre_id INT,
);
IF (EXISTS (SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'music_deleted'))
BEGIN
    CREATE TABLE dbo.music_deleted (
		music_id INT,
		title VARCHAR(80),
		year INT,
		musGenre_id INT
    );
END
GO

CREATE OR ALTER TRIGGER trg_AfterDeleteMusic
ON Music
AFTER DELETE
AS
BEGIN
  
    INSERT INTO DeletedMusic (music_id, title, year, musGenre_id)
    SELECT 
        deleted.music_id,
        deleted.title,
        deleted.year,
        deleted.musGenre_id
    FROM deleted;

	PRINT 'Deleted music record has been inserted into DeletedMusic table';
END;
GO

---------------------------------------------------------------------------------------------

CREATE TRIGGER trg_CheckScoreAvailability
ON purchases
INSTEAD OF INSERT
AS
BEGIN
    DECLARE @score_register INT;

    SELECT @score_register = score_register FROM inserted;

    IF EXISTS (SELECT 1 FROM Score WHERE register_num = @score_register AND availability > 0)
    BEGIN
        INSERT INTO purchases (costumerCC, score_register)
        SELECT costumerCC, score_register FROM inserted;

        UPDATE Score
        SET availability = availability - 1
        WHERE register_num = @score_register;
    END
    ELSE
    BEGIN
        RAISERROR('Score not available for purchase', 16, 1);
    END
END;


----------------------------------------------------------------------------------------------

CREATE TABLE GenreSalesStats (
    musGenre_id INT PRIMARY KEY,
    total_sales DECIMAL(10, 2),
    total_count INT
);
IF (EXISTS (SELECT * 
    FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'dbo' AND TABLE_NAME = 'genre_stats'))
BEGIN
    CREATE TABLE dbo.genre_stats (
		musGenre_id INT PRIMARY KEY,
		total_sales DECIMAL(10, 2),
		total_count INT
    );
END
GO

CREATE TRIGGER trg_UpdateGenreSalesStats
ON purchases
AFTER INSERT
AS
BEGIN
    DECLARE @music_id INT;
    DECLARE @musGenre_id INT;
    DECLARE @price DECIMAL(10, 2);

    SELECT @music_id = m.music_id, @price = s.price
    FROM inserted i
    JOIN Score s ON i.score_register = s.register_num
    JOIN Music m ON s.musicId = m.music_id;

    SELECT @musGenre_id = musGenre_id FROM Music WHERE music_id = @music_id;

    IF EXISTS (SELECT 1 FROM GenreSalesStats WHERE musGenre_id = @musGenre_id)
    BEGIN
        UPDATE GenreSalesStats
        SET total_sales = total_sales + @price, total_count = total_count + 1
        WHERE musGenre_id = @musGenre_id;
    END
    ELSE
    BEGIN
        INSERT INTO GenreSalesStats (musGenre_id, total_sales, total_count)
        VALUES (@musGenre_id, @price, 1);
    END
END;