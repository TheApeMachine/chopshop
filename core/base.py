from abc import ABC, abstractmethod
from typing import Any, Dict, List, Generator
from .llm_interface import LLMInterface
from termcolor import colored

class AIStep(ABC):
    def __init__(self, llm: LLMInterface, color: str):
        self.llm = llm
        self.color = color

    @abstractmethod
    def get_prompt(self, context: Dict[str, Any]) -> str:
        pass

    def generate(self, context: Dict[str, Any]) -> Any:
        prompt = self.get_prompt(context)
        return self.llm.generate(prompt)

    def generate_stream(self, context: Dict[str, Any]) -> Generator[str, None, None]:
        prompt = self.get_prompt(context)
        print(colored(f"\n--- {self.__class__.__name__} ---", self.color))
        for token in self.llm.generate_stream(prompt):
            print(colored(token, self.color), end='', flush=True)
            yield token

class Pipeline(AIStep):
    def __init__(self, llm: LLMInterface, *steps: AIStep):
        super().__init__(llm, 'white')
        self.steps = steps

    def generate_stream(self, initial_context: Dict[str, Any] = {}) -> List[Any]:
        context = initial_context
        results = []
        for step in self.steps:
            result = ''.join(list(step.generate_stream(context)))
            results.append(result)
            context = self.update_context(context, result)
        return results

    def update_context(self, context: Dict[str, Any], result: Any) -> Dict[str, Any]:
        context['last_result'] = result
        return context

    def get_prompt(self, context: Dict[str, Any]) -> str:
        pass