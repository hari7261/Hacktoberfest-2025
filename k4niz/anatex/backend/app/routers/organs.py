from fastapi import APIRouter
from ..controllers.organ_controller import get_organ_info

router = APIRouter()

@router.get("/organ-info/{organ_name}")
def organ_info(organ_name: str):
    return get_organ_info(organ_name)
