from typing import Dict, Any, List
from .base import AIStep
from .llm_interface import LLMInterface
from termcolor import colored
import yaml
from utils.configuration import config
from .prompt import Prompt

class ReasoningEngine(AIStep):
    def __init__(self):
        super().__init__(config.get("ai.prompts.roles.reasoning_engine"))
        self.modules = config.get("ai.prompts.modules")
        
    def generate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return super().generate(context)
