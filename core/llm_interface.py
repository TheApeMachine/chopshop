import os
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Generator
import openai
from termcolor import colored

class LLMInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

    @abstractmethod
    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        pass

class OpenAIInterface(LLMInterface):
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.model = model
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

    def generate(self, prompt: str) -> str:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in software development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                n=1,
                stop=None,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in generating response: {e}")
            return ""

    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an AI assistant specialized in software development."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500,
                n=1,
                stop=None,
                stream=True,
            )
            for chunk in response:
                if chunk['choices'][0]['finish_reason'] is not None:
                    break
                yield chunk['choices'][0]['delta'].get('content', '')
        except Exception as e:
            print(f"Error in generating response: {e}")
            yield ""

class MockLLMInterface(LLMInterface):
    def generate(self, prompt: str) -> str:
        return f"Mock response for prompt: {prompt[:50]}..."

    def generate_stream(self, prompt: str) -> Generator[str, None, None]:
        response = self.generate(prompt)
        for char in response:
            yield char

def create_llm_interface(interface_type: str = "openai", **kwargs) -> LLMInterface:
    if interface_type == "openai":
        return OpenAIInterface(**kwargs)
    elif interface_type == "mock":
        return MockLLMInterface()
    else:
        raise ValueError(f"Unknown interface type: {interface_type}")