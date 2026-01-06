import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key="SECRET_KEY")

def get_bot_response(user_message):
    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful finance assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        return f"AI Error: {str(e)}"