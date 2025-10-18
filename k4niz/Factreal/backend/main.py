"""FastAPI application entry point for FactReal."""
from __future__ import annotations

from fastapi import FastAPI
from .controllers.classify_controller import (
    ClassifyController,
    ClassifyRequest,
    ClassifyResponse,
)

from .routes.classify_router import router as classify_router
from .routes.explain_router import router as explain_router

app = FastAPI(title="FactReal", version="0.1.0")


@app.get("/")
def health() -> dict:
    return {"status": "ok", "service": "FactReal"}


app.include_router(classify_router)
app.include_router(explain_router)


# Convenience: allow POST / to behave like /classify for ease of testing
_root_classify_controller = ClassifyController()


@app.post("/", response_model=ClassifyResponse)
def classify_root(req: ClassifyRequest) -> ClassifyResponse:
    return _root_classify_controller.classify(req)
