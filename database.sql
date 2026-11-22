
-- Create database table for student predictions

CREATE TABLE IF NOT EXISTS predictions (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    gender TEXT NOT NULL,

    parental_education TEXT NOT NULL,

    lunch TEXT NOT NULL,

    test_preparation TEXT NOT NULL,

    reading_score INTEGER NOT NULL,

    writing_score INTEGER NOT NULL,

    predicted_math_score REAL NOT NULL

);
