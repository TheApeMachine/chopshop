from abc import ABC, abstractmethod
from typing import Dict, Any
from .llm import llm
from utils.configuration import config
from termcolor import colored

class AIStep(ABC):
    def __init__(self, role_config: Dict[str, Any]):
        self.config = config
        self.llm = llm
        self.role = role_config.get("role")
        self.responsibility = role_config.get("responsibility")
        self.grammar = role_config.get("grammar")
        self.condition = role_config.get("condition")
        self.color = config.get(f"colors.{self.role}")
        self.steps = role_config.get("steps")
        self.step = 0
        self.results = ["" for _ in range(len(self.steps))]
        
    @abstractmethod
    def generate(self, context):
        prompt = self.dynamic_prompt(context, self.steps[self.step])
        print(colored(prompt.get("system"), "dark_grey"))
        print(colored(prompt.get("context"), "grey"))
        print(colored(prompt.get("task"), "white"))
    
        for chunk in self.llm.generate(prompt):
            print(colored(f"{chunk}", self.color), end='')
            self.results[self.step] += chunk
        
        self.step += 1
            
    def dynamic_prompt(self, context, task):
        return {
            "system": config.get("ai.prompts.system").replace(
                "<{role}>", self.role
            ).replace(
                "<{responsibility}>", self.responsibility
            ).replace(
                "<{condition}>", self.condition
            ),
            "grammar": self.grammar,
            "context": f"<context>\n{context}\n</context>\n",
            "task": f"\n<task>\n{task}\n</task>\n"
        }