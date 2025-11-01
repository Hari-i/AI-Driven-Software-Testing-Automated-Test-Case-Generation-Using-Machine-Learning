import click
import os
import sys
from unit_test_generator import generate_unit_tests
from coverage_tester import generate_coverage_tests
from utils import write_test_file

@click.group()
def cli():
    """Simple Testing Tools CLI."""
    pass

@cli.command()
@click.option('--file', 'file_path', help='Path to Python module')
@click.option('--output', help='Output test file')
@click.option('--type', type=click.Choice(['unit', 'coverage']), help='Type of tests to generate')
@click.option('--explain', is_flag=True, help='Add explanation comments to generated tests')
@click.option('--refine', is_flag=True, help='Refine coverage tests iteratively (up to 3 iterations)')
def generate(file_path: str, output: str, type: str, explain: bool, refine: bool):
    """Generate unit or coverage tests. If no options are provided, runs in interactive mode."""
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        raise click.ClickException("Set GEMINI_API_KEY env var")

    if not file_path or not type:
        # Interactive mode
        click.echo("\n--- Interactive Test Generation ---")
        
        # Get file path
        while not file_path:
            file_path = click.prompt("Enter path to Python module (e.g., demo/math_utils.py)")
            if not os.path.exists(file_path):
                click.echo(f"Error: File not found at '{file_path}'. Please try again.")
                file_path = None
        
        # Get test type
        while not type:
            type = click.prompt("Enter test type (unit or coverage)", type=click.Choice(['unit', 'coverage']))
        
        # Get output file
        if not output:
            default_output = f"test_{os.path.basename(file_path).replace('.py', '')}.py"
            output = click.prompt(f"Enter output test file (default: {default_output})", default=default_output)

    # Read the content of the input file
    with open(file_path, 'r') as f:
        function_code = f.read()
    
    # Extract the module name for import
    module_name_for_import = os.path.splitext(os.path.basename(file_path))[0]

    generated_tests = ""
    if type == 'unit':
        generated_tests = generate_unit_tests(function_code, api_key, module_name_for_import, explain)
    elif type == 'coverage':
        generated_tests = generate_coverage_tests(function_code, api_key, module_name_for_import, explain, refine)
    
    # Prepend the original function code to the generated tests
    final_test_code = function_code + "\n" + generated_tests
    
    write_test_file(output, final_test_code)
    click.echo(f"Generated {type} tests for {file_path} and saved to {output}")

@cli.command()
@click.option('--target', required=True, help='Path to module to mutate')
@click.option('--tests', required=True, help='Path to test file')
def mutate(target: str, tests: str):
    """Run mutation testing on target module."""
    from mutation_tester import run_mutation_testing
    
    click.echo(f"Running mutation testing on {target}...")
    result = run_mutation_testing(target, tests)
    
    if result['success']:
        click.echo("\nMutation Testing Results:")
        click.echo(result['output'])
        summary = result['summary']
        if summary.get('total', 0) > 0:
            survival_rate = (summary.get('survived', 0) / summary['total']) * 100
            click.echo(f"\nSummary: {summary['killed']} killed, {summary['survived']} survived ({survival_rate:.1f}% survival rate)")
    else:
        click.echo(f"Error: {result.get('error', 'Unknown error')}")
        if result.get('output'):
            click.echo(f"Output: {result['output']}")

if __name__ == '__main__':
    cli()