from flask import Flask, render_template, request, jsonify
import os
import sys
import threading
import tempfile
import subprocess
import shutil

# Add the parent directory to the sys.path to import cli and other modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unit_test_generator import generate_unit_tests
from coverage_tester import generate_coverage_tests
from io import StringIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_tests', methods=['POST'])
def generate_tests_endpoint():
    function_code = request.json.get('function_code')
    test_type = request.json.get('test_type', 'unit') # Default to unit tests
    explain = request.json.get('explain', False)
    refine = request.json.get('refine', False)

    if not function_code:
        return jsonify({'error': 'No function code provided'}), 400

    result = {'generated_tests': ''}

    def run_generation():
        nonlocal result
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            result['error'] = "GEMINI_API_KEY environment variable not set."
            return

        try:
            # For web app, use a default module name "module" since we don't have a file path
            # The generated tests will import from this module, and the run_tests endpoint
            # will need to ensure the module can be imported correctly
            module_name_for_import = "module"
            
            if test_type == 'unit':
                generated_tests = generate_unit_tests(function_code, api_key, module_name_for_import, explain)
            elif test_type == 'coverage':
                generated_tests = generate_coverage_tests(function_code, api_key, module_name_for_import, explain, refine)
            else:
                generated_tests = ""
            result['generated_tests'] = generated_tests

        except Exception as e:
            result['error'] = str(e)

    # Run the generation in a separate thread to avoid blocking the Flask app
    generation_thread = threading.Thread(target=run_generation)
    generation_thread.start()
    generation_thread.join() # Wait for the thread to complete for now. For a real app, you'd use a task queue.

    if 'error' in result:
        return jsonify({'error': result['error']}), 500
    return jsonify({'generated_tests': result['generated_tests']})

@app.route('/run_tests', methods=['POST'])
def run_tests_endpoint():
    function_code = request.json.get('function_code')
    generated_tests = request.json.get('generated_tests')

    if not function_code or not generated_tests:
        return jsonify({'error': 'Missing function code or generated tests'}), 400

    # Create a temporary directory for the module and tests
    temp_dir = tempfile.mkdtemp()
    temp_module_path = os.path.join(temp_dir, 'module.py')
    temp_test_path = os.path.join(temp_dir, 'test_module.py')

    # Write the module file
    with open(temp_module_path, 'w') as f:
        f.write(function_code)

    # Write the test file (without prepending function_code, since it's in module.py)
    with open(temp_test_path, 'w') as f:
        f.write(generated_tests)

    test_results = {'stdout': '', 'stderr': '', 'exit_code': 0}

    try:
        # Run pytest on the generated test file
        # The module.py file will be in the same directory, so imports will work
        env = os.environ.copy()
        env['PYTHONPATH'] = temp_dir + os.pathsep + env.get('PYTHONPATH', '')

        # Use --json-report to get structured output, if pytest-json-report is installed
        # For simplicity, we'll just capture stdout/stderr for now.
        process = subprocess.run(
            [sys.executable, '-m', 'pytest', temp_test_path, '--capture=no'], # --capture=no to see prints
            capture_output=True,
            text=True,
            env=env,
            check=False # Don't raise an exception for non-zero exit codes (test failures)
        )
        test_results['stdout'] = process.stdout
        test_results['stderr'] = process.stderr
        test_results['exit_code'] = process.returncode

    except Exception as e:
        print(f"Error in /run_tests: {e}") # Log the error
        test_results['stderr'] = f"An error occurred during test execution: {e}"
        test_results['exit_code'] = 1
    finally:
        # Clean up temporary files and directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

    return jsonify(test_results)

@app.route('/run_mutation_tests', methods=['POST'])
def run_mutation_tests_endpoint():
    function_code = request.json.get('function_code')
    generated_tests = request.json.get('generated_tests')

    if not function_code or not generated_tests:
        return jsonify({'error': 'Missing function code or generated tests'}), 400

    # Create temporary files for mutation testing
    temp_dir = tempfile.mkdtemp()
    temp_module_path = os.path.join(temp_dir, 'module.py')
    temp_test_path = os.path.join(temp_dir, 'test_module.py')

    with open(temp_module_path, 'w') as f:
        f.write(function_code)
    with open(temp_test_path, 'w') as f:
        f.write(generated_tests)

    try:
        from mutation_tester import run_mutation_testing
        result = run_mutation_testing(temp_module_path, temp_test_path)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)

if __name__ == '__main__':
    app.run(debug=True)
