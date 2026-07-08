from flask import Flask, render_template, request, session
import os

from database import create_table, insert_questions, get_all_questions, is_empty, clear_questions
from parser import load_questions_from_pdf

app = Flask(__name__)
app.secret_key = "online-exam-secret-key-2024"


def initialize_database():
    """
    Create the table and populate it with questions from the PDF.
    Clears old questions and reloads from the PDF on every startup.
    """
    create_table()
    clear_questions()
    questions = load_questions_from_pdf()
    if questions and len(questions) > 0:
        insert_questions(questions)
        return len(questions)
    return None


def calculate_score(questions, user_answers):
    """
    Calculate score based on user answers.
    +1 for correct, -0.5 for incorrect, 0 for unanswered.
    Returns (correct, wrong, unanswered, score).
    """
    correct = 0
    wrong = 0
    unanswered = 0

    for q in questions:
        qid = str(q["id"])
        if qid in user_answers:
            user_ans = user_answers[qid]
            if user_ans == q["correct_answer"]:
                correct += 1
            else:
                wrong += 1
        else:
            unanswered += 1

    score = correct - (wrong * 0.5)
    total = len(questions)
    percentage = round((score / total) * 100, 1) if total > 0 else 0

    return correct, wrong, unanswered, score, percentage


@app.route("/")
def home():
    """Render the home page."""
    return render_template("home.html")


@app.route("/start")
def start():
    """Load the exam page with all questions."""
    questions = get_all_questions()
    if not questions:
        return render_template("exam.html", questions=[], error="No questions available.")
    return render_template("exam.html", questions=questions, error=None)


@app.route("/submit", methods=["POST"])
def submit():
    """Process submitted answers and calculate score."""
    questions = get_all_questions()
    if not questions:
        return render_template("exam.html", questions=[], error="No questions available.")

    # Collect user answers from form data
    user_answers = {}
    for q in questions:
        answer = request.form.get(f"q_{q['id']}")
        if answer:
            user_answers[str(q["id"])] = answer

    correct, wrong, unanswered, score, percentage = calculate_score(questions, user_answers)

    # Store result in session
    session["result"] = {
        "total": len(questions),
        "correct": correct,
        "wrong": wrong,
        "unanswered": unanswered,
        "score": score,
        "percentage": percentage,
    }

    return render_template(
        "result.html",
        total=len(questions),
        correct=correct,
        wrong=wrong,
        unanswered=unanswered,
        score=score,
        percentage=percentage,
    )


@app.route("/result")
def result():
    """Display the stored result."""
    result_data = session.get("result")
    if not result_data:
        return render_template("result.html", error="No result found. Please take the test first.")
    return render_template(
        "result.html",
        total=result_data["total"],
        correct=result_data["correct"],
        wrong=result_data["wrong"],
        unanswered=result_data["unanswered"],
        score=result_data["score"],
        percentage=result_data["percentage"],
    )


# Initialize the database on import (required for Gunicorn)
initialize_database()

if __name__ == "__main__":
    app.run(debug=True)
