# AI-Powered Python Testing Suite

Complete testing pipeline with AI-powered test generation, coverage analysis, and mutation testing. Leverages Gemini AI to automatically generate comprehensive test suites for Python applications.

## Features

- **AI-Powered Test Generation**: Automatically generates unit and coverage tests using Gemini AI
- **Interactive CLI & Web Interface**: Command-line tool and Flask web application
- **Coverage Analysis**: Built-in coverage reporting and analysis
- **Mutation Testing**: Simple, Windows-compatible mutation testing implementation
- **Test Explanations**: Optional explanatory comments for generated tests
- **Refinement Options**: Enhanced coverage test generation with more comprehensive scenarios

## Complete Testing Pipeline

1. **Generate Tests** → 2. **Run Tests** → 3. **Coverage Analysis** → 4. **Mutation Testing**

## Quick Start

### 1. Setup
```bash
# Clone and install
git clone <repository-url>
cd 3.0
pip install -r requirements.txt

# Set Gemini API key
$env:GEMINI_API_KEY="your-api-key"  # PowerShell
# export GEMINI_API_KEY="your-api-key"  # Bash/Zsh
```

### 2. Generate Tests
```bash
# Unit tests
python cli.py generate --file demo/math_utils.py --type unit --output test_unit.py

# Coverage tests with explanations
python cli.py generate --file demo/math_utils.py --type coverage --explain --output test_coverage.py

# Enhanced coverage tests
python cli.py generate --file demo/math_utils.py --type coverage --refine --output test_enhanced.py
```

### 3. Run Tests
```bash
# Execute tests
python -m pytest test_unit.py -v

# With coverage analysis
python -m coverage run -m pytest test_coverage.py && python -m coverage report
```

### 4. Mutation Testing
```bash
python cli.py mutate --target demo/math_utils.py --tests test_unit.py
```

## CLI Usage

### Generate Command
```bash
python cli.py generate [OPTIONS]

Options:
  --file TEXT             Path to Python module
  --output TEXT           Output test file
  --type [unit|coverage]  Type of tests to generate
  --explain               Add explanation comments
  --refine                Enhanced coverage tests (6-8 tests vs 4-5)
```

### Mutate Command
```bash
python cli.py mutate --target <module.py> --tests <test_file.py>
```

### Interactive Mode
```bash
python cli.py generate
# Follow prompts for file path, test type, and output
```

## Web Interface

### Start Web App
```bash
cd webapp
python app.py
# Open http://localhost:5000
```

### Web Features
- Paste code or upload Python files
- Generate unit/coverage tests with AI
- Run tests directly in browser
- Execute mutation testing
- Real-time syntax highlighting

## Example Workflow

```bash
# 1. Generate comprehensive tests
python cli.py generate --file demo/math_utils.py --type coverage --explain --refine --output demo/test_complete.py

# 2. Run tests with coverage
python -m coverage run -m pytest demo/test_complete.py -v
python -m coverage report

# 3. Mutation testing
python cli.py mutate --target demo/math_utils.py --tests demo/test_complete.py

# Expected output:
# Total mutations: 6
# Killed: 6
# Survived: 0
# Survival rate: 0.0%
```

## Project Structure

```
3.0/
├── cli.py                    # Main CLI interface
├── unit_test_generator.py    # AI unit test generation
├── coverage_tester.py        # AI coverage test generation
├── mutation_tester.py        # Simple mutation testing
├── utils.py                  # Core utilities & Gemini integration
├── requirements.txt          # Dependencies
├── webapp/
│   ├── app.py               # Flask web application
│   └── templates/
│       └── index.html       # Web interface
└── demo/
    ├── math_utils.py        # Example module
    └── test_*.py           # Generated test examples
```

## Dependencies

- `google-generativeai` - Gemini AI integration
- `click` - CLI framework
- `flask` - Web interface
- `pytest` - Test execution
- `coverage` - Coverage analysis
- `astunparse` - AST manipulation

## API Integration

The system uses Gemini 2.5 Flash for intelligent test generation:
- Analyzes function complexity and branches
- Generates comprehensive test scenarios
- Covers edge cases and error conditions
- Provides explanatory comments when requested

## Mutation Testing

Simple, Windows-compatible implementation:
- Operator mutations: `+`↔`-`, `*`↔`/`, `==`↔`!=`, etc.
- No external dependencies
- Fast execution with clear results
- Integrates with existing pytest workflow

## Contributing

1. Fork the repository
2. Create feature branch
3. Add tests for new functionality
4. Submit pull request

## License

MIT License - see LICENSE file for details