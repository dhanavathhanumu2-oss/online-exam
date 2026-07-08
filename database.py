import sqlite3
import os

# Database file path
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "database", "exam.db")


def get_connection():
    """Create and return a database connection."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    """Create the questions table if it does not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            option_a TEXT NOT NULL,
            option_b TEXT NOT NULL,
            option_c TEXT NOT NULL,
            option_d TEXT NOT NULL,
            correct_answer TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def insert_questions(questions):
    """
    Insert a list of question dictionaries into the database.
    Each question dict must have: question, option_a, option_b, option_c, option_d, correct_answer.
    """
    conn = get_connection()
    cursor = conn.cursor()
    for q in questions:
        cursor.execute(
            """INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (q["question"], q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_answer"]),
        )
    conn.commit()
    conn.close()


def clear_questions():
    """Delete all questions from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM questions")
    conn.commit()
    conn.close()


def get_all_questions():
    """Fetch all questions from the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM questions")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_question_count():
    """Return the number of questions in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM questions")
    count = cursor.fetchone()[0]
    conn.close()
    return count


def is_empty():
    """Check if the questions table is empty."""
    return get_question_count() == 0
