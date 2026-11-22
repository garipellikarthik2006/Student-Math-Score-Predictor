
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import sqlite3
import joblib
import os

app = Flask(__name__)
app.secret_key = "student-performance-secret-key"

# Load the saved ML model
MODEL_PATH = os.path.join(
    os.path.dirname(__file__),
    "student_performance_model.pkl"
)

model = joblib.load(MODEL_PATH)

# Database configuration
DB_NAME = "students.db"


# Create database and table
def create_database():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gender TEXT NOT NULL,
            parental_education TEXT NOT NULL,
            lunch TEXT NOT NULL,
            test_preparation TEXT NOT NULL,
            reading_score INTEGER NOT NULL,
            writing_score INTEGER NOT NULL,
            predicted_math_score REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# Predict student performance
@app.route("/predict", methods=["POST"])
def predict():

    try:
        gender = request.form["gender"]
        parent_education = request.form["parent_education"]
        lunch = request.form["lunch"]
        preparation = request.form["preparation"]

        reading = int(request.form["reading"])
        writing = int(request.form["writing"])

        # Validate scores
        if not (0 <= reading <= 100 and
                0 <= writing <= 100):
            flash("Scores must be between 0 and 100.")
            return redirect(url_for("home"))

        # Create input dataframe
        student = pd.DataFrame({
            "gender": [gender],
            "parental level of education": [
                parent_education
            ],
            "lunch": [lunch],
            "test preparation course": [
                preparation
            ],
            "reading score": [reading],
            "writing score": [writing]
        })

        # Predict mathematics score
        prediction = float(model.predict(student)[0])

        # Save information in database
        conn = sqlite3.connect(DB_NAME)

        conn.execute("""
            INSERT INTO predictions (
                gender,
                parental_education,
                lunch,
                test_preparation,
                reading_score,
                writing_score,
                predicted_math_score
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            gender,
            parent_education,
            lunch,
            preparation,
            reading,
            writing,
            prediction
        ))

        conn.commit()
        conn.close()

        # Display prediction result
        return render_template(
            "result.html",
            prediction=round(prediction, 2),
            reading=reading,
            writing=writing
        )

    except (ValueError, KeyError):
        flash("Please enter valid student information.")
        return redirect(url_for("home"))


# View previous predictions
@app.route("/history")
def history():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    records = conn.execute("""
        SELECT * FROM predictions
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )

import sqlite3

def create_database():

    # Connect to SQLite database
    conn = sqlite3.connect("students.db")

    # Read SQL file
    with open("database.sql", "r") as file:
        sql_script = file.read()

    # Execute SQL commands
    conn.executescript(sql_script)

    # Save changes
    conn.commit()

    # Close connection
    conn.close()

    print("Database and table created successfully!")


if __name__ == "__main__":
    create_database()
    app.run(debug=True)
