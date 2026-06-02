from google import genai
import fitz
import time
import os

from dotenv import load_dotenv

load_dotenv()

# ---- PUT YOUR GEMINI API KEY HERE ----
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# STEP 1: Read PDF
pdf_path = r"C:\module 7\CompanyDataSheet.pdf"
doc = fitz.open(pdf_path)

pdf_text = ""
for page in doc:
    pdf_text += page.get_text()

print("=== PDF Content Read Successfully ===")
print(pdf_text)
print("=" * 60)
print()

# STEP 2: Ask Questions
questions = [
    "When was TCS founded?",
    "Who is the CEO of TCS?",
    "Where is TCS headquartered?",
    "How many employees does TCS have?",
    "What services does TCS offer?",
    "What is TCS annual revenue for 2024?"  # Not in doc - hallucination test
]

print("=== TCS Document Q&A with LLM ===")
print()

for q in questions:
    prompt = f"""
    Based ONLY on the following document content, answer the question.
    If the answer is not found in the document, say exactly:
    "Information not available in document."
    
    Document:
    {pdf_text}
    
    Question: {q}
    
    Answer in one or two sentences only.
    """

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(f"Q: {q}")
        print(f"A: {response.text.strip()}")

    except Exception as e:
        print(f"Q: {q}")
        print(f"A: ⚠️ API limit hit, waiting 30 seconds...")
        time.sleep(30)  # wait 30 seconds
        # retry once
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        print(f"A: {response.text.strip()}")

    print("-" * 60)
    time.sleep(10)  # wait 10 seconds between each question