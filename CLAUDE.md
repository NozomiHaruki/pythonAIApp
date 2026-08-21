# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

A personal, single-user AI writing tool built with Streamlit and the Gemini API (`google-genai` SDK). All UI text and prompts are in Japanese. There is no database and no authentication by design.

## Commands

```bash
# Setup (Windows / Git Bash)
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt

# Configure API key: copy .env.example to .env and set GEMINI_API_KEY
# (or enter the key directly in the app's sidebar at runtime)

# Run the app
.venv/Scripts/python.exe -m streamlit run app.py

# Compile-check all source (there is no pytest/lint config or test suite in this repo)
.venv/Scripts/python.exe -m py_compile app.py core/*.py pages/*.py
```

## Architecture

- **`app.py`** — entry point / home page. Relies on Streamlit's file-based multipage convention: files under `pages/` are auto-listed in the sidebar, ordered and icon-labeled by their `N_<emoji>_<name>.py` filename.
- **`core/gemini_client.py`** — the single point of contact with the Gemini API. Two entry points:
  - `generate_text(prompt, system_instruction)` — blocking call, returns the full string.
  - `generate_text_stream(prompt, system_instruction)` — generator of text chunks, designed to be passed directly to `st.write_stream()`.
  Both read `model` / `temperature` / `api_key` from `st.session_state` (populated by `render_sidebar()`) and call `st.stop()` on a missing key or API error, so calling pages don't implement their own error handling.
- **`core/ui.py`** — shared UI helpers used by every page:
  - `render_sidebar()` — must be called near the top of every page; sets `st.session_state.api_key` / `model` / `temperature`. Defaults `api_key` from `GEMINI_API_KEY` in `.env` via `python-dotenv`.
  - `render_page_header(title, description)`
  - `render_result(text, filename)` — renders a copyable `st.text_area` plus a download button; called at the end of every tool page.
- **`pages/N_<emoji>_<name>.py`** — one file per writing tool (blog post writer, email reply writer, summarizer, proofreader/rewriter, SNS post generator, translator, title/catchphrase generator). Every page follows the same shape:
  1. `st.set_page_config()`
  2. `render_sidebar()`
  3. `render_page_header()`
  4. input widgets → build a Japanese prompt string + `system_instruction`
  5. `st.write_stream(generate_text_stream(prompt, system_instruction))` inside a bordered `st.container`
  6. `render_result(result, filename)`

  When adding a new writing tool, copy this pattern rather than inventing a new structure.

## Conventions

- `st.session_state` keys `api_key`, `model`, `temperature` are the shared contract between `render_sidebar()` and `core/gemini_client.py` — any new page must call `render_sidebar()` before generating text.
- Model choice is intentionally kept flexible: `core/ui.py`'s `MODEL_OPTIONS` list includes a manual-entry fallback since Gemini model IDs change over time. Don't hardcode a single model ID elsewhere.
- All prompts sent to Gemini, and all UI copy, are written in Japanese to match the target user.
