# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TestAutomationClaudeCode - A Python-based Selenium test automation framework using pytest and the Page Object Model pattern. Designed specifically for use with Claude Code, featuring automatic HTML snapshot capture to help Claude identify accurate locators.

## Project Structure

```
TestAutomationClaudeCode/
├── src/                           # Source code directory
│   ├── framework/                 # Test framework components
│   │   ├── __init__.py
│   │   ├── base_page.py          # Base Page Object Model class with HTML snapshot capability
│   │   ├── config_manager.py     # Configuration management
│   │   └── driver_manager.py     # WebDriver factory and management
│   └── pages/                     # Page Object Model classes
│       ├── __init__.py
│       └── grocerymate_home_page.py  # GroceryMate home page object
├── tests/                         # Test directory
│   ├── __init__.py
│   ├── conftest.py               # Pytest fixtures (driver setup)
│   └── test_grocerymate.py       # GroceryMate test suite
├── page_snapshots/                # HTML snapshots (auto-generated, gitignored)
│   ├── GroceryMateHomePage.html  # Latest snapshot of each page
│   └── history/                  # Historical snapshots
├── screenshots/                   # Test screenshots (auto-generated, gitignored)
│   └── failures/                 # Screenshots on test failure
├── config.yaml                    # Framework configuration
├── pytest.ini                     # Pytest configuration
├── requirements.txt               # Python dependencies (for pip reference)
└── .gitignore                     # Git ignore patterns
```

## Development Setup

Install the required Python packages using apt:

```bash
sudo apt update
sudo apt install -y python3-pytest python3-selenium python3-yaml
```

**Install ChromeDriver** (required for Chrome browser automation):

```bash
# Install Chrome browser (if not already installed)
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb

# Install chromedriver
sudo apt install chromium-chromedriver
```

**For Firefox** (optional, if you want to use Firefox instead):
```bash
sudo apt install firefox firefox-geckodriver
```

**IDE Setup**: Make sure your IDE Python interpreter is set to `/usr/bin/python3` to use the system-installed packages.

## Running Tests

The project uses pytest with configuration in `pytest.ini`. The configuration automatically adds the `src/` directory to the Python path.

### Selenium UI Tests

Run all selenium UI tests:
```bash
pytest -m ui
```

Run GroceryMate tests:
```bash
pytest tests/test_grocerymate.py
```

Run a specific test:
```bash
pytest tests/test_grocerymate.py::TestGroceryMate::test_open_grocerymate_home_page
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

### Test Markers

The framework includes custom markers for organizing tests:
- `@pytest.mark.ui` - UI tests using Selenium
- `@pytest.mark.smoke` - Smoke tests
- `@pytest.mark.regression` - Regression tests

Run tests by marker:
```bash
pytest -m smoke
pytest -m "ui and smoke"
```

## Architecture

The framework follows Python best practices with a src-layout and Page Object Model pattern:

### Framework Components

- **src/framework/base_page.py** - Base Page Object class
  - Provides common page interaction methods (click, enter_text, wait_for_element, etc.)
  - **Automatically saves HTML snapshots** when pages are accessed
  - Snapshots saved to `page_snapshots/PageName.html` for Claude Code to analyze
  - Historical snapshots kept in `page_snapshots/history/` with timestamps
  - Built-in screenshot capture functionality

- **src/framework/driver_manager.py** - WebDriver factory
  - Creates and configures browser instances (Chrome, Firefox)
  - Uses system-installed chromedriver/geckodriver
  - Applies configuration from config.yaml (headless mode, window size, timeouts)

- **src/framework/config_manager.py** - Configuration management
  - Singleton pattern for accessing config.yaml settings
  - Provides dot-notation access (e.g., `config.get('browser.name')`)

### Page Objects

- **src/pages/** - Page Object Model classes
  - Each page inherits from `BasePage`
  - Locators defined as class constants using `(By.LOCATOR_TYPE, "locator_string")` tuples
  - Page-specific methods encapsulate user actions
  - Example: `src/pages/grocerymate_home_page.py`

### Test Organization

- **tests/conftest.py** - Pytest fixtures and configuration
  - `driver` fixture - Creates WebDriver for each test (function scope)
  - `driver_with_screenshots` fixture - Same as driver but captures screenshots on failure
  - `driver_session` fixture - Single driver for entire test session (faster, less isolated)
  - Custom test markers: `@pytest.mark.ui`, `@pytest.mark.smoke`, `@pytest.mark.regression`

- **tests/** - Test files
  - Organized by feature or page
  - Use fixtures from conftest.py
  - Follow pytest naming conventions (`test_*.py`)

### Configuration

- **config.yaml** - Central configuration file
  - Browser settings (name, headless mode, window size, timeouts)
  - Selenium settings (screenshot paths, HTML snapshot paths)
  - Test data (base URLs, timeouts)
  - Logging configuration

## Working with Claude Code and HTML Snapshots

### How HTML Snapshots Work

This framework is specifically designed to work seamlessly with Claude Code:

1. **Automatic Snapshot Capture**: When a page object is instantiated or `open()` is called, the HTML source is automatically saved
2. **Snapshot Location**: `page_snapshots/PageName.html` (e.g., `page_snapshots/GroceryMateHomePage.html`)
3. **Historical Snapshots**: Each snapshot is also saved with a timestamp in `page_snapshots/history/`

### Complete Workflow for Building Page Objects from HTML

This is the recommended workflow for writing automated tests with this framework:

#### Step 1: Create a Basic Test to Navigate to the Page

First, create a simple test that navigates to the page you want to test. Even if you don't have locators yet, this test will capture the HTML snapshot.

**Example**: Create or update `tests/test_grocerymate.py`:
```python
import pytest
from pages.grocerymate_home_page import GroceryMateHomePage

@pytest.mark.ui
def test_open_grocerymate_home_page(driver):
    """Navigate to GroceryMate home page and capture HTML snapshot."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    # HTML snapshot automatically saved to page_snapshots/GroceryMateHomePage.html
    assert driver.current_url is not None
```

#### Step 2: Run the Test to Capture HTML Snapshot

Run the test to navigate to the page and automatically save the HTML:

```bash
pytest tests/test_grocerymate.py::test_open_grocerymate_home_page -v
```

The HTML snapshot will be saved to:
- `page_snapshots/GroceryMateHomePage.html` (latest snapshot)
- `page_snapshots/history/GroceryMateHomePage_YYYYMMDD_HHMMSS.html` (historical copy)

#### Step 3: Ask Claude Code to Analyze HTML and Build Page Object

Now ask Claude Code to read the HTML snapshot and create a complete page object:

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
   - Proper documentation

#### Step 4: Create Additional Test Methods

Once the page object is complete with locators, create additional test methods to exercise the functionality:

```python
@pytest.mark.smoke
def test_search_functionality(driver):
    """Test the search functionality."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    home_page.search_for_product("tomatoes")
    # Add assertions here

@pytest.mark.ui
def test_navigation_to_shop(driver):
    """Test navigation to Shop page."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    home_page.click_shop_nav()
    # Verify navigation occurred
```

#### Step 5: Navigate to Sub-Pages and Repeat

When you need to test a sub-page (like a product details page), repeat the workflow:

1. Create a test that navigates to the sub-page
2. Run the test to capture HTML (a new snapshot will be created for the new page object)
3. Ask Claude Code to analyze the new snapshot
4. Claude Code builds the new page object

**Example**: Testing the Shop page:
```python
# In tests/test_grocerymate_shop.py
@pytest.mark.ui
def test_open_shop_page(driver):
    """Navigate to Shop page and capture HTML."""
    home_page = GroceryMateHomePage(driver)
    home_page.open_home_page()
    home_page.click_shop_nav()

    # Create shop page object
    shop_page = GroceryMateShopPage(driver)
    # HTML snapshot saved to page_snapshots/GroceryMateShopPage.html
```

Then ask Claude Code:
```
"Read page_snapshots/GroceryMateShopPage.html and build a complete Page Object Model
for the shop page with all product filtering, sorting, and cart functionality."
```

### Real Example: GroceryMateHomePage

The `src/pages/grocerymate_home_page.py` file was created using exactly this workflow:

1. **Test Created**: `test_open_grocerymate_home_page` in `tests/test_grocerymate.py`
2. **Test Executed**: HTML snapshot captured to `page_snapshots/GroceryMateHomePage.html`
3. **Claude Code Analyzed**: Read the 134KB HTML file and identified all key elements
4. **Page Object Built**: Complete page object created with:
   - 12 locators organized by section (header, navigation, buttons)
   - 14 methods covering all interactions (search, navigation, clicks)
   - Proper documentation and naming conventions

**Result**: A production-ready page object in `src/pages/grocerymate_home_page.py:20-135` with locators for:
- Search input and icon
- Navigation menu (Home, Shop, Favorites, Contact)
- User account, favorites, and cart icons
- Three "Shop Now" buttons in different page sections
- Contact phone number

### Best Practices

1. **Start Simple**: Create basic test → capture HTML → build page object → add complex tests
2. **One Page at a Time**: Focus on one page object before moving to the next
3. **Update Snapshots**: Re-run tests after UI changes to update HTML snapshots
4. **Ask Specific Questions**: Guide Claude Code to specific sections if the HTML is very large
   - Example: "Focus on the navigation menu in GroceryMateHomePage.html"
5. **Verify Locators**: Run tests after Claude Code builds the page object to verify locators work
6. **Organize by Feature**: Group related tests together (e.g., all shop page tests in `test_grocerymate_shop.py`)

### Troubleshooting Large HTML Files

If an HTML snapshot is too large for Claude Code to read at once:

1. **Ask Claude Code to use grep** to extract specific sections:
   ```
   "Use grep to find all input and button elements in GroceryMateHomePage.html"
   ```

2. **Focus on specific features**:
   ```
   "Read the navigation section of GroceryMateHomePage.html and create locators for menu items"
   ```

3. **Analyze in chunks**: Ask for header elements first, then content, then footer

### Benefits of This Approach

- **Accurate Locators**: Claude Code analyzes actual HTML structure, not assumptions
- **Fast Development**: No manual element inspection in browser DevTools
- **Up-to-Date**: Snapshots refreshed automatically each test run
- **Historical Tracking**: Compare snapshots over time to detect UI changes
- **Better Maintainability**: Claude Code suggests stable, semantic locators (CSS preferred over XPath)
- **Complete Coverage**: Claude Code identifies ALL interactive elements, not just the obvious ones
- **Consistent Patterns**: Page objects follow consistent naming and organization

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
