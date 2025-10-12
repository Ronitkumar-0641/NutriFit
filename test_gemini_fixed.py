import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"API Key loaded: {api_key[:10]}..." if api_key else "No API key found!")

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    prompt = """You are a friendly, evidence-based AI assistant specializing exclusively in nutrition and fitness. 
Always keep responses on-topic and avoid medical diagnoses. 
Provide clear, actionable advice that's easy to understand and implement. 
Here is the conversation history:
- What should I eat before a morning workout?

Provide a motivating, practical answer with actionable tips. 
Keep your response concise but informative (2-4 paragraphs). 
If the conversation drifts away from nutrition or fitness, gently steer it back."""
    
    print(f"\nSending prompt to Gemini 2.0 Flash...")
    
    response = model.generate_content(prompt)
    print(f"\nResponse received:")
    print(response.text)
    print("\n✅ SUCCESS! Gemini API is working correctly!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()