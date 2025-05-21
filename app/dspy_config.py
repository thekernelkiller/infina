import dspy
import os
from dotenv import load_dotenv

def configure_lm():
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")

    try:
        gemini_lm = dspy.LM(model='gemini/gemini-2.0-flash', api_key=gemini_api_key)
        dspy.settings.configure(lm=gemini_lm)
        print("DSPy configured with Gemini model: gemini-2.0-flash")
        return gemini_lm
    except Exception as e:
        print(f"Error configuring Gemini LM: {e}")
        print("Please ensure your GEMINI_API_KEY is correct and you have access to the specified model.")
        raise

if __name__ == '__main__':
    try:
        configure_lm()
        print(f"Current DSPy LM: {dspy.settings.lm}")
    except Exception as e:
        print(f"Failed to initialize and test DSPy LM: {e}") 