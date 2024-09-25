from abc import ABC, abstractmethod

class BaseAdapter(ABC):
    """
    # Why This Class Exists:
    # The BaseAdapter serves as an abstract base class for all language-specific
    # adapters. It defines the common interface that all adapters must implement,
    # ensuring consistency across different programming language support.
    
    # Key Responsibilities:
    # 1. Define the common interface for all adapters
    # 2. Provide any shared functionality for adapters
    """

    @abstractmethod
    def generate_code(self, plan: dict) -> str:
        """
        # Why This Method:
        # This abstract method defines the interface for code generation.
        # Each language-specific adapter will implement this method to
        # generate code based on the provided plan.

        :param plan: A dictionary containing the high-level plan for code generation
        :return: A string containing the generated code
        """
        pass

    @abstractmethod
    def analyze_code(self, code: str) -> dict:
        """
        # Why This Method:
        # This abstract method defines the interface for code analysis.
        # Each language-specific adapter will implement this method to
        # analyze the generated code and provide feedback.

        :param code: A string containing the code to be analyzed
        :return: A dictionary containing the analysis results
        """
        pass