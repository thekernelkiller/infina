# Adaptive Personal AI Companion

This project aims to build an Adaptive Personal AI Companion as outlined in the PRD (`prd.md`).

## Setup

1.  **Clone the repository.**
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
3.  **Install `pip-tools`:**
    ```bash
    pip install pip-tools
    ```
4.  **Create `requirements.in`** with the specified dependencies.
5.  **Compile and install requirements:**
    ```bash
    pip-compile requirements.in -o requirements.txt
    pip install -r requirements.txt
    ```
6.  **Create a `.env` file** in the project root and add your `GEMINI_API_KEY`:
    ```env
    GEMINI_API_KEY="your_gemini_key_here"
    ```

## Running the Application

(To be updated as development progresses - initially for Phase 1 Streamlit app)

```bash
streamlit run app/main.py
```

## Project Structure

Refer to `project_tracking.md` for the intended project structure.

## Development

-   **Linting/Formatting:** Uses Ruff. Configure your IDE or run `ruff check . --fix` and `ruff format .`.
-   **Tests:** Uses Pytest. Run `pytest` from the root directory. 