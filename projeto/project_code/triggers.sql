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
END
GO


DROP TRIGGER IF EXISTS trg_delete_composer;
GO
CREATE TRIGGER trg_delete_composer
ON Composer
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @composer_id INT;
    DECLARE @music_id INT;

    -- Cursor to iterate over deleted composers
    DECLARE composer_cursor CURSOR FOR
        SELECT id FROM deleted;

    OPEN composer_cursor;
    FETCH NEXT FROM composer_cursor INTO @composer_id;

    BEGIN
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Cursor to iterate over music pieces composed by the composer
            DECLARE music_cursor CURSOR FOR
                SELECT music_id FROM writes WHERE composer_id = @composer_id;

            OPEN music_cursor;
            FETCH NEXT FROM music_cursor INTO @music_id;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Delete from the Score table and related tables
                DELETE FROM Instrumentation WHERE scoreNum IN (SELECT register_num FROM Score WHERE musicId = @music_id);
                DELETE FROM stores WHERE score_register IN (SELECT register_num FROM Score WHERE musicId = @music_id);
                DELETE FROM purchases WHERE score_register IN (SELECT register_num FROM Score WHERE musicId = @music_id);
                DELETE FROM arranges WHERE score_register IN (SELECT register_num FROM Score WHERE musicId = @music_id);
				DELETE FROM constitutes WHERE score_register IN (SELECT register_num FROM Score WHERE musicId = @music_id);
                DELETE FROM Score WHERE musicId = @music_id;

				DELETE FROM writes WHERE music_id = @music_id;

                -- Delete the music piece
                DELETE FROM Music WHERE music_id = @music_id;

                FETCH NEXT FROM music_cursor INTO @music_id;
            END

            CLOSE music_cursor;
            DEALLOCATE music_cursor;

            -- Delete the composer
            DELETE FROM Composer WHERE id = @composer_id;

            FETCH NEXT FROM composer_cursor INTO @composer_id;
        END

        CLOSE composer_cursor;
        DEALLOCATE composer_cursor;

    END
END
GO

CREATE TRIGGER trg_delete_arranger
ON Arranger
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @arranger_id INT;
    DECLARE @score_register INT;

    -- Cursor to iterate over deleted arrangers
    DECLARE arranger_cursor CURSOR FOR
        SELECT id FROM deleted;

    OPEN arranger_cursor;
    FETCH NEXT FROM arranger_cursor INTO @arranger_id;

    BEGIN
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Cursor to iterate over scores arranged by the arranger
            DECLARE score_cursor CURSOR FOR
                SELECT score_register FROM arranges WHERE arranger_id = @arranger_id;

            OPEN score_cursor;
            FETCH NEXT FROM score_cursor INTO @score_register;

            WHILE @@FETCH_STATUS = 0
            BEGIN
                -- Delete the instrumentation associated with the score
                DELETE FROM Instrumentation WHERE scoreNum = @score_register;

                -- Delete from the stores table
                DELETE FROM stores WHERE score_register = @score_register;

                -- Delete from the purchases table
                DELETE FROM purchases WHERE score_register = @score_register;

                -- Delete from the arranges table
                DELETE FROM arranges WHERE score_register = @score_register;

				-- Delete from the constitutes table
				DELETE FROM constitutes WHERE score_register = @score_register

                -- Delete the score
                DELETE FROM Score WHERE register_num = @score_register;

                FETCH NEXT FROM score_cursor INTO @score_register;
            END

            CLOSE score_cursor;
            DEALLOCATE score_cursor;

            -- Delete the arranger
            DELETE FROM Arranger WHERE id = @arranger_id;

            FETCH NEXT FROM arranger_cursor INTO @arranger_id;
        END

        CLOSE arranger_cursor;
        DEALLOCATE arranger_cursor;
    END
END
GO

DROP TRIGGER IF EXISTS trg_delete_warehouse;
GO
CREATE TRIGGER trg_delete_warehouse
ON Warehouse
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @warehouse_id INT;

    -- Cursor to iterate over deleted warehouses
    DECLARE warehouse_cursor CURSOR FOR
        SELECT id FROM deleted;

    OPEN warehouse_cursor;
    FETCH NEXT FROM warehouse_cursor INTO @warehouse_id;

    BEGIN
        WHILE @@FETCH_STATUS = 0
        BEGIN
            -- Delete from the stores table
            DELETE FROM stores WHERE warehouse_id = @warehouse_id;

            -- Delete from the warehouse_location table
            DELETE FROM warehouse_location WHERE warehouse_id = @warehouse_id;

            -- Delete the warehouse
            DELETE FROM Warehouse WHERE id = @warehouse_id;

            FETCH NEXT FROM warehouse_cursor INTO @warehouse_id;
        END

        CLOSE warehouse_cursor;
        DEALLOCATE warehouse_cursor;
    END
END
GO

DROP TRIGGER IF EXISTS trg_delete_customer;
GO
CREATE TRIGGER trg_delete_customer
ON Customer
INSTEAD OF DELETE
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @customer_cc INT;

    -- Cursor to iterate over deleted customers
    DECLARE customer_cursor CURSOR FOR
        SELECT numCC FROM deleted;

    OPEN customer_cursor;
    FETCH NEXT FROM customer_cursor INTO @customer_cc;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        -- Delete from the purchases table
        DELETE FROM purchases WHERE costumerCC = @customer_cc;

        -- Delete from the Transaction table
        DELETE FROM [Transaction] WHERE customer_CC = @customer_cc;

        -- Delete the customer
        DELETE FROM Customer WHERE numCC = @customer_cc;

        FETCH NEXT FROM customer_cursor INTO @customer_cc;
    END

    CLOSE customer_cursor;
    DEALLOCATE customer_cursor;
END
GO