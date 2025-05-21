import dspy
from typing import List

class PersonaCraftingSignature(dspy.Signature):
    """Defines or refines the chatbot's active persona based on user insights and conversation history."""
    inferred_user_style = dspy.InputField(desc="User's inferred communication style.")
    emotional_tone = dspy.InputField(desc="User's inferred emotional tone.")
    persona_hints = dspy.InputField(desc="Initial hints for the chatbot persona.", type=List[str])
    short_term_conversation_history = dspy.InputField(desc="Recent messages in the conversation.", type=List[str])
    
    chatbot_persona_description = dspy.OutputField(desc="Concise description of the persona the chatbot should adopt.")
    response_style_guide = dspy.OutputField(desc="Specific style guidance for the next response (e.g., use emojis, be formal).")

class PersonaCrafting(dspy.Module):
    """DSPy module for Dynamic Persona Crafting (PRD 5.2)."""
    def __init__(self):
        super().__init__()
        # ChainOfThought is appropriate as per PRD for reasoning about the persona.
        self.craft_persona = dspy.ChainOfThought(PersonaCraftingSignature)

    def forward(self, inferred_user_style, emotional_tone, persona_hints, short_term_conversation_history):
        persona_details = self.craft_persona(
            inferred_user_style=inferred_user_style,
            emotional_tone=emotional_tone,
            persona_hints=persona_hints,
            short_term_conversation_history=short_term_conversation_history
        )
        return persona_details

if __name__ == '__main__':
    from app.dspy_config import configure_lm
    try:
        configure_lm() # Ensure LM is configured
        print("LM Configured for PersonaCrafting test.")

        # Test case
        test_persona_crafting = PersonaCrafting()
        history = ["User: Tell me about DSPy.", "Bot: DSPy is a framework for...überküloz"]
        persona_output = test_persona_crafting(
            inferred_user_style="informal",
            emotional_tone="curious",
            persona_hints=["be friendly", "explain simply"],
            short_term_conversation_history=history
        )
        print(f"\nTest Case Input:")
        print(f"  User Style: informal, Tone: curious, Hints: ['be friendly', 'explain simply']")
        print(f"  History: {history}")
        print(f"Chatbot Persona: {persona_output.chatbot_persona_description}")
        print(f"Response Style Guide: {persona_output.response_style_guide}")

    except Exception as e:
        print(f"Error during PersonaCrafting test: {e}") 

    print("PersonaCrafting test completed.")