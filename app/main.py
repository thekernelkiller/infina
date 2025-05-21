import streamlit as st
from dspy_config import configure_lm
from core.user_understanding import UserUnderstanding
from core.persona_crafting import PersonaCrafting
from core.response_generation import ResponseGeneration
from core.session_memory import SessionMemory

st.set_page_config(
    page_title="Adaptive AI Companion",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

def initialize_session_state():
    if "lm_configured" not in st.session_state:
        st.session_state.lm_configured = False
    if "error_message" not in st.session_state:
        st.session_state.error_message = None
    if "chat_session" not in st.session_state:
        st.session_state.chat_session = None
    if "user_understanding_module" not in st.session_state:
        st.session_state.user_understanding_module = None
    if "persona_crafting_module" not in st.session_state:
        st.session_state.persona_crafting_module = None
    if "response_generation_module" not in st.session_state:
        st.session_state.response_generation_module = None
    if "current_persona_desc" not in st.session_state:
        st.session_state.current_persona_desc = "Default Assistant Persona"
    if "current_style_guide" not in st.session_state:
        st.session_state.current_style_guide = "Be helpful and informative."
    if "messages" not in st.session_state:
        st.session_state.messages = []

initialize_session_state()
if not st.session_state.lm_configured:
    with st.spinner("Configuring AI Model..."):
        try:
            configure_lm()

            user_understanding = UserUnderstanding()
            user_understanding.load("models/optimized_user_understanding_student.json")
            st.session_state.user_understanding_module = user_understanding
            
            persona_crafting = PersonaCrafting()
            persona_crafting.load("models/optimized_persona_crafting_student.json")
            st.session_state.persona_crafting_module = persona_crafting
            
            response_generation = ResponseGeneration()
            response_generation.load("models/optimized_response_generation_student.json")
            st.session_state.response_generation_module = response_generation
            
            st.session_state.chat_session = SessionMemory()
            st.session_state.lm_configured = True
            st.sidebar.success("AI Model Configured Successfully! (Gemini with Optimized Modules)")
        except Exception as e:
            st.session_state.error_message = f"Error initializing AI: {str(e)}"
            st.sidebar.error(st.session_state.error_message)
            st.error(f"Critical Error: Could not configure AI. Please check console and .env settings. Details: {e}")

st.title("🤖 Adaptive Personal AI Companion (Phase 1 MVP)")
st.caption("Powered by DSPy and Gemini")

if st.session_state.error_message:
    st.error(f"Initialization Error: {st.session_state.error_message}")
elif not st.session_state.lm_configured:
    st.warning("AI Model is not configured. Please check the sidebar and logs.")
else:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What's on your mind?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_session.add_message("user", prompt)
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.spinner("Thinking..."):
            try:
                user_utterances_for_understanding = [prompt] 

                understanding_output = st.session_state.user_understanding_module(
                    user_utterances=user_utterances_for_understanding
                )
                st.sidebar.subheader("User Understanding Output:")
                st.sidebar.json({
                    "style": understanding_output.inferred_style,
                    "tone": understanding_output.emotional_tone,
                    "keywords": understanding_output.intent_keywords,
                    "hints": understanding_output.persona_hints
                })

                history_for_persona = st.session_state.chat_session.get_formatted_history(max_turns=4)
                
                persona_output = st.session_state.persona_crafting_module(
                    inferred_user_style=understanding_output.inferred_style,
                    emotional_tone=understanding_output.emotional_tone,
                    persona_hints=understanding_output.persona_hints,
                    short_term_conversation_history=history_for_persona
                )
                st.session_state.current_persona_desc = persona_output.chatbot_persona_description
                st.session_state.current_style_guide = persona_output.response_style_guide
                st.sidebar.subheader("Dynamic Persona Output:")
                st.sidebar.write(f"**Persona:** {st.session_state.current_persona_desc}")
                st.sidebar.write(f"**Style Guide:** {st.session_state.current_style_guide}")

                history_for_response = st.session_state.chat_session.get_formatted_history(max_turns=10)
                response_output = st.session_state.response_generation_module(
                    user_query=prompt,
                    short_term_conversation_history=history_for_response,
                    chatbot_persona_description=st.session_state.current_persona_desc,
                    response_style_guide=st.session_state.current_style_guide
                )
                bot_response = response_output.chatbot_response

            except Exception as e:
                bot_response = f"Sorry, I encountered an error: {str(e)}"
                st.error(bot_response)
        
        st.session_state.messages.append({"role": "assistant", "content": bot_response})
        st.session_state.chat_session.add_message("bot", bot_response)
        with st.chat_message("assistant"):
            st.markdown(bot_response)

    st.sidebar.divider()
    st.sidebar.header("Session Info")
    if st.session_state.lm_configured:
        st.sidebar.write(f"**Current Persona:** {st.session_state.current_persona_desc}")
        st.sidebar.write(f"**Response Style:** {st.session_state.current_style_guide}")
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.session_state.chat_session.clear()
            st.session_state.current_persona_desc = "Default Assistant Persona (awaiting input)"
            st.session_state.current_style_guide = "Be helpful and informative."
            st.rerun()
    else:
        st.sidebar.warning("AI not fully initialized.")
