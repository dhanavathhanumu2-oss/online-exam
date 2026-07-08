# Online Examination System

A simple web-based online examination system built with Flask and SQLite.

## Project Overview

This application allows users to:
- View a welcome page with a Start Test button
- Answer multiple-choice questions loaded from a PDF file
- Complete the exam within a 30-minute timer (auto-submits when time runs out)
- View results with correct/wrong/unanswered counts, score, and percentage

## Required Libraries

- Flask
- pdfplumber

## Installation

1. Navigate to the project directory:
   ```
   cd OnlineExam
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## How to Run

1. Place your questions PDF file in the `pdfs/` folder as `questions.pdf`.

2. Run the application:
   ```
   python app.py
   ```

3. Open your browser and go to:
   ```
   http://127.0.0.1:5000
   ```

## Folder Structure

```
OnlineExam/
│
├── app.py              # Main Flask application
├── database.py         # Database operations
├── parser.py           # PDF parsing logic
├── requirements.txt    # Python dependencies
│
├── database/
│     └── exam.db       # SQLite database (auto-created)
│
├── pdfs/
│     └── questions.pdf # Questions file
│
├── templates/
│     ├── home.html     # Home page
│     ├── exam.html     # Exam page
│     └── result.html   # Result page
│
├── static/
│     ├── css/
│     │      └── style.css
│     │
│     └── js/
│            └── timer.js
│
└── README.md
```

## Example PDF Format

The PDF must follow this format:

```
Q1. What is Python?

A. Programming Language

B. Database

C. Browser

D. Operating System

Answer: A



Q2. HTML stands for?

A. Hyper Text Machine Language

B. Hyper Text Markup Language

C. Home Tool Markup Language

D. High Transfer Markup Language

Answer: B
```

## How Scoring Works

- **Correct answer**: +1 mark
- **Wrong answer**: -0.5 marks
- **Unanswered**: 0 marks

**Example:**
- Correct: 8
- Wrong: 4
- Unanswered: 3
- Score = 8 - (4 × 0.5) = 6
- Percentage = (6 / 15) × 100 = 40%
