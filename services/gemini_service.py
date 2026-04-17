import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-3-flash-preview"


# ---------------- CHUNKING FUNCTIONS ----------------

def split_text_smart(text, max_chars=3000):
    sentences = re.split(r'(?<=[.!?]) +', text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_chars:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def add_overlap(chunks, overlap_size=200):
    overlapped_chunks = []

    for i in range(len(chunks)):
        if i == 0:
            overlapped_chunks.append(chunks[i])
        else:
            overlap = chunks[i - 1][-overlap_size:]
            overlapped_chunks.append(overlap + " " + chunks[i])

    return overlapped_chunks


def remove_duplicates(items):
    return list(dict.fromkeys(items))

# ---------------- MAIN FUNCTION ----------------

def generate_summary(chat_text):
    print("🔵 Gemini API is being called...")

    model = genai.GenerativeModel(MODEL_NAME)

    # STEP 1: Smart chunking
    chunks = split_text_smart(chat_text)
    chunks = add_overlap(chunks)

    all_summaries = []
    all_key_points = []
    all_action_items = []

    number_api_call = 1

    # STEP 2: Process each chunk
    for chunk in chunks:
        prompt = f"""
        You are an expert conversation analyst. Carefully read the following conversation and extract structured insights with precision.

        Instructions:
        - Be concise but thorough — avoid fluff or repetition
        - Use clear, professional language
        - Only include information explicitly stated or strongly implied in the conversation
        - For action items, always identify the responsible person and a deadline if mentioned

        Conversation:
        {chunk}

        Return ONLY valid JSON in the following format:

        {{
        "title": "short heading (max 6 words)",
        "summary": "2–4 sentence summary",
        "key_points": ["point 1", "point 2"],
        "action_items": ["Person — Task — Deadline"]
        }}
        """

        print("Gemini API = ", number_api_call)
        number_api_call = number_api_call + 1

        response = model.generate_content(prompt)
        raw_output = response.text.strip()

        try:
            data = json.loads(raw_output)
        except json.JSONDecodeError:
            print("❌ JSON parsing failed for chunk")
            continue

        all_summaries.append(data.get("summary", ""))
        all_key_points.extend(data.get("key_points", []))
        all_action_items.extend(data.get("action_items", []))

    # STEP 3: Deduplicate
    all_key_points = remove_duplicates(all_key_points)
    all_action_items = remove_duplicates(all_action_items)

    # STEP 4: Combine summaries
    combined_text = " ".join(all_summaries)

    # STEP 5: Final summarization pass
    final_prompt = f"""
    You are an expert summarizer.

    Combine the following partial summaries into a final structured output.

    Text:
    {combined_text}

    Return ONLY valid JSON:

    {{
    "title": "short heading (max 6 words)",
    "summary": "final summary",
    "key_points": ["important point"],
    "action_items": ["Person — Task — Deadline"]
    }}
    """

    print("Final Gemini API call")
    final_response = model.generate_content(final_prompt)

    try:
        raw = final_response.text.strip()

        # Remove markdown if present
        raw = raw.replace("```json", "").replace("```", "").strip()

        try:
            final_data = json.loads(raw)
        except json.JSONDecodeError:
            print("❌ Final JSON parsing failed, using fallback")
            final_data = {
                "summary": combined_text,
                "key_points": all_key_points,
                "action_items": all_action_items
            }
    except json.JSONDecodeError:
        print("❌ Final JSON parsing failed, using fallback")

        final_data = {
            "summary": combined_text,
            "key_points": all_key_points,
            "action_items": all_action_items
        }

    print("🟢 Final structured response ready!")

    return final_data

def answer_all_questions(summary, questions):
    questions_text = "\n".join([
        f"Q{i+1}: {q}" for i, q in enumerate(questions)
    ])

    prompt = f"""
    You are an intelligent assistant.

    Based on the summary below, answer ALL the questions.

    Summary:
    {summary}

    Questions:
    {questions_text}

    Instructions:
    - Answer every question
    - Keep answers concise and accurate
    - Do NOT skip any question
    - Do NOT add explanations outside the JSON

    IMPORTANT:
    Return output ONLY in valid JSON format.

    Output format:
    [
    {{"question": "Question 1", "answer": "Answer 1"}},
    {{"question": "Question 2", "answer": "Answer 2"}}
    ]

    Rules:
    - Use double quotes (")
    - No trailing commas
    - No extra text before or after JSON
    - Ensure valid JSON that can be parsed using json.loads()
    - If a question cannot be answered from the summary, use "answer": "Not found in summary"
    """

    model = genai.GenerativeModel(MODEL_NAME)

    print("Gemini API call to generate answers")
    response = model.generate_content(prompt)
    print("Final Answers generated")
    return response.text.strip()