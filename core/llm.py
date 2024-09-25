import openai
import os
from typing import Generator
from utils.configuration import config

class LLM:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LLM, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        openai.api_key = os.getenv("OPENAI_API_KEY")

        if not openai.api_key:
            raise ValueError("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")

        self.client = openai.OpenAI(api_key=openai.api_key)

    def generate(self, prompt):
        try:
            stream = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "system", "content": prompt.get("system")
                }, {
                    "role": "system", "content": prompt.get("grammar")
                }, {
                    "role": "user", "content": prompt.get("context")
                }, {
                    "role": "user", "content": prompt.get("task")
                }],
                stream=True,
            )
            for chunk in stream:
                if chunk.choices[0].finish_reason is not None:
                    break
                yield chunk.choices[0].delta.content or ""
        except Exception as e:
            print(f"Error in generating response: {e}")
            yield ""


llm = LLM()