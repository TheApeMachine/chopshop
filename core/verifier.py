from typing import Dict, Any
from .base import AIStep
from termcolor import colored
from utils.configuration import config

class Verifier(AIStep):
    def __init__(self, *steps: AIStep):
        super().__init__(config.get("ai.prompts.roles.verifier"))
        
    def generate(self, context: Dict[str, Any]) -> Any:
        return super().generate(context)
