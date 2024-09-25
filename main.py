from core.pipeline import Pipeline
from core.reasoning_engine import ReasoningEngine
from core.verifier import Verifier
from test_challenges import CODING_CHALLENGES
from termcolor import colored

def main():
    print(colored("Constructing pipeline...", 'white', attrs=['bold']))

    pipeline = Pipeline(
        Verifier(ReasoningEngine()),
    )

    for challenge in CODING_CHALLENGES:
        print(colored(f"\nProcessing challenge: {challenge['name']}", 'white', attrs=['bold']))
        print(colored("-" * 50, 'white'))
        
        task_description = f"{challenge['description']}\n\nDetails:\n{challenge['details']}"
        pipeline.generate(task_description)
        
        print(colored("\nChallenge completed. Press Enter to continue to the next challenge...", 'white'))
        input()

if __name__ == "__main__":
    main()