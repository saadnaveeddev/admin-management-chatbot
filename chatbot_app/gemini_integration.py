import google.generativeai as genai
import os

def configure_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

def get_gemini_response(prompt):
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

def parse_command(command):
    # This is a placeholder. In a real application, you'd use a more sophisticated prompt
    # and potentially function calling with Gemini to extract structured data.
    # For now, we'll just return the command as is and expect the Streamlit app
    # to handle basic keyword matching or simple parsing.
    return command


