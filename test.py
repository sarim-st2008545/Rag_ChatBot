from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

try:
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": "Hello"}],
        model="llama-3.3-70b-versatile",
    )
    print("API working! Response:", response.choices[0].message.content)
except Exception as e:
    print("API error:", str(e))