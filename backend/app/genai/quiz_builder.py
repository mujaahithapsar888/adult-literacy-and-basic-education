import os
import json
import google.generativeai as genai

# Fallback mock if API key isn't set
def generate_mock_quiz(topic: str):
    return json.dumps([
        {"q": f"What is a fundamental concept in {topic}?", "options": ["A", "B", "C", "D"], "answer": "A"},
        {"q": "Which of these represents a core principle?", "options": ["A", "B", "C", "D"], "answer": "B"}
    ])

def build_quiz_from_topic(topic: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "mock":
        return generate_mock_quiz(topic)
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f'''
        You are an expert adult education teacher.
        Create a 2-question multiple choice quiz about "{topic}".
        Return ONLY a valid JSON array of objects, with no markdown formatting or backticks.
        Each object must have 'q' (string), 'options' (array of 4 strings), and 'answer' (string).
        '''
        response = model.generate_content(prompt)
        # Attempt to parse to ensure it's valid JSON
        quiz_json = response.text.replace('```json', '').replace('```', '').strip()
        json.loads(quiz_json) 
        return quiz_json
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return generate_mock_quiz(topic)
