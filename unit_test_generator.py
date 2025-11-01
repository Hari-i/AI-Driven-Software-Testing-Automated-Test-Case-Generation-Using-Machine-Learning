from utils import setup_gemini, extract_functions

def generate_unit_tests(function_code: str, api_key: str, module_name_for_import: str, explain: bool = False) -> str:
    """Generate basic unit tests using Gemini."""
    model = setup_gemini(api_key)
    functions = extract_functions(source=function_code)
    
    test_imports = f"import pytest\nfrom unittest.mock import patch\nfrom {module_name_for_import} import {', '.join([f['name'] for f in functions])}\n"
    test_code = ""
    
    for func in functions:
        prompt = f"""
        Generate 3-4 pytest test functions for this Python function, covering normal, edge, and error cases.
        Do NOT include markdown code blocks (```python). Do NOT include 'import pytest' within functions.
        Assume the function '{func['name']}' is available in the test environment.
        Use assert for comparisons and pytest.raises for exceptions.
        
        {f"Add a comment '# EXPLAIN: [reason]' above each test function explaining its purpose." if explain else ""}

        Function:
        {func['source']}
        
        Output ONLY the test functions (e.g., def test_normal_add(): ...), no imports or other boilerplate.
        """
        
        response = model.generate_content(prompt)
        test_methods = response.text.strip().replace('```python', '').replace('```', '').strip()
        test_code += f"{test_methods}\n\n"
    
    return test_imports + test_code