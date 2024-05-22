CREATE OR ALTER PROCEDURE insert_music
    @title VARCHAR(80),
    @year INT,
    @musGenre_id INT,
    @fname VARCHAR(50),
    @lname VARCHAR(50)
AS
BEGIN
    -- Check if the music already exists
    IF EXISTS (SELECT 1 FROM Music WHERE title = @title AND [year] = @year AND musGenre_id = @musGenre_id)
    BEGIN
        RAISERROR ('Music already exists', 16, 1);
        RETURN;
    END

    -- Declare variables for new IDs
    DECLARE @new_music_id INT;
    DECLARE @composer_id INT;

    -- Generate new music ID
    SELECT @new_music_id = COALESCE(MAX(music_id), 0) + 1 FROM Music;

    -- Check if the writer (composer) exists
    SELECT @composer_id = id FROM Writer WHERE Fname = @fname AND Lname = @lname;

    IF @composer_id IS NULL
    BEGIN
        RAISERROR ('Composer does not exist', 16, 1);
        RETURN;
    END

    -- Insert into Music table
    INSERT INTO Music (music_id, title, [year], musGenre_id)
    VALUES (@new_music_id, @title, @year, @musGenre_id);

    -- Insert into Composer table if not exists
    IF NOT EXISTS (SELECT 1 FROM Composer WHERE id = @composer_id)
    BEGIN
        INSERT INTO Composer (id)
        VALUES (@composer_id);
    END

    -- Insert into Writes table
    INSERT INTO Writes (music_id, composer_id)
    VALUES (@new_music_id, @composer_id);
END;
GO