import dspy

class UserUnderstandingSignature(dspy.Signature):
    """Analyzes user utterances to infer style, tone, intent, and provide persona hints."""
    user_utterances = dspy.InputField(desc="A list of the user's recent messages.")
    
    inferred_style = dspy.OutputField(desc="Inferred communication style (e.g., formal, informal).")
    emotional_tone = dspy.OutputField(desc="Inferred emotional tone (e.g., happy, frustrated).")
    intent_keywords = dspy.OutputField(desc="Primary intent keywords from the user's messages.", type=list[str])
    persona_hints = dspy.OutputField(desc="Hints for the chatbot's persona (e.g., be direct, be empathetic).", type=list[str])

class UserUnderstanding(dspy.Module):
    """DSPy module for Initial User Understanding (PRD 5.1)."""
    def __init__(self):
        super().__init__()
        # As per PRD, ChainOfThought is suitable here to allow reasoning.
        self.generate_insights = dspy.ChainOfThought(UserUnderstandingSignature)

    def forward(self, user_utterances):
        # Ensure user_utterances is a list, as expected by the signature if it's meant to process multiple.
        # If only the last utterance is needed, the signature and this call might be simplified.
        insights = self.generate_insights(user_utterances=user_utterances)
        return insights

if __name__ == '__main__':
    # This section is for testing the module individually.
    # It requires dspy_config to be run or LM to be configured.
    from app.dspy_config import configure_lm
    try:
        configure_lm() # Ensure LM is configured
        print("LM Configured for UserUnderstanding test.")

        # Test case 1: Simple frustrated user
        test_understanding = UserUnderstanding()
        utterances1 = ["This thing is broken! I need help now."]
        result1 = test_understanding(user_utterances=utterances1)
        print(f"\nTest Case 1 Input: {utterances1}")
        print(f"Inferred Style: {result1.inferred_style}")
        print(f"Emotional Tone: {result1.emotional_tone}")
        print(f"Intent Keywords: {result1.intent_keywords}")
        print(f"Persona Hints: {result1.persona_hints}")

        # Test case 2: More inquisitive user
        utterances2 = ["Hmm, I'm not sure how this feature works. Can you explain it clearly?"]
        result2 = test_understanding(user_utterances=utterances2)
        print(f"\nTest Case 2 Input: {utterances2}")
        print(f"Inferred Style: {result2.inferred_style}")
        print(f"Emotional Tone: {result2.emotional_tone}")
        print(f"Intent Keywords: {result2.intent_keywords}")
        print(f"Persona Hints: {result2.persona_hints}")

    except Exception as e:
        print(f"Error during UserUnderstanding test: {e}")
        print("Ensure GEMINI_API_KEY is set in .env and dspy_config.py runs successfully.") 