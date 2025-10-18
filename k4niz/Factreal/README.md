FactReal — AI Backend for Bias/Misinformation Detection
=======================================================

FactReal is an AI-powered backend system that detects bias, misinformation, and propaganda in text (e.g., social posts, articles). It returns classifications with confidence scores and explainable reasoning, and optionally performs lightweight fact checking.

- Tech: FastAPI, Hugging Face Transformers
- Targets: Hacktoberfest-friendly, modular, easy to extend

Features
--------
- Bias detection: neutral, biased, misleading, propaganda
- Explainable reasoning: natural language explanation
- Optional fact verification: Wikipedia / NewsAPI (stubs included)
- Modular layers: models → services → controllers → routes

Project Structure
-----------------
```
backend/
  models/
    bias_model.py          # Transformer zero-shot bias classifier (with offline fallback)
    reasoning_model.py     # Text-to-text reasoning generator (with offline fallback)
    fact_checker.py        # Optional fact check (Wikipedia/NewsAPI)
  services/
    preprocessing_service.py
    classification_service.py
    explainability_service.py
    api_service.py
  controllers/
    classify_controller.py
    explain_controller.py
  routes/
    classify_router.py
    explain_router.py
  utils/
    logger.py
    config.py
  data/
    sample_dataset.jsonl   # Small sample data to try
  scripts/
    sample_requests.py     # Example client calls
    run_server.ps1         # Windows: start dev server
  main.py                  # FastAPI app entry

requirements.txt           # Python dependencies
README.md                  # You are here
```

Cleanup
-------
If you see stray files like `controllers.py` or `models.py` in this folder root, they are not used by the modular backend and can be safely deleted.

Quickstart
----------
1) Create and activate a virtual environment (recommended).

2) Install requirements:
```powershell
pip install -r requirements.txt
```

3) Run the API server (Windows PowerShell):
```powershell
./backend/scripts/run_server.ps1
```
This starts Uvicorn with auto-reload at http://127.0.0.1:8000.

4) Try example requests in a new terminal:
```powershell
python ./backend/scripts/sample_requests.py
```
Or use the interactive docs at:
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

Environment Configuration
-------------------------
Environment variables (optional) are loaded via `utils/config.py`:
- MODEL_BIAS (default: "facebook/bart-large-mnli")
- MODEL_REASONING (default: "google/flan-t5-base")
- THRESHOLD_BIAS (default: 0.55)
- ENABLE_FACT_CHECK (default: false)
- NEWS_API_KEY (optional)

Create a `.env` file next to `requirements.txt` if desired:
```
MODEL_BIAS=facebook/bart-large-mnli
MODEL_REASONING=google/flan-t5-base
THRESHOLD_BIAS=0.6
ENABLE_FACT_CHECK=true
NEWS_API_KEY=...
```

Hacktoberfest Contribution Guide
--------------------------------
- Good first issues: implement new models, improve heuristics, add datasets, expand fact-checkers
- Coding style: type hints, docstrings, small functions, tests where reasonable
- Folder-first design: add new models in `backend/models/`, new services in `backend/services/`, and wire via controllers/routes
- Please add comments to every function you create; keep public APIs stable

Data & Models
-------------
- The code uses Hugging Face pipelines. If models can’t be downloaded (e.g., offline), the code falls back to safe heuristic baselines so the API keeps working for demos and local development.
- To change models, set env vars or edit `utils/config.py`.

License
-------
This project follows the repository’s LICENSE.
