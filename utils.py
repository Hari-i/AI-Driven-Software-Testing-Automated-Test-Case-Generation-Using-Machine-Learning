import ast
import astunparse
import os
from typing import List, Dict, Union
import google.generativeai as genai

def setup_gemini(api_key: str):
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-2.5-flash')

def extract_functions(source: Union[str, None], file_path: str = None) -> List[Dict]:
    """Parse AST to extract function defs with source code."""
    if source is None:
        if not file_path or not os.path.exists(file_path):
            raise ValueError("Provide either source code or a valid file path")
        with open(file_path, 'r') as f:
            source = f.read()
    
    tree = ast.parse(source)
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_src = astunparse.unparse(node)
            functions.append({
                'name': node.name,
                'source': func_src,
                'params': [arg.arg for arg in node.args.args],
                'branches': len([n for n in ast.walk(node) if isinstance(n, ast.If)])
            })
    if not functions:
        raise ValueError("No functions found in provided code")
    return functions

def write_test_file(output_path: str, test_code: str):
    """Write generated tests to file."""
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(test_code)
    print(f"Tests written to {output_path}")