from .base import AIStep
from typing import List, Any, Dict
from .llm_interface import LLMInterface
from termcolor import colored
from utils.configuration import config

class Pipeline(AIStep):
    def __init__(self, *steps: AIStep):
        super().__init__(config.get("ai.prompts.roles.pipeline"))
        self.steps = steps
        self.color = config.get("colors.pipeline")
        
        print(colored(f"\nPipeline steps: {[step.__class__.__name__ for step in self.steps]}", 'white', attrs=['bold']))
        
    def generate(self, initial_context: Dict[str, Any] = {}) -> List[Any]:
        print(colored(f"\nProcessing pipeline: {self.__class__.__name__}", 'white', attrs=['bold']))

        context = initial_context

        for step in self.steps:
            print(colored(f"\nProcessing step: {step.__class__.__name__}", 'white', attrs=['bold']))
            context = step.generate(context)
                    
        return context
