"""FastAPI router for explanation endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from ..controllers.explain_controller import (
    ExplainController,
    ExplainRequest,
    ExplainResponse,
)


router = APIRouter(prefix="/explain", tags=["explain"])
controller = ExplainController()


@router.post("", response_model=ExplainResponse)
def explain(req: ExplainRequest) -> ExplainResponse:
    """Generate an explanation for a text and label."""
    return controller.explain(req)
