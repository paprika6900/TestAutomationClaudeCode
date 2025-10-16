# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TestAutomationClaudeCode - A Python-based test automation project using pytest. Currently contains a simple calculator module that serves as a placeholder application under test.

## Project Structure

```
TestAutomationClaudeCode/
├── src/                      # Source code directory
│   └── calculator/           # Calculator package (application under test)
│       ├── __init__.py
│       └── calculator.py     # Core calculator functions
├── tests/                    # Test directory
│   ├── __init__.py
│   └── test_calculator.py    # Calculator test suite
├── pytest.ini                # Pytest configuration
├── requirements.txt          # Python dependencies
├── setup.sh                  # Setup script for environment
└── .gitignore                # Git ignore patterns
```

## Development Setup

### Initial Setup

Run the automated setup script:
```bash
./setup.sh
```

This will:
1. Install python3.12-venv if needed
2. Create a virtual environment in `venv/`
3. Install all dependencies from requirements.txt

### Manual Setup

If you prefer to set up manually:

```bash
# Install venv package (if not already installed)
sudo apt install python3.12-venv

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Activating the Virtual Environment

Before running tests or working with the project:
```bash
source venv/bin/activate
```

To deactivate:
```bash
deactivate
```

## Running Tests

The project uses pytest with configuration in `pytest.ini`. The configuration automatically adds the `src/` directory to the Python path.

Run all tests:
```bash
pytest
```

Run tests with verbose output (default in pytest.ini):
```bash
pytest -v
```

Run a specific test file:
```bash
pytest tests/test_calculator.py
```

Run a specific test class:
```bash
pytest tests/test_calculator.py::TestCalculator
```

Run a specific test method:
```bash
pytest tests/test_calculator.py::TestCalculator::test_add_positive_numbers
```

Run tests with coverage:
```bash
pytest --cov=calculator
```

## Architecture

The project follows Python best practices with a src-layout:

- **src/calculator/** - Application code organized as a package
  - The calculator module is imported as `from calculator.calculator import add`
  - Package structure allows for future expansion

- **tests/** - Test code organized as a package
  - Mirror the structure of src/ for clarity
  - Use pytest's class-based organization for grouping related tests
  - Test files follow the `test_*.py` naming convention

- **pytest.ini** - Centralizes pytest configuration
  - Sets test discovery paths and patterns
  - Adds src/ to Python path automatically
  - Configures output verbosity and behavior

## Git Workflow

**IMPORTANT**: When requested to commit and push changes, always follow this workflow:

1. **Create a new feature branch** with a clear, descriptive name
   ```bash
   git checkout -b feature/descriptive-name
   ```

2. **Stage and commit changes** with a clear commit message explaining all changes
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

3. **Push the feature branch** to remote
   ```bash
   git push -u origin feature/descriptive-name
   ```

4. **Create a Merge Request (Pull Request)** to master branch
   - Use `gh pr create` command
   - Include summary of changes and test plan

5. **Wait for code review** - Do NOT merge or checkout master until the user completes their review and gives approval
