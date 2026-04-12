import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3-flash-preview"

def generate_summary(chat_text):
    print("🔵 Gemini API is being called...")  # Console log

    model = genai.GenerativeModel(MODEL_NAME)

    prompt = f"""
    Summarize the following conversation into a clear and concise paragraph.

    Conversation:
    {chat_text}
    """

    response = model.generate_content(prompt)

    print("🟢 Gemini response received!")  # Console log

    return response.text.strip()