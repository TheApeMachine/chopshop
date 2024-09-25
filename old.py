import numpy as np
from llama_cpp import Llama
from tree_sitter import Language, Parser
from typing import Any, List, Tuple, Dict, Optional
import re
import os
import ast
import tokenize
import io
from collections import defaultdict
from radon.complexity import cc_visit
import logging
import json
from functools import lru_cache
import concurrent.futures

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as f:
    CONFIG = json.load(f)

# Initialize the model
model = Llama(model_path=CONFIG['model_path'], n_ctx=CONFIG['n_ctx'], n_gpu_layers=CONFIG['n_gpu_layers'])

# TreeSitter setup
current_dir = os.path.dirname(os.path.abspath(__file__))
my_languages_so_path = os.path.join(current_dir, 'tree-sitter-python.so')
PY_LANGUAGE = Language(my_languages_so_path, 'python')
parser = Parser()
parser.set_language(PY_LANGUAGE)

@lru_cache(maxsize=100)
def verification_layer(logits: np.ndarray, temperature: float = 0.2) -> np.ndarray:
    scaled_logits = logits / temperature
    probs = np.exp(scaled_logits - np.max(scaled_logits))
    return probs / np.sum(probs)

def infer_type_from_context(param_name: str, code_body: str) -> str:
    type_patterns = [
        (r'\b{}\s*=\s*\d+', 'int'),
        (r'\b{}\s*=\s*\d+\.\d+', 'float'),
        (r'\b{}\s*=\s*".*"', 'str'),
        (r'\b{}\s*=\s*\[.*\]', 'List[Any]'),
        (r'\b{}\s*=\s*\(.*\)', 'Tuple[Any, ...]'),
        (r'\b{}\s*=\s*\{{.*\}}', 'Dict[Any, Any]'),
        (r'\bfor\s+{}\s+in', 'Iterable[Any]'),
    ]
    
    for pattern, type_hint in type_patterns:
        if re.search(pattern.format(re.escape(param_name)), code_body):
            return type_hint
    
    return 'Any'

def add_type_hints(params: str, code_body: str) -> str:
    param_list = [p.strip() for p in params.split(',') if p.strip()]
    return ', '.join([f"{p}: {infer_type_from_context(p, code_body)}" for p in param_list])

def refinement_layer(code: str) -> str:
    functions = re.findall(r'def (\w+)\((.*?)\):\n(.*?)\n(?=\s*def|\s*$)', code, re.DOTALL)
    for func_name, params, body in functions:
        type_hinted_params = add_type_hints(params, body)
        code = re.sub(fr'def {func_name}\(.*?\):', f'def {func_name}({type_hinted_params}) -> Any:', code)

    lines = code.split('\n')
    refined_lines = []
    for line in lines:
        stripped = line.strip()
        indent_level = (len(line) - len(stripped)) // 4 if not (stripped.startswith('def ') or stripped.startswith('class ')) else 0
        refined_lines.append('    ' * indent_level + stripped)
    
    refined_code = '\n'.join(refined_lines)
    refined_code = re.sub(
        r'(def \w+\(.*?\).*?:)\s*(?!\s*""")',
        lambda m: f"{m.group(1)}\n    \"\"\"TODO: Add docstring here.\"\"\"\n",
        refined_code
    )
    
    return refined_code

def analyze_code(code: str) -> Dict[str, Any]:
    try:
        ast.parse(code)
        syntax_valid = True
    except SyntaxError:
        syntax_valid = False
        return {'syntax_valid': False, 'quality_score': 0}

    tree = parser.parse(bytes(code, "utf8"))
    root_node = tree.root_node
    
    metrics = {
        'num_functions': 0,
        'num_classes': 0,
        'num_comments': 0,
        'lines_of_code': len(code.split('\n')),
        'cyclomatic_complexity': defaultdict(int),
        'syntax_valid': syntax_valid
    }

    for block in cc_visit(code):
        metrics['cyclomatic_complexity'][block.name] = block.complexity

    try:
        with io.StringIO(code) as f:
            tokens = list(tokenize.generate_tokens(f.readline))
            metrics['num_comments'] = sum(1 for tok in tokens if tok.type == tokenize.COMMENT)
    except tokenize.TokenError:
        pass

    for node in root_node.children:
        if node.type == 'function_definition':
            metrics['num_functions'] += 1
        elif node.type == 'class_definition':
            metrics['num_classes'] += 1

    avg_cc = sum(metrics['cyclomatic_complexity'].values()) / len(metrics['cyclomatic_complexity']) if metrics['cyclomatic_complexity'] else 0
    comment_ratio = metrics['num_comments'] / metrics['lines_of_code'] if metrics['lines_of_code'] > 0 else 0
    
    metrics['average_cyclomatic_complexity'] = avg_cc
    metrics['quality_score'] = max(0, min(1.0, (metrics['num_functions'] + metrics['num_classes']) * 0.1 + comment_ratio * 0.5 - avg_cc * 0.05))
    
    return metrics

def generate_with_verification(prompt: str, config: Dict[str, Any]) -> str:
    try:
        initial_output = model(prompt, max_tokens=config['max_tokens'], temperature=config['temperature'])
        generated_text = initial_output['choices'][0]['text']
        
        verification_prompt = f"Verify and improve the following Python code:\n{generated_text}\nEnsure it follows PEP 8 style guidelines, includes type hints, and has comprehensive docstrings."
        verification_output = model(verification_prompt, max_tokens=config['max_tokens'], temperature=config['verify_temp'])
        verified_text = verification_output['choices'][0]['text']
        
        refined_text = refinement_layer(verified_text)
        return refined_text
    except Exception as e:
        logger.error(f"Error in code generation: {str(e)}")
        return ""

def iterative_generation(prompt: str, config: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    current_code = prompt
    best_code = ""
    best_analysis = {'quality_score': 0}
    
    for i in range(config['n_iterations']):
        current_code = generate_with_verification(current_code, config)
        analysis = analyze_code(current_code)
        logger.info(f"Iteration {i+1} - Quality Score: {analysis['quality_score']:.2f}, Syntax Valid: {analysis['syntax_valid']}, Avg CC: {analysis.get('average_cyclomatic_complexity', 'N/A')}")
        
        if analysis['quality_score'] > best_analysis['quality_score']:
            best_code = current_code
            best_analysis = analysis
        
        if analysis['quality_score'] > config['quality_threshold'] and analysis['syntax_valid']:
            break
    
    return best_code, best_analysis

def parallel_generation(prompt: str, config: Dict[str, Any], n_parallel: int = 3) -> Tuple[str, Dict[str, Any]]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=n_parallel) as executor:
        futures = [executor.submit(iterative_generation, prompt, config) for _ in range(n_parallel)]
        results = [future.result() for future in concurrent.futures.as_completed(futures)]
    
    best_code, best_analysis = max(results, key=lambda x: x[1]['quality_score'])
    return best_code, best_analysis

if __name__ == "__main__":
    prompt = "Write a Python function to calculate the fibonacci sequence efficiently"
    final_code, analysis = parallel_generation(prompt, CONFIG)
    
    logger.info("\nFinal code:")
    logger.info(final_code)
    
    logger.info("\nCode Analysis:")
    for key, value in analysis.items():
        logger.info(f"{key}: {value}")

    # Save the generated code to a file
    with open('generated_code.py', 'w') as f:
        f.write(final_code)
    
    logger.info("\nGenerated code has been saved to 'generated_code.py'")