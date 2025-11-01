import ast
import subprocess
import sys
import os
import tempfile
import shutil

def run_mutation_testing(target_path: str, test_path: str) -> dict:
    """Simple mutation testing implementation."""
    try:
        with open(target_path, 'r') as f:
            source_code = f.read()
        
        mutations = generate_simple_mutations(source_code)
        total_mutations = len(mutations)
        killed = 0
        survived = 0
        
        for i, mutated_code in enumerate(mutations):
            if test_mutation(mutated_code, test_path, target_path):
                survived += 1
            else:
                killed += 1
        
        survival_rate = (survived / total_mutations * 100) if total_mutations > 0 else 0
        
        output = f"""Simple Mutation Testing Results:
Total mutations: {total_mutations}
Killed: {killed}
Survived: {survived}
Survival rate: {survival_rate:.1f}%
"""
        
        return {
            'success': True,
            'output': output,
            'summary': {
                'total': total_mutations,
                'killed': killed,
                'survived': survived
            }
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e),
            'output': '',
            'summary': {}
        }

def generate_simple_mutations(source_code: str) -> list:
    """Generate simple mutations by replacing operators."""
    mutations = []
    
    # Simple operator mutations
    operator_mutations = [
        ('+', '-'),
        ('-', '+'),
        ('*', '/'),
        ('/', '*'),
        ('==', '!='),
        ('!=', '=='),
        ('<', '>='),
        ('>', '<='),
        ('<=', '>'),
        ('>=', '<')
    ]
    
    for old_op, new_op in operator_mutations:
        if old_op in source_code:
            mutated = source_code.replace(old_op, new_op, 1)
            if mutated != source_code:
                mutations.append(mutated)
    
    return mutations

def test_mutation(mutated_code: str, test_path: str, original_target_path: str) -> bool:
    """Test if a mutation survives (returns True if survived)."""
    try:
        # Create temporary files
        temp_dir = tempfile.mkdtemp()
        target_name = os.path.basename(original_target_path)
        temp_target = os.path.join(temp_dir, target_name)
        
        # Write mutated code
        with open(temp_target, 'w') as f:
            f.write(mutated_code)
        
        # Copy test file
        test_name = os.path.basename(test_path)
        temp_test = os.path.join(temp_dir, test_name)
        shutil.copy2(test_path, temp_test)
        
        # Run tests
        result = subprocess.run([
            sys.executable, '-m', 'pytest', temp_test, '-q'
        ], capture_output=True, cwd=temp_dir, timeout=10)
        
        # Clean up
        shutil.rmtree(temp_dir)
        
        # If tests pass, mutation survived
        return result.returncode == 0
        
    except:
        return False