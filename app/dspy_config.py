import dspy
import os
from dotenv import load_dotenv

def configure_lm():
    """Loads API keys and configures the DSPy LM (Gemini)."""
    load_dotenv()
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file or environment variables.")

    # Configure Gemini
    # Note: model names might need adjustment based on exact availability
    # and your specific Gemini access (e.g., 'gemini-pro', 'gemini-1.5-flash-latest')
    try:
        # Corrected way to instantiate Gemini model using dspy.LM
        gemini_lm = dspy.LM(model='gemini/gemini-2.0-flash', api_key=gemini_api_key)
        # For more control, you can specify model arguments directly if supported by the Google integration through dspy.LM
        # e.g., gemini_lm = dspy.LM(model='gemini-1.5-flash-latest', api_key=gemini_api_key, temperature=0.7, max_output_tokens=500)
        dspy.settings.configure(lm=gemini_lm)
        print("DSPy configured with Gemini model: gemini-2.0-flash")
        return gemini_lm
    except Exception as e:
        print(f"Error configuring Gemini LM: {e}")
        print("Please ensure your GEMINI_API_KEY is correct and you have access to the specified model.")
        raise

if __name__ == '__main__':
    # This allows you to test the configuration directly
    try:
        configure_lm()
        print(f"Current DSPy LM: {dspy.settings.lm}")
        # Example of a simple prediction (will make an API call)
        # predict_test = dspy.Predict("question -> answer")
        # result = predict_test(question="What is the capital of France?")
        # print(f"Test prediction: {result.answer}")
    except Exception as e:
        print(f"Failed to initialize and test DSPy LM: {e}") 