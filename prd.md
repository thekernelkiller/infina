Okay, this is shaping up to be a well-defined and exciting project! Let's craft a detailed Technical Product Requirements Document (PRD).

## Technical Product Requirements Document: Adaptive Personal AI Companion

**1. Introduction & Vision**

This document outlines the technical requirements for building an Adaptive Personal AI Companion. The core vision is to create a chatbot that offers a deeply personalized and adaptive conversational experience. Unlike generic chatbots, this companion will quickly (within 1-2 interactions) "kick into" a persona suitable and compatible with the user's communication style, tone, intent, and emotional state. It will continuously refine this persona based on ongoing conversation and leverage long-term memory to enhance personalization across sessions. The system will be powered by an optimized small language model (with on-device deployment as a long-term goal) and will possess proactive agentic capabilities to assist the user effectively.

**2. Core Idea & Guiding Principles**

*   **Deep Personalization:** The chatbot should feel uniquely attuned to each user.
*   **Rapid Adaptation:** The system must quickly infer and adopt a compatible persona.
*   **Continuous Learning:** The chatbot's understanding of the user and its persona should evolve.
*   **Proactive Assistance:** Agentic capabilities should be used intelligently to aid the user, sometimes without explicit requests.
*   **Efficiency & Privacy:** Prioritize small models and local data storage (SQLite) for potential on-device deployment and enhanced privacy.
*   **Modularity & Optimization (DSPy):** Leverage DSPy for structured development, enabling robust optimization of the small LM's performance.
*   **User-Centric Design:** The system should minimize the need for users to "prompt engineer" their requests.

**3. Non-Functional Requirements (NFRs)**

*   **Responsiveness:**
    *   Persona "kick-in" should be noticeable within 1-2 user interactions.
    *   Typical chatbot response latency should be interactive (e.g., < 2-3 seconds for core responses, agentic tasks may take longer and should indicate progress).
*   **Personalization Depth:** The system should demonstrate increasingly nuanced understanding and adaptation to a user over multiple sessions.
*   **Consistency:** The adopted persona for a user should remain reasonably consistent within a session and evolve predictably across sessions.
*   **Accuracy (Agentic Tasks):** Information provided through web search or calculations must be accurate. Reports should be factual and well-summarized.
*   **Resource Efficiency:** Optimized for small LMs. Memory and CPU usage should be mindful of potential on-device deployment.
*   **Scalability (User Base):** While the initial focus is a personal bot, the architecture should allow for managing multiple distinct user profiles if scaled.
*   **Maintainability:** The system, built with DSPy, should be modular, allowing individual components (persona inference, response generation, tools) to be updated or optimized independently.
*   **Upgradability:** The architecture should facilitate iterative improvements and the addition of new features or agentic capabilities without requiring complete rewrites.
*   **Privacy:** User data, especially long-term memory and PII, must be handled securely. SQLite for local storage is a first step. No sensitive data should be logged externally without explicit user consent.

**4. Technical Stack Summary**

*   **Core Logic Framework:** DSPy
*   **Programming Language:** Python
*   **Language Models (LMs):**
    *   **Primary (Student):** A small, efficient LM (e.g., a 1-3B parameter model like Phi-3-mini, Llama-3.1-8B-Instruct-slim (if available/quantized), or similar, suitable for potential on-device).
    *   **Teacher/Optimizer LM:** A larger, capable model (e.g., GPT-4o-mini, GPT-4o) for bootstrapping, data generation, and optimization phases.
*   **Frontend:** Streamlit (for demonstration and interaction)
*   **Backend (if deployed as a service):** FastAPI
*   **Long-Term Memory:** SQLite3 (local database per user or centralized with user separation)
*   **Web Search Tool:** Serper API
*   **Calculator Tool:** Python's `eval()` (safeguarded) or a dedicated math expression parsing library.

**5. Functional Features & Iterative Implementation Plan**

---

**Phase 1: MVP - Core Chatbot with Initial Persona Adaptation**

**Goal:** Establish the basic conversational loop with rapid persona "kick-in."

**5.1. Feature: Initial User Understanding**
    *   **Description:** On receiving the first 1-2 messages from a new user (or a user starting a new session), this module analyzes the text to make initial inferences.
    *   **Functionality:**
        *   Infers user's communication style (e.g., formal/informal, concise/verbose).
        *   Infers emotional tone (e.g., happy, frustrated, neutral, curious).
        *   Identifies primary intent keywords.
        *   Suggests initial hints for the chatbot's persona (e.g., "be direct," "be empathetic," "use technical language").
    *   **DSPy Implementation:**
        *   **Module:** `dspy.ChainOfThought` (to allow reasoning about the cues).
        *   **Signature:** `user_utterances: list[str] -> inferred_style: str, emotional_tone: str, intent_keywords: list[str], persona_hints: list[str]`
        *   **Data for Optimization:** Handcrafted examples of short user inputs mapped to desired inferences. E.g., `[{ "user_utterances": ["This thing is broken!"], "inferred_style": "direct", "emotional_tone": "frustrated", ...}]`
        *   **Metric:** Qualitative assessment initially, or an LM-as-judge comparing module output to handcrafted ideal inferences.
    *   **Streamlit Display:** (Internal state, not directly displayed unless for debugging).

**5.2. Feature: Dynamic Persona Crafting**
    *   **Description:** Based on the output from the "Initial User Understanding" module and ongoing conversation, this module defines or refines the chatbot's active persona.
    *   **Functionality:** Generates a concise description of the persona the chatbot should adopt for the *next* interaction.
    *   **DSPy Implementation:**
        *   **Module:** `dspy.ChainOfThought`.
        *   **Signature:** `inferred_user_style: str, emotional_tone: str, persona_hints: list[str], short_term_conversation_history: list[str] -> chatbot_persona_description: str, response_style_guide: str`
        *   **Data for Optimization:** Examples linking user characteristics and conversation snippets to ideal persona descriptions. E.g., `[{ "inferred_user_style": "informal", "emotional_tone": "curious", ..., "chatbot_persona_description": "A friendly and curious assistant that explains things simply."}]`
        *   **Metric:** Qualitative assessment of persona appropriateness.
    *   **Streamlit Display:** (Internal state, but for debugging, one could display the `chatbot_persona_description`).

**5.3. Feature: Persona-Driven Response Generation**
    *   **Description:** Generates the chatbot's actual response, ensuring it aligns with the crafted persona and addresses the user's query.
    *   **Functionality:** Takes user query, history, and the persona description to produce a natural language response.
    *   **DSPy Implementation:**
        *   **Module:** `dspy.ChainOfThought` (to allow reasoning about how to apply the persona).
        *   **Signature:** `user_query: str, short_term_conversation_history: list[str], chatbot_persona_description: str, response_style_guide: str -> chatbot_response: str`
        *   **Data for Optimization:** Examples of (user query, history, persona) -> ideal chatbot response.
        *   **Metric:** Combination of fluency, relevance, and persona adherence (could be judged by an LM).
    *   **Streamlit Display:** Displays `user_query` and `chatbot_response` in a chat interface.

**5.4. Feature: Basic Session Memory**
    *   **Description:** Maintains the history of the current conversation.
    *   **Functionality:** Stores a list of user utterances and chatbot responses for the current session.
    *   **DSPy Implementation:** Managed as Python lists passed as arguments to DSPy modules (e.g., `short_term_conversation_history`). No specific DSPy module, but prompts will be optimized to use this field.
    *   **Streamlit Display:** The chat interface inherently displays session memory.

---

**Phase 2: Long-Term Memory & Continuous Adaptation**

**Goal:** Enable cross-session personalization and continuous persona refinement.

**5.5. Feature: SQLite3 Long-Term User Memory**
    *   **Description:** Persistent storage for user-specific data.
    *   **Functionality:**
        *   Database schema (as discussed previously): `UserSettings`, `UserInterests`, `InteractionSummaries`.
        *   Python functions to CRUD data from SQLite.
    *   **DSPy Implementation:** Standard Python `sqlite3` module. These functions will be wrapped as `dspy.Tool`s if needed by an agent, or called directly by Python logic.
    *   **Streamlit Display:** Not directly, but a "User Profile" debug view could be added.

**5.6. Feature: Long-Term Memory Retrieval**
    *   **Description:** Fetches relevant user profile information at the start of a session or when contextually needed.
    *   **Functionality:** Queries the SQLite DB for the current user's settings, past interaction summaries, or interests.
    *   **DSPy Implementation:**
        *   Can be a Python function called at session start.
        *   Or, a `dspy.Tool` if an agent needs to dynamically query it:
            *   **Tool:** `retrieve_user_profile_snippet(query_about_user: str) -> relevant_profile_info: str`
            *   The output `relevant_profile_info` feeds into the `DynamicPersonaCrafting` module.
        *   **Data/Metric:** Optimization focuses on the *consuming* modules being able to use this retrieved info.
    *   **Streamlit Display:** (Internal state).

**5.7. Feature: End-of-Session Profile Update**
    *   **Description:** Summarizes key learnings from a conversation to update the long-term memory.
    *   **Functionality:** Analyzes the completed conversation and identifies changes/additions to user style preferences, new interests, or successful persona elements.
    *   **DSPy Implementation:**
        *   **Module:** `dspy.ChainOfThought`.
        *   **Signature:** `full_conversation_history: list[str], existing_user_profile: str -> profile_update_summary: str, new_persona_notes: list[str], new_interest_tags: list[str]`
        *   The outputs are then written to SQLite by a Python function. This module runs asynchronously or post-session.
        *   **Data for Optimization:** Examples of conversation histories and the ideal concise updates for the profile.
        *   **Metric:** Accuracy of extracted preferences/interests.
    *   **Streamlit Display:** (Background process).

---

**Phase 3: Agentic Capabilities**

**Goal:** Equip the chatbot with proactive and complex tool-use abilities.

**5.8. Feature: Proactive Web Search (Serper API)**
    *   **Description:** The chatbot autonomously decides when to search the web to gather missing information or verify facts before responding.
    *   **Functionality:**
        1.  Pre-response decision module: Determines if web search is needed.
        2.  If yes, generates a search query.
        3.  Invokes the Serper web search tool.
        4.  Incorporates search results into its response generation.
    *   **DSPy Implementation:**
        *   **Decision Module:** `dspy.Predict` or `dspy.ChainOfThought`.
            *   **Signature:** `user_query: str, conversation_history: list[str] -> needs_web_search: bool, search_query: str`
        *   **Web Search Tool:** `dspy.Tool` wrapping a Python function that calls the Serper API.
            *   **Signature:** `query: str -> search_results: list[str]`
        *   **Response Generation Module (modified from 5.3):** Now takes optional `web_search_results` as input.
            *   **Signature:** `user_query: str, ..., web_search_results: list[str] -> chatbot_response: str`
        *   The overall flow can be orchestrated by a custom `dspy.Module` or a simple `dspy.ReAct` agent that first calls the decision module, then the tool, then the final response module.
        *   **Data for Optimization:** Examples where proactive search is beneficial vs. not, and what good search queries look like. Examples of synthesizing responses from search results.
        *   **Metric:** Response quality, factuality (potentially using an LM-as-judge for fact-checking against search results).
    *   **Streamlit Display:** Could indicate "Searching the web..." and optionally show top results used.

**5.9. Feature: Deep Search Report Generation**
    *   **Description:** The chatbot can conduct multi-step research using web search and synthesize a report on a given topic.
    *   **Functionality:**
        1.  User requests a report (e.g., "Tell me about the latest advancements in X").
        2.  The agent breaks this down into sub-queries, performs multiple web searches, reads/summarizes results, and synthesizes a final report.
    *   **DSPy Implementation:**
        *   **Agent Module:** `dspy.ReAct`.
        *   **Signature for ReAct:** `user_report_request: str -> synthesized_report: str`
        *   **Tools available to ReAct:** `web_search(query: str)`, `summarize_text(text_to_summarize: str, length_hint: str) -> summary: str`.
        *   **Data for Optimization:** Examples of report requests and high-quality reports (or trajectories of how a good report was formed).
        *   **Metric:** Report quality (comprehensiveness, coherence, factuality – likely requires LM-as-judge).
    *   **Streamlit Display:** Shows the final report. A "Show steps" could reveal the agent's search queries and intermediate summaries.

**5.10. Feature: Internal Calculator**
    *   **Description:** The chatbot can perform calculations when needed to answer a query or as part of its reasoning process.
    *   **Functionality:** Identifies when a calculation is needed, forms the expression, and uses a tool to get the result.
    *   **DSPy Implementation:**
        *   **Agent Module:** The same `dspy.ReAct` as in 5.9 (or a shared agent module).
        *   **Calculator Tool:** `dspy.Tool` wrapping Python's `eval()` (with appropriate safety/sandboxing if this were a public service, or a math expression library for on-device).
            *   **Signature:** `expression: str -> result: float`
        *   The ReAct agent learns when to invoke this tool.
        *   **Data/Metric:** Ensure the agent uses it correctly for math-related queries.
    *   **Streamlit Display:** Calculations can be shown as part of the chatbot's "thought" process or explicitly stated in the response.

---

**Phase 4: Background Personalized Curation**

**Goal:** Provide ongoing value to the user even when they are not actively chatting.

**5.11. Feature: Personalized Content Curation**
    *   **Description:** A background process periodically scans for new information relevant to the user's stored interests and curates a list of "news bites" or interesting links.
    *   **Functionality:**
        1.  Reads `UserInterests` from SQLite.
        2.  Generates relevant search queries.
        3.  Uses Serper to fetch news/articles.
        4.  Filters and summarizes relevant items.
        5.  Stores curated items in the `CuratedContent` table in SQLite.
    *   **DSPy Implementation (for the background script):**
        *   **Query Generation Module:** `dspy.ChainOfThought`.
            *   **Signature:** `user_interests: list[str] -> proactive_search_queries: list[str]`
        *   **Filtering/Summarization Module:** `dspy.Predict` or `dspy.ChainOfThought`.
            *   **Signature:** `article_content: str, user_interests: list[str] -> is_relevant: bool, short_summary: str, relevance_score: float`
        *   This is *not* part of the real-time chatbot but a separate Python script run on a schedule.
    *   **Streamlit Display:**
        *   A dedicated section/tab "Your Personalized Feed" where the user can see these curated items.
        *   The main chatbot could proactively offer: "I found a few articles about [topic X] you might like. Want to see them?"

---

**General Optimization Strategy:**

*   For each phase, once the modules are defined, create a small set of high-quality examples (input-output pairs for the specific module or the end-to-end phase).
*   Use a DSPy optimizer (e.g., `dspy.MIPROv2` with a larger teacher LM like GPT-4o-mini, or `dspy.BootstrapFewShotWithRandomSearch`) to compile each module or the composed program, optimizing its prompts (instructions and few-shot examples) for the target small LM.
*   If pursuing on-device and needing maximum efficiency/performance from the small LM, explore `dspy.BootstrapFinetune` after initial prompt optimization.
*   Metrics are key: iterate on them. For persona compatibility, an LM-as-judge module might be needed:
    *   Signature: `user_input_style: str, chatbot_response_style: str, target_persona: str -> compatibility_score: float, feedback: str`

This PRD provides a roadmap. Each feature will require detailed design of its signatures, thoughtful data creation for optimization, and careful metric definition. The power of DSPy will be in making each of these components learnable and adaptable to your specific goals and the chosen small LM.