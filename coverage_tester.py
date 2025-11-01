from utils import setup_gemini, extract_functions

def generate_coverage_tests(function_code: str, api_key: str, module_name_for_import: str, explain: bool = False, refine: bool = False) -> str:
    """Generate coverage-targeted tests using Gemini."""
    model = setup_gemini(api_key)
    functions = extract_functions(source=function_code)
    
    test_imports = f"import pytest\nfrom unittest.mock import patch\nfrom {module_name_for_import} import {', '.join([f['name'] for f in functions])}\n"
    test_code = ""
    
    for func in functions:
        branch_info = f"It has {func['branches']} branches/loops. Target all paths, exceptions, loops."
        test_count = "6-8" if refine else "4-5"
        prompt = f"""
        Generate {test_count} pytest test functions for high coverage of this Python function.
        Do NOT include markdown code blocks (```python). Do NOT include 'import pytest' within functions.
        Assume the function '{func['name']}' is available in the test environment.
        Cover all branches, loops, exceptions, edge inputs (e.g., empty lists, zero, None).
        {"Focus on edge cases and boundary conditions for maximum coverage." if refine else ""}
        
        {f"Add a comment '# EXPLAIN: [reason]' above each test function explaining its purpose." if explain else ""}

        Function: {func['source']}
        {branch_info}
        
        Output ONLY test functions (def test_branch1(): ...), no imports or other boilerplate.
        """
        
        response = model.generate_content(prompt)
        test_methods = response.text.strip().replace('```python', '').replace('```', '').strip()
        test_code += f"{test_methods}\n\n"
    
    return test_imports + test_code