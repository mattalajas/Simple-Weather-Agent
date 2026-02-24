# Simple Weather Agent

A minimal Python agent that:

1. Accepts a user question about weather and activities.
2. Uses an LLM with tool-calling.
3. Calls a weather API tool (`Open-Meteo`).
4. Injects forecast data back into the prompt.
5. Returns a final natural-language answer.

## Requirements

- Python 3.10+
- Gemini API key

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment template:

```bash
copy .env.example .env
```

4. Set `GEMINI_API_KEY` in `.env`.
5. Run:

```bash
python -m src.main "What is the weather in Seattle tomorrow and what should I do?"
```

## Project Layout

See `src/` and `tests/` directories for the scaffolded architecture.
