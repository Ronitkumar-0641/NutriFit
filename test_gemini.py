import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found!")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = "What should I eat before a morning workout? Give me a brief answer."
    print(f"\nSending prompt: {prompt}")
    
    response = model.generate_content(prompt)
    print(f"\nResponse received:")
    print(response.text)
    
except Exception as e:
    print(f"\nError: {e}")
    import traceback
    traceback.print_exc()