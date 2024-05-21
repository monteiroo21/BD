-- Verifica e cria índices para music.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_musGenre_id' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_musGenre_id ON Music (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_writes_music_id' AND object_id = OBJECT_ID('writes'))
CREATE INDEX idx_writes_music_id ON writes (music_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_writes_composer_id' AND object_id = OBJECT_ID('writes'))
CREATE INDEX idx_writes_composer_id ON writes (composer_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Composer_id' AND object_id = OBJECT_ID('Composer'))
CREATE INDEX idx_Composer_id ON Composer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

-- Verifica e cria índices para editor.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Editor_name' AND object_id = OBJECT_ID('Editor'))
CREATE INDEX idx_Editor_name ON Editor ([name]);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Editor_identifier' AND object_id = OBJECT_ID('Editor'))
CREATE INDEX idx_Editor_identifier ON Editor (identifier);

-- Verifica e cria índices para warehouse.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Warehouse_editorId' AND object_id = OBJECT_ID('Warehouse'))
CREATE INDEX idx_Warehouse_editorId ON Warehouse (editorId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Warehouse_name' AND object_id = OBJECT_ID('Warehouse'))
CREATE INDEX idx_Warehouse_name ON Warehouse ([name]);

-- Verifica e cria índices para score.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Score_musicId' AND object_id = OBJECT_ID('Score'))
CREATE INDEX idx_Score_musicId ON Score (musicId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Score_editorId' AND object_id = OBJECT_ID('Score'))
CREATE INDEX idx_Score_editorId ON Score (editorId);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_id' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_id ON Music (music_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Music_title' AND object_id = OBJECT_ID('Music'))
CREATE INDEX idx_Music_title ON Music (title);

-- Verifica e cria índices para composer.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Composer_id' AND object_id = OBJECT_ID('Composer'))
CREATE INDEX idx_Composer_id ON Composer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_musGenre_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_musGenre_id ON Writer (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);

-- Verifica e cria índices para arranger.py
IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Arranger_id' AND object_id = OBJECT_ID('Arranger'))
CREATE INDEX idx_Arranger_id ON Arranger (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_id ON Writer (id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_name' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_name ON Writer (Fname, Lname);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_Writer_musGenre_id' AND object_id = OBJECT_ID('Writer'))
CREATE INDEX idx_Writer_musGenre_id ON Writer (musGenre_id);

IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name = 'idx_MusicalGenre_name' AND object_id = OBJECT_ID('MusicalGenre'))
CREATE INDEX idx_MusicalGenre_name ON MusicalGenre ([name]);
