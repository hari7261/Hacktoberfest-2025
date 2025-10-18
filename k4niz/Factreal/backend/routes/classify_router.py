"""FastAPI router for classification endpoints."""
from __future__ import annotations

from fastapi import APIRouter

from ..controllers.classify_controller import (
    ClassifyController,
    ClassifyRequest,
    ClassifyResponse,
)


router = APIRouter(prefix="/classify", tags=["classify"])
controller = ClassifyController()


@router.post("", response_model=ClassifyResponse)
def classify(req: ClassifyRequest) -> ClassifyResponse:
    """Classify input text and return label, scores, and explanation."""
    return controller.classify(req)
