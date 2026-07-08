from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

questions = [
    {
        "q": "What is Python?",
        "options": ["Programming Language", "Database", "Browser", "Operating System"],
        "answer": "A",
    },
    {
        "q": "HTML stands for?",
        "options": [
            "Hyper Text Machine Language",
            "Hyper Text Markup Language",
            "Home Tool Markup Language",
            "High Transfer Markup Language",
        ],
        "answer": "B",
    },
    {
        "q": "Which of the following is a Python framework?",
        "options": ["Django", "Laravel", "Spring", "React"],
        "answer": "A",
    },
    {
        "q": "What does CSS stand for?",
        "options": [
            "Computer Style Sheets",
            "Cascading Style Sheets",
            "Creative Style Sheets",
            "Colorful Style Sheets",
        ],
        "answer": "B",
    },
    {
        "q": "Which data structure uses LIFO?",
        "options": ["Queue", "Stack", "Array", "Linked List"],
        "answer": "B",
    },
    {
        "q": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "C",
    },
    {
        "q": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": "C",
    },
    {
        "q": "SQL is used for?",
        "options": [
            "Styling web pages",
            "Managing databases",
            "Creating graphics",
            "Building mobile apps",
        ],
        "answer": "B",
    },
    {
        "q": "What is the square root of 64?",
        "options": ["6", "7", "8", "9"],
        "answer": "C",
    },
    {
        "q": "Which protocol is used for web browsing?",
        "options": ["FTP", "SMTP", "HTTP", "TCP"],
        "answer": "C",
    },
]

for i, q in enumerate(questions, 1):
    pdf.cell(0, 10, f"Q{i}. {q['q']}", new_x="LMARGIN", new_y="NEXT")
    labels = ["A", "B", "C", "D"]
    for label, option in zip(labels, q["options"]):
        pdf.cell(0, 10, f"{label}. {option}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Answer: {q['answer']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, "", new_x="LMARGIN", new_y="NEXT")

pdf.output("pdfs/questions.pdf")
print("PDF created successfully at pdfs/questions.pdf")
