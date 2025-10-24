
# Communicates with Gemini API (Google Generative AI)
import os
import google.generativeai as genai

def get_ai_explanation(organ_name: str, description: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Gemini API key not set."
    genai.configure(api_key=api_key)
    prompt = f"Explain the anatomy and function of the human {organ_name}. {description}"
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(prompt)
    return response.text if hasattr(response, 'text') else str(response)
