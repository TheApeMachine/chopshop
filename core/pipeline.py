from .base import AIStep
from typing import List, Any

class Pipeline(AIStep):
    """
    # Why This Class Exists:
    # The Pipeline class is designed to execute a sequence of steps in a structured manner.
    # It ensures that each step is executed in order and that the results from one step are used as input for the next.
    """

    def __init__(self, llm: LLMInterface, *steps: AIStep):
        """
        # Why This Method:
        # Initialize the Pipeline with the steps to be executed.

        :param steps: The steps to be executed in the pipeline
        """
        super().__init__(llm)
        self.steps = steps

    def generate(self) -> List[Any]:
        """
        # Why This Method:
        # This method is the primary interface for executing the pipeline.
        # It iterates through each step, executes it, and collects the results.

        :return: A list of results from each step
        """
        context = initial_context
        results = []

        for step in self.steps:
            result = step.generate(context)
            self.results.append(result)
            results.append(result)
            context = self.update_context(context, result)
        
        return self.results

    def update_context(self, context: Dict[str, Any], result: Any) -> Dict[str, Any]:
        """
        # Why This Method:
        # This method updates the context with the result from the current step.

        :param context: The current context
        :param result: The result from the current step
        :return: The updated context
        """
        context["last_result"] = result
        return context
    

    def get_prompt(self, context: Dict[str, Any]) -> str:
        """
        # Why This Method:
        # This method generates the prompt for the LLM based on the current context.

        :param context: The current context
        :return: The prompt for the LLM
        """
        pass
