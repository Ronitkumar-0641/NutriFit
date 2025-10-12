import os
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Use the latest stable Gemini model with JSON response configuration
model = genai.GenerativeModel(
    'gemini-2.0-flash',
    generation_config={
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,
    }
)

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the response.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error getting response from Gemini: {e}")
        import traceback
        traceback.print_exc()
        return "I'm sorry, I'm having trouble connecting to the AI service. Please try again later."


def extract_json_from_response(text: str) -> str:
    """
    Extract JSON from Gemini response, handling markdown code blocks and other formatting.
    """
    # Remove markdown code blocks if present
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', text, re.DOTALL)
    if json_match:
        return json_match.group(1)
    
    # Try to find JSON object directly
    json_match = re.search(r'\{.*\}', text, re.DOTALL)
    if json_match:
        return json_match.group(0)
    
    return text
