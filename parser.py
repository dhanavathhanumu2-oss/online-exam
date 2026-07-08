import re
import pdfplumber
import os
import glob

# PDF directory
PDF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pdfs")


def find_pdf():
    """Find the first PDF file in the pdfs directory."""
    pdf_files = glob.glob(os.path.join(PDF_DIR, "*.pdf"))
    return pdf_files[0] if pdf_files else None


def extract_text_from_pdf(pdf_path):
    """Extract all text from a PDF file and return as a single string."""
    if not os.path.exists(pdf_path):
        return None
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text.strip()


def parse_questions(text):
    """
    Parse the extracted text and return a list of question dictionaries.
    Expected format:
        Q1. What is Python?
        A. Programming Language
        B. Database
        C. Browser
        D. Operating System
        Answer: A

        Q2. HTML stands for?
        ...
    Questions can be separated by blank lines or be contiguous.
    """
    if not text:
        return []

    # Split text by question headers (e.g., Q1., Q2., etc.)
    blocks = re.split(r"\n(?=Q\d+[\.\s])", text)
    questions = []

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        # Extract question line (starts with Q followed by number and dot)
        question_match = re.search(r"^Q\d+[\.\s]+(.+)", block, re.MULTILINE)
        if not question_match:
            continue

        # Extract options
        option_a = re.search(r"^A[\.\s]+(.+)$", block, re.MULTILINE)
        option_b = re.search(r"^B[\.\s]+(.+)$", block, re.MULTILINE)
        option_c = re.search(r"^C[\.\s]+(.+)$", block, re.MULTILINE)
        option_d = re.search(r"^D[\.\s]+(.+)$", block, re.MULTILINE)

        # Extract answer
        answer_match = re.search(r"Answer:\s*([A-D])", block, re.IGNORECASE)

        if option_a and option_b and option_c and option_d and answer_match:
            questions.append({
                "question": question_match.group(1).strip(),
                "option_a": option_a.group(1).strip(),
                "option_b": option_b.group(1).strip(),
                "option_c": option_c.group(1).strip(),
                "option_d": option_d.group(1).strip(),
                "correct_answer": answer_match.group(1).strip().upper(),
            })

    return questions


def load_questions_from_pdf():
    """
    Load questions from the first PDF found in the pdfs/ directory.
    Returns a list of question dictionaries, or None if no PDF found.
    """
    pdf_path = find_pdf()
    if pdf_path is None:
        return None
    text = extract_text_from_pdf(pdf_path)
    if text is None:
        return None
    return parse_questions(text)
