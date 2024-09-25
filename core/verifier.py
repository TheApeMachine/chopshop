from typing import Dict, Any, Any
from .base import AIStep

class Verifier(AIStep):
    def __init__(self, step: AIStep, color: str):
        self.step = step
        self.color = color
    def get_prompt(self, context: Dict[str, Any]) -> str:
        return """
        Verify the following output:

        {result}

        Consider the following aspects:
        1. Correctness: Does it meet the requirements and solve the problem?
        2. Completeness: Are all parts of the task addressed?
        3. Efficiency: Is the solution optimized and performant?
        4. Readability: Is the output clear and easy to understand?
        5. Best Practices: Does it follow coding standards and best practices?

        Provide a detailed analysis of each aspect and an overall verdict (PASS/FAIL).
        If FAIL, explain what needs to be improved.
        """.format(result=context.get('result', ''))

    def generate(self) -> Any:
        result = self.step.generate()
        verified = self.verify(result)
        if not verified:
            raise ValueError(f"Verification failed for {self.step.__class__.__name__}")
        return result

    def verify(self, result: Any) -> bool:
        # Implement verification logic here
        print(f"Verifying result from {self.step.__class__.__name__}")
        return True  # Placeholder

    def is_verified(self, verification: str) -> bool:
        return "PASS" in verification.upper()