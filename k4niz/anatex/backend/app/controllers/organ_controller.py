from ..services.organ_service import get_organ_description
from ..services.gpt_service import get_ai_explanation

def get_organ_info(organ_name: str):
    description = get_organ_description(organ_name)
    ai_explanation = get_ai_explanation(organ_name, description)
    return {"organ": organ_name, "description": description, "ai_explanation": ai_explanation}
