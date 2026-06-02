from google import genai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# ---- PUT YOUR GEMINI API KEY HERE ----
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# User activity data
user_activity = """
- User A logged in and purchased a laptop worth $1200
- User B logged in but did not make any purchase
- User C purchased a phone worth $800
"""

# Well-structured prompt
prompt = f"""
You are a data analyst. Analyze the following user activity log.

User Activity:
{user_activity}

Task:
1. Summarize the overall user activity
2. Extract structured insights

Return ONLY a valid JSON object in this exact format (no extra text, no markdown):
{{
  "summary": "brief summary here",
  "total_users": 3,
  "purchasing_users": 2,
  "total_revenue": 2000,
  "insights": [
    "insight 1",
    "insight 2"
  ]
}}
"""

# Call Gemini LLM
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

raw_text = response.text.strip()

# Clean and parse JSON
clean_text = raw_text.replace("```json", "").replace("```", "").strip()
result = json.loads(clean_text)

# Display formatted output
print("=== LLM Output ===")
print(json.dumps(result, indent=2))