import os
import pymysql
from pymysql.cursors import DictCursor

# MySQL connection config from environment variables
DB_CONFIG = {
    "host": os.environ.get("MYSQL_HOST", "localhost"),
    "port": int(os.environ.get("MYSQL_PORT", 3306)),
    "user": os.environ.get("MYSQL_USER", "root"),
    "password": os.environ.get("MYSQL_PASSWORD", ""),
    "database": os.environ.get("MYSQL_DATABASE", "online_exam"),
    "charset": "utf8mb4",
}


def get_connection():
    """Create and return a MySQL database connection."""
    return pymysql.connect(**DB_CONFIG, cursorclass=DictCursor)


def create_table():
    """Create the questions table if it does not exist."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    question TEXT NOT NULL,
                    option_a TEXT NOT NULL,
                    option_b TEXT NOT NULL,
                    option_c TEXT NOT NULL,
                    option_d TEXT NOT NULL,
                    correct_answer VARCHAR(5) NOT NULL
                )
            """)
        conn.commit()
    finally:
        conn.close()


def insert_questions(questions):
    """Insert a list of question dictionaries into the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            for q in questions:
                cursor.execute(
                    """INSERT INTO questions (question, option_a, option_b, option_c, option_d, correct_answer)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (q["question"], q["option_a"], q["option_b"], q["option_c"], q["option_d"], q["correct_answer"]),
                )
        conn.commit()
    finally:
        conn.close()


def clear_questions():
    """Delete all questions from the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM questions")
        conn.commit()
    finally:
        conn.close()


def get_all_questions():
    """Fetch all questions from the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM questions")
            return cursor.fetchall()
    finally:
        conn.close()


def get_question_count():
    """Return the number of questions in the database."""
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS cnt FROM questions")
            return cursor.fetchone()["cnt"]
    finally:
        conn.close()


def is_empty():
    """Check if the questions table is empty."""
    return get_question_count() == 0
