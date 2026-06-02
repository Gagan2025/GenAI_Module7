import sqlite3
from google import genai
import re
import os

from dotenv import load_dotenv

load_dotenv()

# ---- PUT YOUR GEMINI API KEY HERE ----
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ============================================
# STEP 1: CREATE DATABASE
# ============================================

conn = sqlite3.connect("sales.db")

cur = conn.cursor()

# ============================================
# STEP 2: CREATE TABLES
# ============================================

cur.executescript("""

CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    name TEXT,
    email TEXT,
    join_date TEXT
);

CREATE TABLE IF NOT EXISTS sales (
    sale_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    product TEXT,
    amount REAL,
    sale_date TEXT,
    FOREIGN KEY(customer_id)
    REFERENCES customer(customer_id)
);

""")

# ============================================
# STEP 3: INSERT SAMPLE DATA
# ============================================

cur.executescript("""

DELETE FROM sales;
DELETE FROM customer;

INSERT INTO customer VALUES
(1,'Alice','alice@mail.com','2024-01-01');

INSERT INTO customer VALUES
(2,'Bob','bob@mail.com','2024-01-02');

INSERT INTO customer VALUES
(3,'Carol','carol@mail.com','2024-01-03');

INSERT INTO customer VALUES
(4,'David','david@mail.com','2024-01-04');

INSERT INTO sales VALUES
(1,1,'Laptop',1200,'2024-05-30');

INSERT INTO sales VALUES
(2,2,'Phone',800,'2024-05-31');

INSERT INTO sales VALUES
(3,3,'Tablet',600,'2024-06-01');

INSERT INTO sales VALUES
(4,1,'Mouse',50,'2024-06-01');

INSERT INTO sales VALUES
(5,4,'Headphones',150,'2024-06-01');

INSERT INTO sales VALUES
(6,2,'Smartwatch',350,'2024-05-31');

""")

conn.commit()

print("✅ Database Created Successfully!")

# ============================================
# STEP 4: DATABASE SCHEMA
# ============================================

schema = """

customer(
customer_id INTEGER PRIMARY KEY,
name TEXT,
email TEXT,
join_date TEXT
)

sales(
sale_id INTEGER PRIMARY KEY,
customer_id INTEGER,
product TEXT,
amount REAL,
sale_date TEXT
)

"""

# ============================================
# STEP 5: TAKE USER QUESTION
# ============================================

question = input("Ask Question: ")

# ============================================
# STEP 6: CREATE PROMPT
# ============================================

prompt = f"""

Database Schema:

{schema}

Convert the user's question into SQLite SQL.

Question:
{question}

Rules:
1. Return ONLY SQL
2. No markdown
3. No explanation
4. Output must run in SQLite

"""

# ============================================
# STEP 7: GENERATE SQL USING GEMINI
# ============================================

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

sql = response.text.strip()

# Remove markdown if generated
sql = re.sub(
    r"```sql|```",
    "",
    sql
).strip()

print("\nGenerated SQL:\n")

print(sql)

# ============================================
# STEP 8: EXECUTE SQL QUERY
# ============================================

try:

    cur.execute(sql)

    rows = cur.fetchall()

    print("\nQuery Result:\n")

    if len(rows) == 0:

        print("No results found.")

    else:

        columns = [desc[0] for desc in cur.description]

        print(" | ".join(columns))

        print("-" * 50)

        for row in rows:

            print(" | ".join(str(v) for v in row))

except Exception as e:

    print("\nExecution Error:")

    print(e)

# ============================================
# STEP 9: CLOSE DATABASE
# ============================================

finally:

    conn.close()

    print("\n✅ Task Completed!")