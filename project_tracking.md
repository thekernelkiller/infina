adaptive_ai_companion/
├── .env                  # Environment variables (API keys, configs) - gitignored
├── .gitignore            # Specifies intentionally untracked files
├── Makefile              # Optional: for common commands (lint, test, run, setup)
├── README.md             # Project overview, setup, how to run, contribution guidelines
├── requirements.in       # Input file for pip-compile (abstract dependencies)
├── requirements.txt      # Pinned dependencies (generated by pip-compile)
│
├── app/                  # Main application logic
│   ├── __init__.py
│   ├── main.py             # Entry point (Streamlit app / FastAPI backend)
│   ├── agent/              # Phase 3: Agentic capabilities
│   │   ├── __init__.py
│   │   ├── agent_core.py     # Core ReAct agent logic (e.g., for 5.8, 5.9, 5.10)
│   │   ├── tools/            # dspy.Tool definitions
│   │   │   ├── __init__.py
│   │   │   ├── web_search_tool.py  # For PRD 5.8, 5.9
│   │   │   ├── calculator_tool.py  # For PRD 5.10
│   │   │   └── memory_tool.py      # For PRD 5.6 (if used as a dynamic tool)
│   │   └── decision_modules.py # DSPy modules for deciding to use tools (e.g., for 5.8)
│   │
│   ├── core/               # Phase 1 & 2: Core chatbot functionalities
│   │   ├── __init__.py
│   │   ├── user_understanding.py # PRD 5.1: Initial User Understanding module
│   │   ├── persona_crafting.py   # PRD 5.2: Dynamic Persona Crafting module
│   │   ├── response_generation.py# PRD 5.3: Persona-Driven Response Generation module
│   │   └── session_memory.py     # PRD 5.4: Basic Session Memory logic
│   │
│   ├── data_management/    # Phase 2: Long-term memory
│   │   ├── __init__.py
│   │   ├── sqlite_handler.py # PRD 5.5: SQLite3 CRUD operations
│   │   └── profile_updater.py  # PRD 5.7: End-of-Session Profile Update module
│   │
│   ├── background_tasks/   # Phase 4: Background personalized curation
│   │   ├── __init__.py
│   │   ├── content_curator.py  # PRD 5.11: Personalized Content Curation logic & modules
│   │   └── scheduler.py        # Optional: If custom scheduling logic is needed
│   │
│   └── dspy_config.py        # Centralized DSPy LM configuration, API key loading
│
├── data/                 # Data for training, evaluation, examples
│   ├── __init__.py
│   ├── examples/           # Handcrafted examples for DSPy modules (as per PRD)
│   │   ├── phase1_user_understanding.jsonl
│   │   ├── phase1_persona_crafting.jsonl
│   │   ├── phase1_response_generation.jsonl
│   │   ├── phase2_profile_update.jsonl
│   │   ├── phase3_agent_web_search_decision.jsonl
│   │   ├── phase3_agent_report_generation.jsonl # Trajectories or (request, report) pairs
│   │   └── phase4_content_curation.jsonl
│   │
│   ├── user_data/          # User-specific data (e.g., SQLite DBs) - gitignored
│   │   └── .gitkeep          # Ensures the directory is tracked if empty
│   │
│   └── curated_content/    # Stores output from background curation - gitignored
│       └── .gitkeep
│
├── scripts/       # DSPy optimization pipelines and compiled programs
│   ├── __init__.py
│   ├── optimization/ # Scripts to run DSPy optimizers for different phases/modules
│   │   ├── __init__.py
│   │   ├── optimize_persona_crafting.py
│   │   ├── optimize_user_understanding.py
│   │   ├── optimize_response_generation.py
│   │
│   └── models/  # Store optimized/compiled DSPy programs (e.g., JSONs)
│       ├── __init__.py
│       └── .gitkeep          # Consider if these should be gitignored or versioned
│
├── notebooks/            # Jupyter notebooks for experimentation, data analysis
│   ├── 00_dspy_quickstart_exploration.ipynb
│   ├── 01_data_preparation_and_analysis.ipynb
│   ├── 02_module_prototyping_user_understanding.ipynb
│   └── .gitkeep
│
├── tests/                # Unit and integration tests
│   ├── __init__.py
│   ├── conftest.py         # Pytest fixtures and shared test utilities
│   │
│   ├── unit/               # Unit tests for individual modules/functions
│   │   ├── __init__.py
│   │   ├── app/
│   │   │   ├── core/
│   │   │   │   ├── test_user_understanding.py
│   │   │   │   ├── test_persona_crafting.py
│   │   │   │   └── test_response_generation.py
│   │   │   ├── agent/
│   │   │   │   └── test_web_search_tool.py
│   │   │   └── data_management/
│   │   │       └── test_sqlite_handler.py
│   │   └── dspy_pipelines/ # Tests for optimization script helpers, etc.
│   │       └── ...
│   │
│   └── integration/        # Integration tests for module interactions / phases
│       ├── __init__.py
│       ├── test_phase1_mvp_flow.py
│       └── test_phase3_agent_proactive_search.py
│
└── metrics_and_evals/    # Scripts, definitions for evaluating DSPy performance
    ├── __init__.py
    ├── custom_metrics.py   # Custom evaluation metrics (e.g., LM-as-judge for persona from PRD)
    ├── evaluation_sets/    # Curated datasets for standardized evaluation runs (hold-out sets)
    │   ├── __init__.py
    │   ├── phase1_mvp_eval.jsonl
    │   ├── phase3_agent_eval.jsonl
    │   └── .gitkeep
    └── evaluation_scripts/ # Scripts to run evaluations and report metrics
        ├── __init__.py
        ├── evaluate_phase1_mvp.py
        └── .gitkeep
```

- default gemini model is `gemini-2.0-flash` and not anything else unless specified. 

## Rules for Maintaining project_tracking.md (AI Assistant Guidelines)

1.  **Purpose:** This document is the primary log for significant project milestones, decisions, and structural changes. It's not a minute-by-minute changelog but a high-level overview of progress.
2.  **Automation with User Oversight:** The AI assistant will propose updates to this file after major steps are completed or when explicitly asked. The user will always review and approve changes.
3.  **Conciseness:** Entries should be brief and to the point. Link to relevant documents (PRD, specific code files) where appropriate.
4.  **Chronological Order:** New updates should be added below existing ones, typically under a new dated section or by updating the status of existing items.
5.  **Focus on "What" and "Why":** Log what was done and briefly why (e.g., "Corrected `dspy_config.py` to use `dspy.LM` for Gemini, aligning with current DSPy best practices.").
6.  **PRD Alignment:** All logged activities should ideally trace back to requirements or goals outlined in `prd.md`. If new requirements emerge, ensure the PRD is updated first or in conjunction.
7.  **Codebase Structure:** Reflect significant changes to the directory structure or key file responsibilities here.
8.  **Model and Environment Notes:** Keep track of key model versions used (e.g., default LLMs, teacher/student models for optimization) and critical environment setup details if they change.
9.  **Clarity on "Done":** When a task is marked as "complete," it implies it meets the immediate requirements. Further iterations or improvements might still occur in later phases.
10. **Pre-computation/Pre-analysis:** Before proposing major code changes or new file structures, the AI should explicitly state it will review relevant documentation (like the PRD, existing `project_tracking.md` entries, or specific files) to ensure alignment and avoid redundant suggestions.

## Project Update Log - Phase 1 Optimization Complete

**Date:** $(date +%Y-%m-%d)

**Summary:**
Phase 1 data creation and DSPy module optimization are complete. Example datasets for `UserUnderstanding`, `PersonaCrafting`, and `ResponseGeneration` were created and used to optimize the respective student models (`gemini/gemini-2.0-flash`) using `gemini-2.5-flash-preview-05-20` as the teacher. Optimized models are saved in the `models/` directory.

**Phase 1 Implementation Status:**

*   **Core Modules & Integration (Complete & Functional):**
    *   `app/core/user_understanding.py` (PRD 5.1)
    *   `app/core/persona_crafting.py` (PRD 5.2)
    *   `app/core/response_generation.py` (PRD 5.3)
    *   `app/core/session_memory.py` (PRD 5.4)
    *   Streamlit UI in `app/main.py` successfully integrates these modules.
*   **DSPy LM Configuration:** Uses `gemini/gemini-2.0-flash` via `dspy.LM`.
*   **Data Creation for Optimization (Complete):**
    *   `data/examples/phase1_user_understanding.jsonl` (25 examples)
    *   `data/examples/phase1_persona_crafting.jsonl` (25 examples)
    *   `data/examples/phase1_response_generation.jsonl` (25 examples)
*   **DSPy Optimization (Complete):**
    *   Optimization scripts created and run:
        *   `scripts/optimization/optimize_user_understanding.py`
        *   `scripts/optimization/optimize_persona_crafting.py`
        *   `scripts/optimization/optimize_response_generation.py`
    *   Optimized student models saved:
        *   `models/optimized_user_understanding_student.json`
        *   `models/optimized_persona_crafting_student.json`
        *   `models/optimized_response_generation_student.json`

**Remaining for Full Phase 1 Completion (as per PRD & DSPy workflow):**

1.  **Define Metrics & Evaluation:**
    *   Establish initial metrics (qualitative or quantitative, potentially LM-as-judge later) for evaluating the performance of `UserUnderstanding`, `PersonaCrafting`, and `ResponseGeneration` modules, as specified in PRD sections 5.1, 5.2, 5.3.
    *   Develop evaluation scripts (e.g., `metrics_and_evals/evaluation_scripts/evaluate_phase1_mvp.py`).
    *   Create a hold-out evaluation dataset (e.g., `metrics_and_evals/evaluation_sets/phase1_mvp_eval.jsonl`).

**Next Immediate Steps:**

*   Define and implement evaluation metrics and scripts for Phase 1 modules.
*   Start developing unit tests for the created modules.

--- 
## Project Update Log - Phase 1 MVP Operational

**Date:** $(date +%Y-%m-%d)

**Summary:**
User confirmed the Phase 1 Streamlit application (`app/main.py`) is operational. The `app/dspy_config.py` was manually updated by the user to use `gemini/gemini-2.0-flash` as the default Gemini model, which is now the project's default.

**Phase 1 Implementation Status:**

*   **Core Modules & Integration (Complete & Functional):**
    *   `app/core/user_understanding.py` (PRD 5.1)
    *   `app/core/persona_crafting.py` (PRD 5.2)
    *   `app/core/response_generation.py` (PRD 5.3)
    *   `app/core/session_memory.py` (PRD 5.4)
    *   Streamlit UI in `app/main.py` successfully integrates these modules, establishing the basic conversational loop.
*   **DSPy LM Configuration:** Uses `gemini/gemini-2.0-flash` via `dspy.LM`.

**Remaining for Full Phase 1 Completion (as per PRD & DSPy workflow):**

1.  **Data Creation for Optimization:**
    *   Develop handcrafted example datasets (`.jsonl` format) for the core Phase 1 DSPy modules. These examples will be used by DSPy optimizers.
    *   Target files:
        *   `data/examples/phase1_user_understanding.jsonl`
        *   `data/examples/phase1_persona_crafting.jsonl`
        *   `data/examples/phase1_response_generation.jsonl`

2.  **Define Metrics & Evaluation:**
    *   Establish initial metrics (qualitative or quantitative, potentially LM-as-judge later) for evaluating the performance of `UserUnderstanding`, `PersonaCrafting`, and `ResponseGeneration` modules, as specified in PRD sections 5.1, 5.2, 5.3.

3.  **DSPy Optimization:**
    *   Apply a DSPy optimizer (e.g., `BootstrapFewShotWithRandomSearch`) to the Phase 1 modules using the created example data. This aims to improve the zero-shot performance by optimizing prompts and few-shot examples for the `gemini/gemini-2.0-flash` model.
    *   This involves creating optimization scripts (e.g., `dspy_pipelines/optimization_scripts/optimize_phase1_mvp.py`).

**Next Immediate Steps:**

*   Begin drafting and creating the example data (`.jsonl` files) for the three core DSPy modules of Phase 1.
*   Start developing unit tests for the created modules.