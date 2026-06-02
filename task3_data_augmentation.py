from google import genai
import pandas as pd
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ---- PUT YOUR GEMINI API KEY HERE ----
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Step 1: Read existing CSV
df = pd.read_csv("sample_data.csv")
print("=== Original Data ===")
print(df)
print()

# Step 2: Ask LLM to generate similar data
prompt = f"""
Here is a sample dataset of customer sales:
{df.to_string()}

Generate 5 more similar rows of realistic fake data following the 
exact same column structure: customer_id, name, email, product, amount, date

Rules:
- customer_id should continue from 4 to 8
- Use realistic names and emails
- Products should be electronics like: Laptop, Phone, Tablet, Headphones, Smartwatch
- Amount should be between 100 and 2000
- Dates should be in format YYYY-MM-DD

Return ONLY a JSON array, no extra text, no markdown:
[
  {{"customer_id": 4, "name": "...", "email": "...", "product": "...", "amount": 999, "date": "2024-01-18"}}
]
"""

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

raw = response.text.replace("```json","").replace("```","").strip()
new_rows = json.loads(raw)

# Step 3: Combine original + generated data
new_df = pd.DataFrame(new_rows)
final_df = pd.concat([df, new_df], ignore_index=True)

print("=== Augmented Data (Original + AI Generated) ===")
print(final_df)

# Step 4: Save to new CSV
final_df.to_csv("augmented_data.csv", index=False)
print()
print("✅ Saved to augmented_data.csv")