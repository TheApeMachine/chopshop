from core.base import Pipeline
from core.task_manager import TaskManager
from core.reasoning_engine import ReasoningEngine
from core.code_generator import CodeGenerator
from core.verifier import Verifier
from core.synthesizer import Synthesizer
from core.llm_interface import create_llm_interface
from test_challenges import CODING_CHALLENGES
from termcolor import colored
from gliner import GLiNER

def main():
    llm = create_llm_interface("openai", model="gpt-3.5-turbo")  # or "gpt-4" if available
    ner = GLiNER.from_pretrained("numind/NuNerZero")
    
    pipeline = Pipeline(
        llm,
        Verifier(llm, TaskManager(ner, 'cyan'), 'yellow'),
        Verifier(llm, ReasoningEngine(llm, 'magenta'), 'yellow'),
        Verifier(llm, Synthesizer(
            llm,
            Verifier(llm, CodeGenerator(llm, "moderate", 'green'), 'yellow'),
            Verifier(llm, CodeGenerator(llm, "strict", 'blue'), 'yellow'),
            Verifier(llm, CodeGenerator(llm, "creative", 'red'), 'yellow'),
            color='white'
        ), 'yellow')
    )

    for challenge in CODING_CHALLENGES:
        print(colored(f"\nProcessing challenge: {challenge['name']}", 'white', attrs=['bold']))
        print(colored("-" * 50, 'white'))
        
        task_description = f"{challenge['description']}\n\nDetails:\n{challenge['details']}"
        results = pipeline.generate_stream({'task_description': task_description})
        
        print(colored("\nChallenge completed. Press Enter to continue to the next challenge...", 'white'))
        input()

if __name__ == "__main__":
    main()