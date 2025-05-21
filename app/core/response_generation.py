import dspy
from typing import List

class ResponseGenerationSignature(dspy.Signature):
    user_query = dspy.InputField(desc="The user's current query/message.")
    short_term_conversation_history = dspy.InputField(desc="Recent messages in the conversation.", type=List[str])
    chatbot_persona_description = dspy.InputField(desc="The active persona description for the chatbot.")
    response_style_guide = dspy.InputField(desc="Specific style guidance for this response.")
    
    chatbot_response = dspy.OutputField(desc="The natural language response from the chatbot.")

class ResponseGeneration(dspy.Module):
    def __init__(self):
        super().__init__()
        self.generate_response = dspy.ChainOfThought(ResponseGenerationSignature)

    def forward(self, user_query, short_term_conversation_history, chatbot_persona_description, response_style_guide):
        response = self.generate_response(
            user_query=user_query,
            short_term_conversation_history=short_term_conversation_history,
            chatbot_persona_description=chatbot_persona_description,
            response_style_guide=response_style_guide
        )
        return response

if __name__ == '__main__':
    from app.dspy_config import configure_lm
    try:
        configure_lm()
        print("LM Configured for ResponseGeneration test.")

        test_response_gen = ResponseGeneration()
        history = ["User: Hi there!", "Bot: Hello! How can I help you today?"]
        response_output = test_response_gen(
            user_query="What is DSPy?",
            short_term_conversation_history=history,
            chatbot_persona_description="A helpful and slightly formal assistant.",
            response_style_guide="Answer clearly and concisely."
        )
        print(f"\nTest Case Input:")
        print(f"  User Query: What is DSPy?")
        print(f"  History: {history}")
        print(f"  Persona: A helpful and slightly formal assistant.")
        print(f"  Style Guide: Answer clearly and concisely.")
        print(f"Chatbot Response: {response_output.chatbot_response}")

    except Exception as e:
        print(f"Error during ResponseGeneration test: {e}") 