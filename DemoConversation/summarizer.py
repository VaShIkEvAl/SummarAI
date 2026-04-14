import google.generativeai as genai

# Set your API key
genai.configure(api_key="AIzaSyBuw0svkpG-cGaFsLCO3dKDyQxT7t63-0Q")

model = genai.GenerativeModel("gemini-pro")

def summarize_text(text):
    prompt = f"Summarize the following conversation:\n\n{text}"

    response = model.generate_content(prompt)

    return response.text