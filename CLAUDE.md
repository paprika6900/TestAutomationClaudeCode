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

4. **Create a Pull Request targeting main/master branch**
   - **CRITICAL**: ALWAYS target main/master branch (NOT feature branches)
   - Use `gh pr create` command (defaults to main branch)
   - Include summary of changes and test plan
   - Example: `gh pr create --title "Add feature X" --body "Description"`

5. **Wait for code review** - Do NOT merge or checkout master until the user completes their review and gives approval

### Why Always Target Main/Master

- This is a **solo developer project** - no need for intermediate feature branches
- Direct PRs to main simplify the workflow
- Easier to track what's in production (main branch)
- Reduces unnecessary branch management overhead

## Claude Code Workflow Requirements

### Context Window Management

**CRITICAL**: Before starting ANY new task, Claude Code MUST check the context window usage and manage it proactively.

#### When to Check Context Window

- **At the start of EVERY new user prompt**: Before beginning work on any task
- **When approaching 100,000 tokens**: Proactively warn the user
- **Before reading large files**: Especially HTML snapshots or log files

#### How to Check Context Window

Monitor the token usage displayed in system warnings:
```
<system_warning>Token usage: 85000/200000; 115000 remaining</system_warning>
```

#### Action Thresholds

| Token Usage | Remaining | Action Required |
|------------|-----------|-----------------|
| < 100,000  | > 100,000 | Continue normally |
| 100,000-150,000 | 50,000-100,000 | **Warn user** - Context getting full, may need compaction soon |
| 150,000-180,000 | 20,000-50,000 | **Strongly recommend** user runs `/compact` command |
| > 180,000  | < 20,000  | **STOP and request** user runs `/compact` before continuing |

#### Compact Command

When context is too full, ask the user to run:
```
/compact
```

This will:
- Summarize the conversation history
- Reset the context window
- Allow Claude Code to continue with a fresh context

#### Example Workflow

**Good**:
```
User: "Please add comprehensive logging to all framework components"

Claude: "I notice the context window is at 150,000 tokens (30,000 remaining).
Before proceeding with adding logging across all components, I recommend running
the /compact command to ensure we have sufficient space to complete this task
without interruption.

Should I proceed now, or would you like to compact first?"
```

**Bad**:
```
User: "Please add comprehensive logging to all framework components"

Claude: [Starts working without checking context]
[Runs out of context mid-task]
[Cannot complete the work]
```

### Logging Standards

All framework components, page objects, and tests MUST implement comprehensive logging following these standards:

#### Logging Levels

Use appropriate logging levels for different types of messages:

| Level | When to Use | Examples |
|-------|------------|----------|
| **DEBUG** | Detailed diagnostic information | Element located, method entry/exit, configuration values |
| **INFO** | General informational messages about program execution | Page loaded, action completed, test started |
| **WARNING** | Warning messages for unexpected but handled situations | Element not found (but handled), deprecated usage |
| **ERROR** | Error messages for failures that don't stop execution | Element timeout, assertion failure, screenshot save failure |
| **CRITICAL** | Critical errors that may cause program termination | Driver creation failure, config file missing |

#### Framework Component Logging

Every framework component in `src/framework/` MUST include logging:

**Required imports**:
```python
import logging

logger = logging.getLogger(__name__)
```

**Examples from `base_page.py`**:
```python
# DEBUG: Detailed diagnostic information
logger.debug(f"Initialized {self.__class__.__name__} with timeout={timeout}s")
logger.debug(f"Attempting to click element: {locator_str}")
logger.debug(f"Successfully clicked element: {locator_str}")

# INFO: Significant actions
logger.info(f"{self.__class__.__name__}: Opening URL: {url}")
logger.info(f"Saving HTML snapshot for {page_name}")

# WARNING: Unexpected but handled situations
logger.warning(f"Could not cleanup history files for {page_name}: {e}")

# ERROR: Failures with context
logger.error(f"Element not clickable within timeout: {locator_str} on page {current_url}")
logger.error(f"Failed to save HTML snapshot for {page_name}: {e}", exc_info=True)
```

#### Page Object Logging

Page objects in `src/pages/` SHOULD include logging for:

- **Page navigation**: When navigating to the page
- **Key actions**: Login, form submission, critical clicks
- **Data retrieval**: Getting important text or values

**Example**:
```python
import logging

logger = logging.getLogger(__name__)

class GroceryMateLoginPage(BasePage):
    def login(self, username, password):
        """Perform login with provided credentials."""
        logger.info(f"Attempting login for user: {username}")
        try:
            self.enter_text(self.EMAIL_INPUT, username)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.click(self.SIGN_IN_BUTTON)
            logger.info("Login form submitted successfully")
        except Exception as e:
            logger.error(f"Login failed for user {username}: {e}", exc_info=True)
            raise
```

#### Test Logging

Tests SHOULD log:

- **Test steps**: Major steps in the test flow
- **Assertions**: What is being verified
- **Test data**: Important test data being used

**Use the logging utilities** from `src/framework/logger.py`:

```python
from framework.logger import get_test_logger, log_test_step, log_assertion

logger = get_test_logger(__name__)

def test_login_with_valid_credentials(driver):
    log_test_step(logger, "Navigate to login page")
    login_page = GroceryMateLoginPage(driver)
    login_page.navigate_to_login()

    log_test_step(logger, "Perform login with valid credentials")
    login_page.login_with_config_credentials()

    log_test_step(logger, "Verify successful login")
    current_url = driver.current_url
    expected = "not on /auth page"
    actual = f"Current URL: {current_url}"
    passed = 'auth' not in current_url.lower()

    log_assertion(logger, "User redirected from auth page", actual, expected, passed)
    assert passed, f"Login failed - still on auth page: {current_url}"
```

#### Assertion Messages

All assertions MUST include clear, descriptive messages that provide context:

**Bad**:
```python
assert element_visible  # No context!
assert text == "Login"  # What element? Where?
```

**Good**:
```python
assert element_visible, (
    f"Login button should be visible on page {current_url}. "
    f"Locator: {LOGIN_BUTTON}"
)

assert text == "Login", (
    f"Header title should be 'Login' but was '{text}'. "
    f"Page: {current_url}, Locator: {HEADER_TITLE}"
)
```

**Best** (with logging):
```python
log_assertion(logger, "Login button visibility", element_visible, True, element_visible)
assert element_visible, (
    f"Login button should be visible on page {current_url}. "
    f"Locator: {LOGIN_BUTTON}, Timeout: {timeout}s"
)
```

#### Sensitive Data Masking

**ALWAYS** mask sensitive data in logs:

```python
# Mask passwords, tokens, API keys, etc.
display_text = "****" if any(word in locator[1].lower()
                             for word in ['password', 'token', 'secret', 'api_key'])
                else text
logger.debug(f"Entering text '{display_text}' into element: {locator_str}")
```

#### Exception Logging

When logging exceptions, ALWAYS include the stack trace:

```python
try:
    # Some operation
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)  # exc_info=True includes stack trace
    raise
```

#### Log File Organization

Logs are organized as follows:

- **Framework logs**: `logs/framework_YYYYMMDD_HHMMSS.log`
- **Test logs**: `logs/test_name_YYYYMMDD_HHMMSS.log`
- **Console output**: All INFO and above messages
- **File output**: All DEBUG and above messages

Use the logger utilities in `src/framework/logger.py`:

```python
from framework.logger import setup_logger, get_test_logger

# For framework components
logger = setup_logger(__name__, level=logging.INFO)

# For tests (gets both console and file logging)
logger = get_test_logger(__name__)
```

### Logging Best Practices Summary

1. **✅ DO**: Log all significant actions with context
2. **✅ DO**: Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
3. **✅ DO**: Include current URL, locators, and values in error messages
4. **✅ DO**: Mask sensitive data (passwords, tokens, API keys)
5. **✅ DO**: Include stack traces for exceptions (`exc_info=True`)
6. **✅ DO**: Write clear assertion messages with full context
7. **❌ DON'T**: Log sensitive data in plain text
8. **❌ DON'T**: Use print() statements - use logger instead
9. **❌ DON'T**: Write assertions without descriptive messages
10. **❌ DON'T**: Swallow exceptions without logging

### Framework Extensibility

This framework is designed to be reusable for **any website**, not just GroceryMate:

#### GroceryMate as an Example

- `src/pages/grocerymate_*.py` - Example page objects for GroceryMate
- `tests/test_grocerymate*.py` - Example tests for GroceryMate

#### Adding New Websites

To test a different website:

1. **Update config.yaml** with the new base URL
2. **Create new page objects** in `src/pages/your_site_*.py`
3. **Create new tests** in `tests/test_your_site*.py`
4. **Follow the HTML snapshot workflow** to build page objects
5. **Use the same logging standards** as the example files

The framework components (`src/framework/`) remain unchanged and work with any website.

**Example structure for testing multiple sites**:
```
src/pages/
├── grocerymate_home_page.py    # Example: GroceryMate
├── grocerymate_login_page.py   # Example: GroceryMate
├── amazon_home_page.py          # Your site: Amazon
├── amazon_product_page.py       # Your site: Amazon
└── github_repo_page.py          # Your site: GitHub

tests/
├── test_grocerymate.py          # Example tests
├── test_grocerymate_login.py    # Example tests
├── test_amazon.py               # Your tests
└── test_github.py               # Your tests
```

Keep the GroceryMate files as examples and reference implementations.
