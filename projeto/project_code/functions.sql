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

CREATE OR ALTER PROCEDURE add_composer
    @Fname VARCHAR(60),
    @Lname VARCHAR(60),
    @genre CHAR(1),
    @birthYear INT,
    @deathYear INT,
    @musGenre_id INT
AS
BEGIN
    -- Check if the writer already exists
    DECLARE @existing_writer_id INT;
    SELECT @existing_writer_id = id FROM Writer WHERE Fname = @Fname AND Lname = @Lname;

    IF @existing_writer_id IS NULL
    BEGIN
        -- Generate new writer ID
        DECLARE @new_writer_id INT;
        SELECT @new_writer_id = COALESCE(MAX(id), 0) + 1 FROM Writer;

        -- Insert into Writer table
        INSERT INTO Writer (id, Fname, Lname, genre, birthYear, deathYear, musGenre_id)
        VALUES (@new_writer_id, @Fname, @Lname, @genre, @birthYear, @deathYear, @musGenre_id);

        -- Insert into Composer table
        INSERT INTO Composer (id)
        VALUES (@new_writer_id);

        PRINT 'Composer added successfully.';
    END
    ELSE
    BEGIN
        -- Check if the writer is already a composer
        IF NOT EXISTS (SELECT 1 FROM Composer WHERE id = @existing_writer_id)
        BEGIN
            -- Insert into Composer table
            INSERT INTO Composer (id)
            VALUES (@existing_writer_id);

            PRINT 'Existing writer added as composer successfully.';
        END
        ELSE
        BEGIN
            PRINT 'Composer already exists.';
        END
    END
END;
GO


CREATE OR ALTER PROCEDURE add_arranger
    @Fname VARCHAR(60),
    @Lname VARCHAR(60),
    @genre CHAR(1),
    @birthYear INT,
    @deathYear INT,
    @musGenre_id INT
AS
BEGIN
    -- Check if the writer already exists
    IF NOT EXISTS (SELECT 1 FROM Writer WHERE Fname = @Fname AND Lname = @Lname)
    BEGIN
        -- Generate new writer ID
        DECLARE @new_writer_id INT;
        SELECT @new_writer_id = COALESCE(MAX(id), 0) + 1 FROM Writer;

        -- Insert into Writer table
        INSERT INTO Writer (id, Fname, Lname, genre, birthYear, deathYear, musGenre_id)
        VALUES (@new_writer_id, @Fname, @Lname, @genre, @birthYear, @deathYear, @musGenre_id);

        -- Insert into Composer table
        INSERT INTO Arranger (id)
        VALUES (@new_writer_id);

        PRINT 'Arranger added successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Arranger already exists.';
    END
END;
GO

CREATE OR ALTER PROCEDURE add_editor
    @name VARCHAR(50),
	@location VARCHAR(50)

AS
BEGIN
    -- Check if the writer already exists
    IF NOT EXISTS (SELECT 1 FROM Editor WHERE name = @name)
    BEGIN
        -- Generate new writer ID
        DECLARE @new_editor_id INT;
        SELECT @new_editor_id = COALESCE(MAX(identifier), 0) + 1 FROM Editor;

        -- Insert into Writer table
        INSERT INTO Editor (identifier, [name], [location]) 
        VALUES (@new_editor_id, @name, @location);

        PRINT 'Editor added successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Editor already exists.';
    END
END;
GO