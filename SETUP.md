# Setup Instructions

## Prerequisites
- Python 3.8 or higher
- Gemini API key from [Google AI Studio](https://aistudio.google.com/)

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ai-python-testing-suite
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Gemini API key**:
   
   **Windows (PowerShell)**:
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   ```
   
   **Linux/macOS (Bash/Zsh)**:
   ```bash
   export GEMINI_API_KEY="your-api-key-here"
   ```

4. **Verify installation**:
   ```bash
   python cli.py --help
   ```

## Quick Test

Generate tests for the demo module:
```bash
python cli.py generate --file demo/math_utils.py --type unit --output demo/test_example.py
python -m pytest demo/test_example.py -v
```

## Web Interface

Start the web application:
```bash
cd webapp
python app.py
```
Open http://localhost:5000 in your browser.

## Troubleshooting

- **API Key Issues**: Ensure your Gemini API key is valid and properly set
- **Import Errors**: Verify all dependencies are installed with `pip list`
- **Permission Errors**: Run with appropriate permissions for file operations