import re
from typing import Dict, Any, List
from .base import AIStep

class TaskManager(AIStep):
    """
    # Why This Class Exists:
    # The TaskManager is responsible for handling incoming coding tasks.
    # It serves as the entry point for user requests and coordinates the initial
    # processing of tasks before they're passed to other components.
    
    # Key Responsibilities:
    # 1. Receive and validate incoming task requests
    # 2. Extract key information from the task description
    # 3. Initialize the task context for further processing
    """

    def __init__(self, model: Any, color: str):
        """
        # Why This Method:
        # Initialize any necessary attributes for the TaskManager.
        # We're setting up a dictionary to map language keywords to full names.
        """
        self.model = model
        self.labels = ["language", "concept", "interface", "behavior", "requirement", "constraint"]
        self.color = color
        
    def get_prompt(self, context: Dict[str, Any]) -> str:
        return """
        You are an AI assistant tasked with analyzing a coding task description.
        Please extract the following information from the task description:
        - Programming language
        - Key concepts
        - Required interfaces
        - Expected behaviors
        - Main requirements
        - Any constraints

        Task description: {task_description}

        Provide your analysis in a structured format.
        """.format(task_description=context.get('task_description', ''))

    def generate(self) -> Dict[str, Any]:
        """
        # Why This Method:
        # This method is the primary interface for receiving new coding tasks.
        # It performs initial processing and validation of the task description.

        :return: A dictionary containing the processed task information
        """
        task_description = input("Please describe your coding task: ")
        return self.receive_task(task_description)

    def receive_task(self, task_description: str) -> Dict[str, Any]:
        """
        # Why This Method:
        # This method is the primary interface for receiving new coding tasks.
        # It performs initial processing and validation of the task description.

        # The Process:
        # 1. Validate the input
        # 2. Extract key information (e.g., programming language, task type)
        # 3. Create a structured task context for further processing

        :param task_description: A string describing the coding task
        :return: A dictionary containing the processed task information
        """
        if not isinstance(task_description, str) or not task_description.strip():
            raise ValueError("Task description must be a non-empty string")

        entities = self.model.predict_entities(task_description, self.labels)
        merged_entities = self._merge_entities(entities, task_description)

        task_context = {
            "original_description": task_description,
            "entities": merged_entities,
            "language": self._extract_language(merged_entities),
            "concepts": self._extract_by_label(merged_entities, "concept"),
            "interfaces": self._extract_by_label(merged_entities, "interface"),
            "behaviors": self._extract_by_label(merged_entities, "behavior"),
            "requirements": self._extract_by_label(merged_entities, "requirement"),
            "constraints": self._extract_by_label(merged_entities, "constraint")
        }

        return task_context

    def _merge_entities(self, entities: List[Dict], text: str) -> List[Dict]:
        """
        # Why This Method:
        # Merge adjacent entities with the same label for more coherent results.
        """
        if not entities:
            return []
        merged = []
        current = entities[0]
        for next_entity in entities[1:]:
            if next_entity['label'] == current['label'] and (next_entity['start'] == current['end'] + 1 or next_entity['start'] == current['end']):
                current['text'] = text[current['start']: next_entity['end']].strip()
                current['end'] = next_entity['end']
            else:
                merged.append(current)
                current = next_entity
        merged.append(current)
        return merged

    def _extract_language(self, description: str) -> str:
        """
        # Why This Method:
        # To determine the programming language for the task.
        # It looks for language keywords in the description.

        :param description: The task description
        :return: The identified programming language or "Unknown"
        """
        for entity in entities:
            if entity['label'] == 'language':
                return entity['text']
        return "Unknown"

    def _extract_by_label(self, entities: List[Dict], label: str) -> List[str]:
        """
        # Why This Method:
        # Extract all entities with a specific label.
        """
        return [entity['text'] for entity in entities if entity['label'] == label]