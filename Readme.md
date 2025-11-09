# Ollama + SQLite — Query-grounded LLM examples

This repository demonstrates how to take SQL query results from a local SQLite database, format the results (JSON or a compact "TOON" encoding), and send them as the only context to an Ollama model so the model answers strictly from the provided data.

Why this repo?
- Shows how to ground LLM answers in data (avoid hallucinations).
- Compares plain JSON context with a compact TOON encoder to reduce tokens.
- Includes a small seeder to create sample data and quick example scripts.

Contents
- `src/with_toon.py` — TOON-encoded context + Ollama example
- `src/without_toon.py` — JSON context + Ollama example
- `src/seeder.py` — creates `users.db` with sample rows using Faker
- `src/initial.py` — small TOON encode/decode demo
- `.gitignore`, `requirements.txt`, `LICENSE`

Prerequisites
- Python 3.10+
- Ollama running locally (default: http://localhost:11434) and the model you intend to use pulled locally

Quick setup
1. Create a virtualenv and install deps (Windows PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Seed the database:

```powershell
python src/seeder.py
# creates users.db in the repo root
```

3. Run examples:

```powershell
python src/with_toon.py
python src/without_toon.py
```

Notes and tips
- The scripts force the model to answer ONLY from the provided context — the system prompt explicitly instructs the model to avoid external knowledge.
- TOON is a compact, human-readable tabular encoding used to reduce token usage. If `toon_format` is not available as a package in your environment, see `src/initial.py` to understand the format used in this repo.
- If Ollama raises connection or model errors, ensure Ollama is running and you have pulled the chosen model. Example: `ollama pull deepseek-r1:1.5b`

License
This project is released under the MIT license — see `LICENSE`.

Sharing on LinkedIn
- A short post: "Demo: grounding Ollama model answers in SQLite results (JSON vs TOON) — includes seeder and examples. Check it out: <repo link>"
- Add a short GIF or screenshot of the script output for better engagement.

If you'd like, I can also:
- rename `Readme.md` to `README.md`
- run a quick smoke test (run `seeder.py` and one example) in this environment and report the output
- open a PR-ready commit with these changes and a suggested GitHub repo description and topics

Output tokens 1036
Total tokens 1855


