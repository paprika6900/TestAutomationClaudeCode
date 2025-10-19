# TestAutomationClaudeCode

A Python-based Selenium test automation framework using pytest and the Page Object Model pattern. Designed specifically for use with Claude Code, featuring automatic HTML snapshot capture to help Claude identify accurate locators.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Architecture](#architecture)
- [Working with Claude Code and HTML Snapshots](#working-with-claude-code-and-html-snapshots)
- [Framework Extensibility](#framework-extensibility)

## Project Overview

This framework is designed to be reusable for **any website**, not just GroceryMate. GroceryMate serves as a reference implementation demonstrating the framework's capabilities and the recommended workflow for building page objects with Claude Code assistance.

### Key Features

- **Page Object Model (POM)**: Clean separation of test logic and page interactions
- **Automatic HTML Snapshots**: Captures page HTML for Claude Code to analyze and build accurate locators
- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Comprehensive Logging**: Debug-friendly logging at all levels
- **Flexible Configuration**: YAML-based configuration for easy customization
- **Multiple Browser Support**: Chrome and Firefox supported out of the box

## Project Structure

```
TestAutomationClaudeCode/
├── src/                           # Source code directory
│   ├── framework/                 # Test framework components
│   │   ├── __init__.py
│   │   ├── base_page.py          # Base Page Object Model class with HTML snapshot capability
│   │   ├── config_manager.py     # Configuration management
│   │   ├── driver_manager.py     # WebDriver factory and management
│   │   └── logger.py             # Logging utilities
│   └── pages/                     # Page Object Model classes
│       ├── __init__.py
│       ├── grocerymate_home_page.py    # Example: GroceryMate home page
│       └── grocerymate_login_page.py   # Example: GroceryMate login page
├── tests/                         # Test directory
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures (driver setup)
│   ├── test_grocerymate.py       # Example: GroceryMate home tests
│   ├── test_grocerymate_login.py # Example: GroceryMate login tests
│   └── test_html_snapshots.py    # HTML snapshot capture tests
├── page_snapshots/                # HTML snapshots (auto-generated, gitignored)
│   ├── GroceryMateHomePage.html  # Latest snapshot of each page
│   └── history/                  # Historical snapshots
├── screenshots/                   # Test screenshots (auto-generated, gitignored)
│   └── failures/                 # Screenshots on test failure
├── logs/                          # Log files (auto-generated, gitignored)
├── config.yaml                    # Framework configuration
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies
├── CLAUDE.md                      # Claude Code workflow instructions
├── NOTEPAD.md                     # Task tracking and notes
└── README.md                      # This file
```

## Development Setup

### Installing Dependencies

**Option 1: Using pip (Recommended for Windows)**
```bash
pip install -r requirements.txt
```

**Option 2: Using apt (Linux)**
```bash
sudo apt update
sudo apt install -y python3-pytest python3-selenium python3-yaml
```

### Browser Setup

The framework uses `webdriver-manager` to automatically download and manage browser drivers. No manual driver installation is required.

**Chrome** (Recommended):
- Install Google Chrome browser
- The framework will automatically download the correct ChromeDriver on first run

**Firefox** (Optional):
- Install Firefox browser
- The framework will automatically download the correct GeckoDriver on first run

### IDE Setup

- **Python Interpreter**: Python 3.8 or higher
- **Working Directory**: Set to project root (`TestAutomationClaudeCode/`)
- The `pytest.ini` configuration automatically adds `src/` to the Python path

## Running Tests

The project uses pytest with configuration in `pytest.ini`.

### Selenium UI Tests

Run all Selenium UI tests:
```bash
pytest -m ui
```

Run specific test suites:
```bash
# GroceryMate home page tests
pytest tests/test_grocerymate.py

# GroceryMate login tests
pytest tests/test_grocerymate_login.py

# HTML snapshot capture tests
pytest tests/test_html_snapshots.py -m html_capture
```

Run a specific test:
```bash
pytest tests/test_grocerymate.py::TestGroceryMateHomePage::test_home_page_loads
```

### All Tests

Run all tests:
```bash
pytest
```

Run with verbose output:
```bash
pytest -v
```

Run with detailed logging:
```bash
pytest -v --log-cli-level=DEBUG
```

### Test Markers

The framework includes custom markers for organizing tests:

- `@pytest.mark.ui` - UI tests using Selenium
- `@pytest.mark.smoke` - Smoke tests (critical functionality)
- `@pytest.mark.regression` - Regression tests
- `@pytest.mark.functional` - Functional tests
- `@pytest.mark.html_capture` - HTML snapshot capture tests

Run tests by marker:
```bash
pytest -m smoke
pytest -m "ui and smoke"
pytest -m "functional and not smoke"
```

## Architecture

The framework follows Python best practices with a src-layout and Page Object Model pattern.

### Framework Components

#### `src/framework/base_page.py`
Base Page Object class providing:
- Common page interaction methods (`click`, `enter_text`, `wait_for_element`, etc.)
- **Automatic HTML snapshot capture** when pages are accessed
- Snapshots saved to `page_snapshots/PageName.html` for Claude Code analysis
- Historical snapshots in `page_snapshots/history/` with timestamps
- Built-in screenshot capture functionality
- Comprehensive logging of all interactions

#### `src/framework/driver_manager.py`
WebDriver factory that:
- Creates and configures browser instances (Chrome, Firefox)
- Uses `webdriver-manager` for automatic driver downloads
- Works cross-platform (Windows, Linux, macOS)
- Applies configuration from `config.yaml` (headless mode, window size, timeouts)

#### `src/framework/config_manager.py`
Configuration management:
- Singleton pattern for accessing `config.yaml` settings
- Provides dot-notation access (e.g., `config.get('browser.name')`)
- Supports nested configuration values

#### `src/framework/logger.py`
Logging utilities:
- `setup_logger()`: Configure loggers with console and file output
- `get_test_logger()`: Specialized logger for test execution
- `log_test_step()`: Log test steps with visual separation
- `log_assertion()`: Log assertion results with pass/fail status

### Page Objects

Page Object Model classes in `src/pages/`:
- Each page inherits from `BasePage`
- Locators defined as class constants using `(By.LOCATOR_TYPE, "locator_string")` tuples
- Page-specific methods encapsulate user actions
- Examples: `grocerymate_home_page.py`, `grocerymate_login_page.py`

### Test Organization

#### `tests/conftest.py`
Pytest fixtures and configuration:
- `driver` fixture - Creates WebDriver for each test (function scope)
- `driver_with_screenshots` fixture - Captures screenshots on test failure
- `driver_session` fixture - Single driver for entire test session (faster, less isolated)
- Custom test markers configured

#### Test Files
- Organized by feature or page (e.g., `test_grocerymate.py`, `test_grocerymate_login.py`)
- Use fixtures from `conftest.py`
- Follow pytest naming conventions (`test_*.py`)

### Configuration

#### `config.yaml`
Central configuration file containing:
- **Browser settings**: name, headless mode, window size, timeouts
- **Selenium settings**: screenshot paths, HTML snapshot paths, history settings
- **Test data**: base URLs, login credentials
- **Logging configuration**: levels, formats

## Working with Claude Code and HTML Snapshots

### How HTML Snapshots Work

This framework is specifically designed to work seamlessly with Claude Code:

1. **Automatic Snapshot Capture**: When a page object is instantiated or `open()` is called, the HTML source is automatically saved
2. **Snapshot Location**: `page_snapshots/PageName.html` (e.g., `page_snapshots/GroceryMateHomePage.html`)
3. **Historical Snapshots**: Each snapshot is also saved with a timestamp in `page_snapshots/history/`
4. **Manual Snapshot Capture**: Use `page.save_html_snapshot()` to capture on-demand

### Complete Workflow for Building Page Objects

This is the recommended workflow for writing automated tests with this framework:

#### Step 1: Create a Basic Test to Navigate to the Page

Create a simple test that navigates to the page you want to test. This test will capture the HTML snapshot.

**Example**: In `tests/test_html_snapshots.py`:
```python
import pytest
from pages.grocerymate_home_page import GroceryMateHomePage

@pytest.mark.html_capture
def test_capture_home_page_html(driver):
    """Capture HTML snapshot of the GroceryMate home page."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()

    # Manually save HTML snapshot with 2-version history
    home_page.save_html_snapshot(keep_history=2)

    # Basic verification
    assert driver.current_url is not None
    print(f"\n✓ Home page HTML captured: {driver.current_url}")
```

#### Step 2: Run the Test to Capture HTML Snapshot

Run the test to navigate to the page and save the HTML:

```bash
pytest tests/test_html_snapshots.py::test_capture_home_page_html -v
```

The HTML snapshot will be saved to:
- `page_snapshots/GroceryMateHomePage.html` (latest snapshot)
- `page_snapshots/history/GroceryMateHomePage_YYYYMMDD_HHMMSS.html` (historical copy)

#### Step 3: Ask Claude Code to Analyze HTML and Build Page Object

Ask Claude Code to read the HTML snapshot and create a complete page object:

**Example prompt**:
```
"Read page_snapshots/GroceryMateHomePage.html and build a complete Page Object Model
for the GroceryMate home page. Include locators for all interactive elements like
navigation menu, search bar, user icons, and any call-to-action buttons."
```

Claude Code will:
1. Read the HTML snapshot
2. Identify all major interactive elements (buttons, links, inputs, etc.)
3. Create accurate CSS selectors or other locator strategies
4. Generate a complete page object class with:
   - Well-organized locator constants grouped by section
   - Descriptive method names for each interaction
   - Proper documentation and logging

#### Step 4: Create Functional Test Methods

Once the page object is complete with locators, create functional tests:

```python
@pytest.mark.functional
@pytest.mark.smoke
def test_search_functionality(driver):
    """Test the search functionality."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    home_page.search_for_product("tomatoes")
    # Add assertions here

@pytest.mark.functional
def test_navigation_to_shop(driver):
    """Test navigation to Shop page."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    home_page.click_shop_nav()
    # Verify navigation occurred
```

#### Step 5: Navigate to Sub-Pages and Repeat

When you need to test a sub-page, repeat the workflow:

1. Create HTML capture test for the sub-page
2. Run the test to capture HTML
3. Ask Claude Code to analyze the new snapshot
4. Claude Code builds the new page object
5. Create functional tests using the new page object

### Real Example: GroceryMate Implementation

The GroceryMate page objects were created using exactly this workflow:

1. **Tests Created**: `test_html_snapshots.py` with capture tests
2. **Tests Executed**: HTML snapshots captured
3. **Claude Code Analyzed**: Read the HTML files and identified all key elements
4. **Page Objects Built**: Complete page objects created with comprehensive locators and methods

**Results**:
- `grocerymate_home_page.py`: 12 locators, 14 methods
- `grocerymate_login_page.py`: 7 locators, 8 methods
- Production-ready with proper documentation and logging

### Best Practices

1. **Start Simple**: Create basic test → capture HTML → build page object → add complex tests
2. **One Page at a Time**: Focus on one page object before moving to the next
3. **Update Snapshots**: Re-run capture tests after UI changes to update HTML snapshots
4. **Ask Specific Questions**: Guide Claude Code to specific sections if HTML is very large
   - Example: "Focus on the navigation menu in GroceryMateHomePage.html"
5. **Verify Locators**: Run functional tests after Claude Code builds the page object
6. **Organize by Feature**: Group related tests together
7. **Use Manual Capture**: Call `save_html_snapshot(keep_history=2)` for on-demand captures

### Troubleshooting Large HTML Files

If an HTML snapshot is too large for Claude Code to read at once:

1. **Use grep to extract sections**:
   ```
   "Use grep to find all input and button elements in GroceryMateHomePage.html"
   ```

2. **Focus on specific features**:
   ```
   "Read the navigation section of GroceryMateHomePage.html and create locators for menu items"
   ```

3. **Analyze in chunks**: Ask for header elements first, then content, then footer

### Benefits of This Approach

- ✅ **Accurate Locators**: Claude Code analyzes actual HTML structure
- ✅ **Fast Development**: No manual element inspection in browser DevTools
- ✅ **Up-to-Date**: Snapshots refreshed automatically each test run
- ✅ **Historical Tracking**: Compare snapshots over time to detect UI changes
- ✅ **Better Maintainability**: Claude Code suggests stable, semantic locators
- ✅ **Complete Coverage**: Claude Code identifies ALL interactive elements
- ✅ **Consistent Patterns**: Page objects follow consistent naming and organization

## Framework Extensibility

This framework is designed to be reusable for **any website**, not just GroceryMate.

### GroceryMate as an Example

The following files serve as reference implementations:
- `src/pages/grocerymate_*.py` - Example page objects
- `tests/test_grocerymate*.py` - Example tests
- `tests/test_html_snapshots.py` - Example HTML capture workflow

### Adding New Websites

To test a different website:

1. **Update config.yaml** with the new base URL:
   ```yaml
   test_data:
     base_url: "https://your-website.com/"
   ```

2. **Create new page objects** in `src/pages/your_site_*.py`:
   ```python
   from framework.base_page import BasePage

   class YourSiteHomePage(BasePage):
       # Define locators and methods
       pass
   ```

3. **Create HTML capture tests** in `tests/test_html_snapshots.py`:
   ```python
   @pytest.mark.html_capture
   def test_capture_your_site_home_page_html(driver):
       """Capture HTML snapshot of your site."""
       home_page = YourSiteHomePage(driver)
       home_page.open_home_page()
       home_page.save_html_snapshot(keep_history=2)
   ```

4. **Create functional tests** in `tests/test_your_site.py`

5. **Follow the HTML snapshot workflow** to build page objects with Claude Code

6. **Use the same logging standards** as the example files

The framework components (`src/framework/`) remain unchanged and work with any website.

### Example Structure for Multiple Sites

```
src/pages/
├── grocerymate_home_page.py    # Example: GroceryMate
├── grocerymate_login_page.py   # Example: GroceryMate
├── amazon_home_page.py         # Your site: Amazon
├── amazon_product_page.py      # Your site: Amazon
└── github_repo_page.py         # Your site: GitHub

tests/
├── test_grocerymate.py         # Example tests
├── test_grocerymate_login.py   # Example tests
├── test_amazon.py              # Your tests
├── test_github.py              # Your tests
└── test_html_snapshots.py      # All HTML capture tests
```

Keep the GroceryMate files as examples and reference implementations.

## Contributing

This project is designed for use with Claude Code. See `CLAUDE.md` for Claude Code workflow instructions and `NOTEPAD.md` for current task tracking.

## License

This project is provided as-is for educational and testing purposes.
