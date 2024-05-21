CREATE OR ALTER PROCEDURE insert_music
    @title VARCHAR(80),
    @year INT,
    @musGenre_id INT
AS
BEGIN
    IF EXISTS (SELECT 1 FROM Music WHERE title = @title AND [year] = @year AND musGenre_id = @musGenre_id)
    BEGIN
        RAISERROR ('Music already exists', 16, 1);
        RETURN;
    END
    ELSE
    BEGIN
        DECLARE @new_music_id INT;
        SELECT @new_music_id = COALESCE(MAX(music_id), 0) + 1 FROM Music;
        
        INSERT INTO Music (music_id, title, [year], musGenre_id)
        VALUES (@new_music_id, @title, @year, @musGenre_id);
    END
END;
GO
