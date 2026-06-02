import streamlit as st
import sqlite3
from google import genai
import pandas as pd
import re
import os
from dotenv import load_dotenv

load_dotenv()

# ============================================
# PAGE TITLE
# ============================================

st.set_page_config(
    page_title="AI SQL Assistant",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI SQL Assistant")
st.write("Ask questions in simple English and get SQL results instantly.")

# ============================================
# GEMINI API
# ============================================

# ---- PUT YOUR GEMINI API KEY HERE ----
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ============================================
# CREATE DATABASE
# ============================================

conn = sqlite3.connect("sales.db")

cur = conn.cursor()

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

# ============================================
# DATABASE SCHEMA
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
# USER INPUT
# ============================================

question = st.text_input(
    "Ask your database question:"
)

# ============================================
# BUTTON
# ============================================

if st.button("Generate SQL & Execute"):

    if question == "":

        st.warning("Please enter a question.")

    else:

        with st.spinner("Generating SQL..."):

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

            try:

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

                sql = response.text.strip()

                sql = re.sub(
                    r"```sql|```",
                    "",
                    sql
                ).strip()

                st.subheader("Generated SQL")

                st.code(sql, language="sql")

                # Execute SQL
                cur.execute(sql)

                rows = cur.fetchall()

                columns = [desc[0] for desc in cur.description]

                st.subheader("Query Result")

                if len(rows) == 0:

                    st.info("No results found.")

                else:

                    df = pd.DataFrame(
                        rows,
                        columns=columns
                    )

                    st.dataframe(df)

            except Exception as e:

                st.error(f"Error: {e}")

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.caption("Built with Streamlit + Gemini AI")
st.title("App Running Successfully")