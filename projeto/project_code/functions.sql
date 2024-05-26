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

        -- Insert into Arranger table
        INSERT INTO Arranger (id)
        VALUES (@new_writer_id);

        PRINT 'Arranger added successfully.';
    END
    ELSE
    BEGIN
        -- Check if the writer is already a arranger
        IF NOT EXISTS (SELECT 1 FROM Arranger WHERE id = @existing_writer_id)
        BEGIN
            -- Insert into Composer table
            INSERT INTO Arranger (id)
            VALUES (@existing_writer_id);

            PRINT 'Existing writer added as arranger successfully.';
        END
        ELSE
        BEGIN
            PRINT 'Arranger already exists.';
        END
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


CREATE OR ALTER PROCEDURE add_warehouse
    @warehouse_name VARCHAR(80),
    @storage INT,
    @editorId INT,
    @warehouse_location VARCHAR(80)
AS
BEGIN
    -- Check if the editor exists
    IF NOT EXISTS (SELECT 1 FROM Editor WHERE identifier = @editorId)
    BEGIN
        RAISERROR ('Editor does not exist', 16, 1);
        RETURN;
    END

    -- Check if the warehouse with the same name and editor already exists
    IF EXISTS (SELECT 1 FROM Warehouse WHERE name = @warehouse_name AND editorId = @editorId)
    BEGIN
        RAISERROR ('Warehouse with this name already exists for the given editor', 16, 1);
        RETURN;
    END

    -- Declare variable for new warehouse ID
    DECLARE @new_warehouse_id INT;
    SELECT @new_warehouse_id = COALESCE(MAX(id), 0) + 1 FROM Warehouse;

    -- Insert into Warehouse table
    INSERT INTO Warehouse (id, name, storage, editorId)
    VALUES (@new_warehouse_id, @warehouse_name, @storage, @editorId);

    -- Insert into warehouse_location table
    INSERT INTO warehouse_location (warehouse_location, warehouse_id)
    VALUES (@warehouse_location, @new_warehouse_id);

    PRINT 'Warehouse added successfully.';
END;
GO

CREATE OR ALTER PROCEDURE add_score
    @edition INT,
    @price DECIMAL(10, 2),
    @availability INT,
    @difficultyGrade INT,
    @musicId INT,
    @editorId INT
AS
BEGIN
    -- Check if the music exists
    IF NOT EXISTS (SELECT 1 FROM Music WHERE music_id = @musicId)
    BEGIN
        RAISERROR ('Music does not exist', 16, 1);
        RETURN;
    END

    -- Check if the editor exists
    IF NOT EXISTS (SELECT 1 FROM Editor WHERE identifier = @editorId)
    BEGIN
        RAISERROR ('Editor does not exist', 16, 1);
        RETURN;
    END

    -- Declare variable for new score register number
    DECLARE @new_register_num INT;
    SELECT @new_register_num = COALESCE(MAX(register_num), 0) + 1 FROM Score;

    -- Insert into Score table
    INSERT INTO Score (register_num, edition, price, availability, difficultyGrade, musicId, editorId)
    VALUES (@new_register_num, @edition, @price, @availability, @difficultyGrade, @musicId, @editorId);

    PRINT 'Score added successfully.';
END;
GO


CREATE OR ALTER PROCEDURE add_customer
    @numCC INT,
    @email_address VARCHAR(80),
    @numBankAccount INT,
    @cellNumber INT,
    @name VARCHAR(60)
AS
BEGIN
    -- Verifica se o número do cartão de cidadão já existe
    IF EXISTS (SELECT 1 FROM Customer WHERE numCC = @numCC)
    BEGIN
        RAISERROR ('Cliente com este número de cartão de cidadão já existe', 16, 1);
        RETURN;
    END

    -- Verifica se o número da conta bancária já está associado a outro cliente
    IF EXISTS (SELECT 1 FROM Customer WHERE numBankAccount = @numBankAccount)
    BEGIN
        RAISERROR ('Número da conta bancária já está associado a outro cliente', 16, 1);
        RETURN;
    END

    -- Verifica se o número de celular tem exatamente 9 dígitos
    IF LEN(CAST(@cellNumber AS VARCHAR(10))) != 9
    BEGIN
        RAISERROR ('Número de celular deve ter exatamente 9 dígitos', 16, 1);
        RETURN;
    END

    -- Verifica se o número do cartão de cidadão tem exatamente 8 dígitos
    IF LEN(CAST(@numCC AS VARCHAR(10))) != 8
    BEGIN
        RAISERROR ('Número do cartão de cidadão deve ter exatamente 8 dígitos', 16, 1);
        RETURN;
    END

    -- Insere o novo cliente
    INSERT INTO Customer (numCC, email_address, numBankAccount, cellNumber, [name])
    VALUES (@numCC, @email_address, @numBankAccount, @cellNumber, @name);

    PRINT 'Cliente adicionado com sucesso.';
END;
GO


CREATE OR ALTER PROCEDURE edit_music
    @music_id INT,
    @title VARCHAR(80),
    @year INT,
    @musGenre_id INT,
    @fname VARCHAR(50),
    @lname VARCHAR(50)
AS
BEGIN
    -- Check if the music exists
    IF NOT EXISTS (SELECT 1 FROM Music WHERE music_id = @music_id)
    BEGIN
        RAISERROR ('Music does not exist', 16, 1);
        RETURN;
    END

    -- Declare variable for composer ID
    DECLARE @composer_id INT;

    -- Check if the writer (composer) exists
    SELECT @composer_id = id FROM Writer WHERE Fname = @fname AND Lname = @lname;

    IF @composer_id IS NULL
    BEGIN
        RAISERROR ('Composer does not exist', 16, 1);
        RETURN;
    END

    -- Update Music table
    UPDATE Music
    SET title = @title, [year] = @year, musGenre_id = @musGenre_id
    WHERE music_id = @music_id;

    -- Check if the composer is already in the Composer table
    IF NOT EXISTS (SELECT 1 FROM Composer WHERE id = @composer_id)
    BEGIN
        INSERT INTO Composer (id)
        VALUES (@composer_id);
    END

    -- Update Writes table
    IF EXISTS (SELECT 1 FROM Writes WHERE music_id = @music_id)
    BEGIN
        UPDATE Writes
        SET composer_id = @composer_id
        WHERE music_id = @music_id;
    END
    ELSE
    BEGIN
        INSERT INTO Writes (music_id, composer_id)
        VALUES (@music_id, @composer_id);
    END
END;
GO

CREATE OR ALTER PROCEDURE edit_composer
    @old_Fname VARCHAR(60),
    @old_Lname VARCHAR(60),
    @new_Fname VARCHAR(60),
    @new_Lname VARCHAR(60),
    @genre CHAR(1),
    @birthYear INT,
    @deathYear INT,
    @musGenre_id INT
AS
BEGIN
    -- Check if the composer exists
    DECLARE @composer_id INT;
    SELECT @composer_id = w.id 
    FROM Writer w
    JOIN Composer c ON w.id = c.id
    WHERE w.Fname = @old_Fname AND w.Lname = @old_Lname;

    IF @composer_id IS NOT NULL
    BEGIN
        -- Check if the new name already exists for a different composer
        DECLARE @existing_new_composer_id INT;
        SELECT @existing_new_composer_id = id 
        FROM Writer 
        WHERE Fname = @new_Fname AND Lname = @new_Lname AND id != @composer_id;

        IF @existing_new_composer_id IS NOT NULL
        BEGIN
            PRINT 'A different composer with the new name already exists.';
            RETURN;
        END

        -- Update the Writer table with new name and details
        UPDATE Writer
        SET Fname = @new_Fname, Lname = @new_Lname, genre = @genre, birthYear = @birthYear, deathYear = @deathYear, musGenre_id = @musGenre_id
        WHERE id = @composer_id;

        PRINT 'Composer details updated successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Composer does not exist.';
    END
END;
GO

CREATE OR ALTER PROCEDURE edit_editor
    @old_name VARCHAR(50),
    @new_name VARCHAR(50),
    @location VARCHAR(50)
AS
BEGIN
    -- Check if the editor exists
    DECLARE @editor_id INT;
    SELECT @editor_id = identifier 
    FROM Editor
    WHERE [name] = @old_name;

    IF @editor_id IS NOT NULL
    BEGIN
        -- Check if the new name already exists for a different editor
        DECLARE @existing_new_editor_id INT;
        SELECT @existing_new_editor_id = identifier 
        FROM Editor 
        WHERE [name] = @new_name AND identifier != @editor_id;

        IF @existing_new_editor_id IS NOT NULL
        BEGIN
            PRINT 'A different editor with the new name already exists.';
            RETURN;
        END

        -- Update the Editor table with new name and details
        UPDATE Editor
        SET [name] = @new_name, [location] = @location
        WHERE identifier = @editor_id;

        PRINT 'Editor details updated successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Editor does not exist.';
    END
END
GO

CREATE OR ALTER PROCEDURE edit_warehouse
    @warehouse_id INT,
    @new_name VARCHAR(80),
    @new_storage INT,
    @new_editor_id INT,
    @new_warehouse_location VARCHAR(80)
AS
BEGIN
    -- Check if the warehouse exists
    IF NOT EXISTS (SELECT 1 FROM Warehouse WHERE id = @warehouse_id)
    BEGIN
        PRINT 'Warehouse does not exist.';
        RETURN;
    END

    -- Check if the new editor exists
    IF NOT EXISTS (SELECT 1 FROM Editor WHERE identifier = @new_editor_id)
    BEGIN
        PRINT 'Editor does not exist.';
        RETURN;
    END

    -- Update the Warehouse details
    UPDATE Warehouse
    SET name = @new_name, storage = @new_storage, editorId = @new_editor_id
    WHERE id = @warehouse_id;

    -- Update the warehouse location
    UPDATE warehouse_location
    SET warehouse_location = @new_warehouse_location
    WHERE warehouse_id = @warehouse_id;

    PRINT 'Warehouse details updated successfully.';
END;
GO

CREATE OR ALTER PROCEDURE edit_arranger
    @old_Fname VARCHAR(60),
    @old_Lname VARCHAR(60),
    @new_Fname VARCHAR(60),
    @new_Lname VARCHAR(60),
    @genre CHAR(1),
    @birthYear INT,
    @deathYear INT,
    @musGenre_id INT
AS
BEGIN
    -- Check if the composer exists
    DECLARE @arranger_id INT;
    SELECT @arranger_id = w.id 
    FROM Writer w
    JOIN Arranger a ON w.id = a.id
    WHERE w.Fname = @old_Fname AND w.Lname = @old_Lname;

    IF @arranger_id IS NOT NULL
    BEGIN
        -- Check if the new name already exists for a different arranger
        DECLARE @existing_new_arranger_id INT;
        SELECT @existing_new_arranger_id = id 
        FROM Writer 
        WHERE Fname = @new_Fname AND Lname = @new_Lname AND id != @arranger_id;

        IF @existing_new_arranger_id IS NOT NULL
        BEGIN
            PRINT 'A different arranger with the new name already exists.';
            RETURN;
        END

        -- Update the Writer table with new name and details
        UPDATE Writer
        SET Fname = @new_Fname, Lname = @new_Lname, genre = @genre, birthYear = @birthYear, deathYear = @deathYear, musGenre_id = @musGenre_id
        WHERE id = @arranger_id;

        PRINT 'Arranger details updated successfully.';
    END
    ELSE
    BEGIN
        PRINT 'Arranger does not exist.';
    END
END;
GO

CREATE OR ALTER PROCEDURE edit_score
    @register_num INT,
    @new_edition VARCHAR(50),
    @new_price DECIMAL(10, 2),
    @new_availability INT,
    @new_difficultyGrade INT,
    @new_music_id INT,
    @new_editor_id INT
AS
BEGIN
    -- Check if the score exists
    IF NOT EXISTS (SELECT 1 FROM Score WHERE register_num = @register_num)
    BEGIN
        PRINT 'Score does not exist.';
        RETURN;
    END

    -- Check if the new music exists
    IF NOT EXISTS (SELECT 1 FROM Music WHERE music_id = @new_music_id)
    BEGIN
        PRINT 'Music does not exist.';
        RETURN;
    END

    -- Check if the new editor exists
    IF NOT EXISTS (SELECT 1 FROM Editor WHERE identifier = @new_editor_id)
    BEGIN
        PRINT 'Editor does not exist.';
        RETURN;
    END

    -- Update the Score table with new details
    UPDATE Score
    SET edition = @new_edition, 
        price = @new_price, 
        availability = @new_availability, 
        difficultyGrade = @new_difficultyGrade, 
        musicId = @new_music_id, 
        editorId = @new_editor_id
    WHERE register_num = @register_num;

    PRINT 'Score details updated successfully.';
END;
GO
