# Ollama + SQLite — Project Documentation

This document collects the full context, walkthrough, and shareable copy for the "Ollama + SQLite" demo repository. Use this file to create a PDF for a LinkedIn post, or import into Napkin.ai for a visual narrative. It contains: background, architecture, installation, how the TOON format works, example runs and token comparisons, ready-to-post LinkedIn copy (short/medium/long), troubleshooting, and FAQs.

---

## About

This repository shows how to ground an LLM's answers in deterministic data taken from a local SQLite database. It demonstrates two approaches:

- Plain JSON context: Query results are converted to JSON and provided as the only context to the model.
- TOON-encoded context: A compact, human-readable tabular encoding (TOON) reduces tokens while preserving the needed structured information.

The goal: let a locally-run Ollama model answer questions using only the query results (to avoid hallucinations) and to compare token usage between JSON and TOON encodings.

Primary use cases:
- Reproducible demos for technical audiences
- Backend patterns for deterministic LLM responses
- Demonstrations of token-saving encodings for cost/performance

Target audience: engineers and data scientists interested in local LLM workflows, reproducible prompt engineering, and token efficiency techniques.

---

## Repository layout (what's important)

- `src/with_toon.py` — example: convert SQL rows to TOON and ask the Ollama model.
- `src/without_toon.py` — example: convert SQL rows to JSON and ask the Ollama model.
- `src/seeder.py` — generate a sample `users.db` using Faker.
- `src/initial.py` — a small demo of TOON encode/decode used for quick testing.
- `requirements.txt` — dependencies to install.
- `.gitignore`, `LICENSE` — housekeeping files.
- `docs/PROJECT_DOCUMENTATION.md` — this file.

---

## Concept & Contract (2–3 bullets)

- Input: a SQL query (SELECT) run locally against `users.db`.
- Output: a short, deterministic natural-language answer produced by an Ollama model, limited to the provided context.
- Error mode: if the DB is missing or the context lacks the answer, the model will return a clear fallback (explicitly asked to do so).

### Edge cases considered

- Empty query results: the system prompt instructs the model to say it couldn't find the information.
- Large result sets: TOON reduces token usage but very large result sets can still exceed local model limits; filter or paginate queries.
- Ollama offline or model not pulled: scripts handle exceptions and print a clear message.

---

## TOON: Compact encoding overview

TOON is a small, readable tabular encoding used in this project for compact context. Basic rules used here:

- For arrays of uniform objects (rows), represent the header once and present rows separated by new lines.
- Example:

```
[2,]{id,name}:
  1,Alice
  2,Bob
```

- Why TOON? It removes JSON punctuation overhead (braces, quotes) and can reduce token counts when sending structured tables to LLMs.

If you don't have a `toon_format` package installed, `src/initial.py` demonstrates the encoding/decoding used in this repo and can be used to reimplement the encoder.

---

## Installation (Windows PowerShell)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

Note: If `toon_format` is a local utility (not on PyPI), either remove it from `requirements.txt` and include the local implementation or install it from the correct source.

3. Ensure Ollama is running and a model is pulled (example):

```powershell
# Start Ollama per your local instructions (if applicable)
# Pull or ensure model exists, e.g.:
# ollama pull deepseek-r1:1.5b
```

---

## Seed sample data

```powershell
python src/seeder.py
# Creates users.db in repo root and prints a small sample of rows
```

If you prefer a smaller or larger sample, edit `src/seeder.py` and change the generation count.

---

## Run the examples

1) JSON version:

```powershell
python src/without_toon.py
```

2) TOON version:

```powershell
python src/with_toon.py
```

Expected behavior: each script queries the seeded `users` table, formats the rows (JSON or TOON), sends them to Ollama with a strict system prompt, and prints the model's response.

---

## Example queries and expected outputs

Example 1 (Pizza & >30):

- SQL used:

```sql
SELECT name, age, fav_food, city
FROM users
WHERE fav_food = 'Pizza' AND age > 30;
```

- Observed token counts (from test runs in this repo):

| Encoding | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|
| JSON (without TOON) | 265 | 389 | 654 |
| TOON | 181 | 308 | 489 |

Example 2 (age > 18):

| Encoding | Input tokens | Output tokens | Total tokens |
|---|---:|---:|---:|
| JSON (without TOON) | 2062 | 445 | 2507 |
| TOON | 819 | 1036 | 1855 |

These numbers demonstrate token savings and potential cost/performance benefits when using TOON in large contexts. Results will vary with model, text encoding, and system prompt.

---

## How the prompt enforces grounding

Both scripts use a two-part chat message: a strict system prompt plus a user prompt that includes the question and the entire contextual payload (JSON or TOON). The system prompt explicitly instructs the model:

- Answer using ONLY the provided context.
- If the context doesn't include the answer, say so.

This pattern is a practical way to minimize hallucinations in local LLM workflows.

---

## Troubleshooting

- Ollama connection error: ensure Ollama is running at `http://localhost:11434`. If you run Ollama on a different host/port, update the `Client(host=...)` call.
- Model error: pull the required model (`ollama pull <model>`), or change `OLLAMA_MODEL` in the scripts to a model you have.
- Missing package errors: install with `pip install -r requirements.txt` or add local modules to `PYTHONPATH` / include them in repo.
- Large context token limits: reduce query result size, filter columns, or summarize rows before sending.

---

## LinkedIn-ready copy

Use any of the following variants depending on the post length you prefer. Pair with a short GIF or a screenshot showing the example output for higher engagement.

Short (one-liner):

"Demo: Grounding local Ollama model answers in SQLite query results — includes a compact TOON encoding to reduce tokens and cost. Code + examples: <repo link>"

Medium (detailed):

"I built a small demo that forces an Ollama model to answer *only* from SQL query results. The repo compares plain JSON vs a compact TOON encoding to show token savings. It includes a seeder, runnable examples, and clear prompts to avoid hallucinations. Try it locally: seed the DB, run the examples, and compare token counts. Code: <repo link>"

```powershell
pandoc docs/PROJECT_DOCUMENTATION.md -o Ollama_SQLite_Demo.pdf --pdf-engine=xelatex
```
---

## FAQ

Q: Is TOON a standard library? A: Not a standard package — it's a compact, domain-specific encoding used here. If `toon_format` is not available on PyPI, include its implementation in the repo or use `src/initial.py` as a reference implementation.

Q: Can I run this in the cloud? A: Yes, but Ollama is designed as a local inference service — to run in cloud VMs, ensure the environment matches dependencies and that the model is available for the cloud instance.

Q: Which models work best? A: Smaller deterministic models reduce cost, but your choice depends on latency and quality. The repo uses `deepseek-r1:1.5b` as an example — replace with any Ollama-compatible model you have.

---

## License

This project uses the MIT License — see the top-level `LICENSE` file.

---

## Credits & acknowledgements

- Author: (Replace with your name here)
- Toy dataset generated with Faker (MIT compatible)
- TOON: small encoding idea used for compact tabular representations — adapt freely.

---

