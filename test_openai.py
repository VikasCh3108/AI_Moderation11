import openai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

def test_openai_connection():
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello, this is a test message."}]
        )
        print("API Key is working! Response received:")
        print(response.choices[0].message.content)
        return True
    except Exception as e:
        print("Error testing OpenAI API key:")
        print(e)
        return False

if __name__ == "__main__":
    print("OpenAI API Key:", os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "Not found")
    test_openai_connection()
