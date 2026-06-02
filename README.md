# Module 7 - Generative AI & AI Agenting Assignment

## Overview
This project demonstrates the use of Generative AI (Google Gemini) 
for Data Engineering tasks including prompt engineering, LLM interaction,
data augmentation, document querying, and natural language to SQL conversion.

## Project Structure

module 7/
├── .env                          # API keys (never commit this!)
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation
├── prompts.txt                   # Task 1 - 3 Prompt Engineering examples
├── task2_chat_llm.py             # Task 2 - Chat with LLM & format output
├── task3_data_augmentation.py    # Task 3 - Data generation & augmentation
├── task4_doc_query.py            # Task 4 - PDF document querying
├── task5_nl_to_sql.py            # Task 5 - Natural language to SQL
├── create_db.py                  # Helper - creates SQLite database
├── sample_data.csv               # Input data for Task 3
├── augmented_data.csv            # Output data from Task 3
├── TCS_Company_Data.pdf          # PDF used in Task 4
└── sql_extraction/
└── sales.db                  # SQLite database for Task 5

## Setup Instructions

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd module-7
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup API Key
- Get your free Gemini API key from: https://aistudio.google.com/app/api-keys
- Create a `.env` file in the root folder
- Add your key:
GEMINI_API_KEY=your_key_here

### 4. Setup Database (for Task 5)
```bash
python create_db.py
```

## Running Each Task

### Task 1 - Prompt Engineering
Open `prompts.txt` — contains 3 well-structured prompts for data engineering use cases.

### Task 2 - Chat with LLM
```bash
python task2_chat_llm.py
```
Sends user activity data to Gemini and returns structured JSON insights.

### Task 3 - Data Augmentation
```bash
python task3_data_augmentation.py
```
Reads `sample_data.csv` and generates 5 additional similar rows using Gemini.

### Task 4 - Document Querying
```bash
python task4_doc_query.py
```
Reads `TCS_Company_Data.pdf` and answers questions using Gemini.

### Task 5 - Natural Language to SQL
```bash
python task5_nl_to_sql.py
```
Type a natural language question and Gemini converts it to SQL and runs it.

Example questions:
- `Show all customers who bought a Laptop`
- `What is the total revenue from all sales?`
- `Show the highest sales amount done by each customer`

## Technologies Used
- Python 3.x
- Google Gemini API (gemini-2.0-flash)
- SQLite3
- Pandas
- PyMuPDF (fitz)
- python-dotenv

## Important Notes
- Never commit your `.env` file
- Free Gemini API has daily rate limits
- If you hit rate limits, create a new API key or wait 24 hours

Step 5: Generate requirements.txt automatically
You can also run this in terminal to auto-generate it:
bashpip freeze > requirements.txt

Your final folder should look like:
C:\module 7\
├── .env                       ← API key
├── .gitignore                 ← git ignore rules  
├── requirements.txt           ← dependencies
├── README.md                  ← project docs
├── prompts.txt
├── task2_chat_llm.py
├── task3_data_augmentation.py
├── task4_doc_query.py
├── task5_nl_to_sql.py
├── create_db.py
├── sample_data.csv
├── augmented_data.csv
├── TCS_Company_Data.pdf
└── sql_extraction/
    └── sales.db
Let me know when done and we'll move to Azure deployment! 🚀  