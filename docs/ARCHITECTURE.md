# Architecture Documentation

Complete technical reference for the TestAutomationClaudeCode framework.

## Framework Components

### BasePage (`src/framework/base_page.py`)

**Purpose**: Base class for all page objects with common interaction methods and HTML snapshot capability.

**Key Methods**:
- `click(locator)` - Click element with wait
- `enter_text(locator, text)` - Enter text with clear
- `get_text(locator)` - Get element text
- `is_element_visible(locator)` - Check visibility
- `save_html_snapshot(keep_history=2)` - Manual snapshot capture
- `take_screenshot(filename)` - Save screenshot

**Logging Examples**:
```python
import logging
logger = logging.getLogger(__name__)

# In __init__
logger.debug(f"Initialized {self.__class__.__name__} with timeout={timeout}s")

# In click()
logger.debug(f"Attempting to click element: {locator_str}")
logger.debug(f"Successfully clicked element: {locator_str}")

# On error
logger.error(f"Element not clickable: {locator_str} on page {current_url}")
```

**HTML Snapshot System**:
- Automatically saves on page load
- Location: `page_snapshots/PageName.html`
- History: `page_snapshots/history/PageName_YYYYMMDD_HHMMSS.html`
- Configurable history retention (default: 2 versions)

### DriverManager (`src/framework/driver_manager.py`)

**Purpose**: Factory for creating and configuring WebDriver instances.

**Key Methods**:
- `get_driver()` - Create configured driver
- `quit_driver(driver)` - Safe driver cleanup

**Features**:
- Auto-downloads drivers via `webdriver-manager`
- Cross-platform (Windows, Linux, macOS)
- Configurable via `config.yaml`
- Supports Chrome and Firefox

**Configuration Options** (in `config.yaml`):
```yaml
browser:
  name: "chrome"
  headless: false
  window_size: "1920x1080"
  implicit_wait: 10
  page_load_timeout: 30
```

**Logging Examples**:
```python
logger.info(f"Creating WebDriver for browser: {browser_name}")
logger.debug(f"Headless: {headless}, Window: {window_size}")
logger.info(f"Successfully created {browser_name} WebDriver")
```

### ConfigManager (`src/framework/config_manager.py`)

**Purpose**: Singleton for accessing `config.yaml` settings with dot-notation.

**Usage**:
```python
from framework.config_manager import config

# Get values with dot notation
base_url = config.get('test_data.base_url')
username = config.get('test_data.login.username')
headless = config.get('browser.headless', False)  # with default
```

**Benefits**:
- Single source of truth for configuration
- Type-safe access
- Default value support
- Nested key access with dots

### Logger (`src/framework/logger.py`)

**Purpose**: Centralized logging configuration and utilities.

**Functions**:

```python
# Setup logger for framework components
from framework.logger import setup_logger
logger = setup_logger(__name__, level=logging.INFO)

# Setup logger for tests (includes file logging)
from framework.logger import get_test_logger
logger = get_test_logger(__name__)

# Log test steps with visual separation
from framework.logger import log_test_step
log_test_step(logger, "Navigate to login page")

# Log assertions with pass/fail
from framework.logger import log_assertion
log_assertion(logger, "Login successful", actual, expected, passed)
```

**Log Organization**:
- Framework logs: `logs/framework_YYYYMMDD_HHMMSS.log`
- Test logs: `logs/test_name_YYYYMMDD_HHMMSS.log`
- Console: INFO and above
- File: DEBUG and above

**Log Levels Guide**:

| Level | Use For | Example |
|-------|---------|---------|
| DEBUG | Diagnostic details | `Element located at {locator}` |
| INFO | General flow | `Page loaded: {url}` |
| WARNING | Unexpected but handled | `Element slow to load` |
| ERROR | Failures | `Login failed: {error}` |
| CRITICAL | Fatal errors | `Driver creation failed` |

**Sensitive Data Masking**:
```python
# ALWAYS mask passwords, tokens, API keys
display_text = "****" if any(word in field.lower()
                             for word in ['password', 'token', 'secret', 'api_key'])
                else text
logger.debug(f"Entering text '{display_text}' into {locator}")
```

**Exception Logging**:
```python
try:
    some_operation()
except Exception as e:
    # ALWAYS include exc_info=True for stack traces
    logger.error(f"Operation failed: {e}", exc_info=True)
    raise
```

## Page Object Model Standards

### Structure

```python
from selenium.webdriver.common.by import By
from framework.base_page import BasePage
import logging

logger = logging.getLogger(__name__)

class ExamplePage(BasePage):
    """
    Page Object for Example page.

    URL: https://example.com/page
    """

    # ==================== LOCATORS ====================
    # Group by page section with comments

    # Header Section
    LOGO = (By.CSS_SELECTOR, ".header img.logo")
    USER_MENU = (By.CSS_SELECTOR, ".user-menu")

    # Login Form
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # ==================== METHODS ====================

    def __init__(self, driver):
        """Initialize the Example page."""
        super().__init__(driver)

    def login(self, email, password):
        """
        Perform login with provided credentials.

        Args:
            email: User email address
            password: User password
        """
        logger.info(f"Attempting login for user: {email}")
        try:
            self.enter_text(self.EMAIL_INPUT, email)
            self.enter_text(self.PASSWORD_INPUT, password)
            self.click(self.LOGIN_BUTTON)
            logger.info("Login form submitted successfully")
        except Exception as e:
            logger.error(f"Login failed for {email}: {e}", exc_info=True)
            raise
```

### Locator Strategy Priority

1. **CSS Selectors** (Preferred)
   ```python
   BUTTON = (By.CSS_SELECTOR, ".submit-btn")
   INPUT = (By.CSS_SELECTOR, "input[name='email']")
   ```

2. **IDs** (If unique and semantic)
   ```python
   FORM = (By.ID, "login-form")
   ```

3. **Data Attributes** (If available)
   ```python
   BUTTON = (By.CSS_SELECTOR, "[data-testid='submit']")
   ```

4. **XPath** (Last resort)
   ```python
   LINK = (By.XPATH, "//a[contains(text(), 'Login')]")
   ```

### Naming Conventions

- **Locators**: `UPPERCASE_SNAKE_CASE`
- **Methods**: `lowercase_snake_case`
- **Classes**: `PascalCase` ending with `Page`
- Be descriptive: `LOGIN_BUTTON` not `BUTTON_1`

## Test Organization

### Test Structure

```python
import pytest
from pages.example_page import ExamplePage
from framework.logger import get_test_logger, log_test_step, log_assertion

logger = get_test_logger(__name__)

@pytest.mark.functional
@pytest.mark.smoke
class TestExamplePage:
    """Functional tests for Example page."""

    def test_login_with_valid_credentials(self, driver):
        """
        Test login with valid credentials.

        Steps:
        1. Navigate to login page
        2. Enter valid credentials
        3. Click login button
        4. Verify successful login
        """
        log_test_step(logger, "Navigate to login page")
        page = ExamplePage(driver)
        page.navigate_to_login()

        log_test_step(logger, "Perform login")
        page.login("user@example.com", "password123")

        log_test_step(logger, "Verify login success")
        current_url = driver.current_url
        passed = 'dashboard' in current_url
        log_assertion(logger, "Redirected to dashboard",
                     current_url, "dashboard page", passed)

        assert passed, (
            f"Should redirect to dashboard after login. "
            f"Current URL: {current_url}"
        )
```

### Test Markers

Define in `pytest.ini`:
```ini
[pytest]
markers =
    ui: UI tests using Selenium
    smoke: Critical functionality tests
    regression: Full regression suite
    functional: Functional tests
    html_capture: HTML snapshot capture tests
```

Usage:
```bash
pytest -m smoke              # Run smoke tests
pytest -m "ui and smoke"     # Run UI smoke tests
pytest -m "not regression"   # Skip regression
```

### Fixtures (`tests/conftest.py`)

**driver** - Function scope, new driver per test:
```python
@pytest.fixture
def driver():
    """Create driver for each test."""
    driver = DriverManager.get_driver()
    yield driver
    DriverManager.quit_driver(driver)
```

**driver_session** - Session scope, one driver for all tests:
```python
@pytest.fixture(scope="session")
def driver_session():
    """Create one driver for entire session."""
    driver = DriverManager.get_driver()
    yield driver
    DriverManager.quit_driver(driver)
```

**driver_with_screenshots** - Captures screenshot on failure:
```python
@pytest.fixture
def driver_with_screenshots(request, driver):
    """Driver that takes screenshot on test failure."""
    yield driver
    if request.node.rep_call.failed:
        screenshot_path = f"screenshots/failures/{request.node.name}.png"
        driver.save_screenshot(screenshot_path)
```

## Assertion Best Practices

### Bad Assertions
```python
assert element_visible  # No context!
assert text == "Login"  # What element? Where?
```

### Good Assertions
```python
assert element_visible, (
    f"Login button should be visible on page {current_url}. "
    f"Locator: {LOGIN_BUTTON}, Timeout: {timeout}s"
)

assert text == "Login", (
    f"Header title should be 'Login' but was '{text}'. "
    f"Page: {current_url}, Locator: {HEADER_TITLE}"
)
```

### Best Assertions (with logging)
```python
from framework.logger import log_assertion

passed = element_visible
log_assertion(logger, "Login button visibility",
             element_visible, True, passed)

assert passed, (
    f"Login button should be visible. "
    f"Page: {current_url}, Locator: {LOGIN_BUTTON}"
)
```

## HTML Snapshot Workflow Details

### Automatic Snapshots

Triggered when:
- Page object `__init__()` is called
- `open()` method is called
- `open_home_page()` or similar navigation methods

Location: `page_snapshots/PageClassName.html`

### Manual Snapshots

```python
# In test
page = GroceryMateHomePage(driver)
page.open_home_page()

# Manually save with 2-version history
page.save_html_snapshot(keep_history=2)
```

### Snapshot Analysis Workflow

1. **Run HTML capture test**:
   ```bash
   pytest tests/test_html_snapshots.py::test_capture_home_page_html -v
   ```

2. **Ask Claude Code to analyze**:
   ```
   "Read page_snapshots/GroceryMateHomePage.html and build a Page Object
   with locators for all interactive elements."
   ```

3. **Claude Code creates complete page object** with:
   - Organized locators
   - Interaction methods
   - Documentation
   - Logging

4. **Run functional tests** to verify locators work

### Large HTML Files

If snapshot is too large:
- **Extract sections**: `grep -A 10 "nav" page_snapshots/Page.html`
- **Focus request**: "Analyze only the header section"
- **Split analysis**: Header first, then content, then footer

## Configuration Reference

### config.yaml Structure

```yaml
browser:
  name: "chrome"
  headless: false
  window_size: "1920x1080"
  implicit_wait: 10
  page_load_timeout: 30

selenium:
  screenshot_on_failure: true
  screenshot_path: "screenshots/failures"
  html_snapshot_path: "page_snapshots"
  html_snapshot_history_path: "page_snapshots/history"
  html_snapshot_history_keep: 2

test_data:
  base_url: "https://grocerymate.masterschool.com/"
  login:
    username: "user@user.com"
    password: "user123"

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### Environment-Specific Configs

For different environments (dev/staging/prod):

```bash
# config.dev.yaml
test_data:
  base_url: "https://dev.example.com/"

# config.prod.yaml
test_data:
  base_url: "https://example.com/"
```

Load via environment variable:
```python
config_file = os.getenv('TEST_CONFIG', 'config.yaml')
```

## Framework Extensibility

### Adding New Websites

The framework is designed to test ANY website:

1. **Update config** with new base URL
2. **Create page objects** in `src/pages/yoursite_*.py`
3. **Create HTML capture tests** in `tests/test_html_snapshots.py`
4. **Use Claude Code** to build page objects from snapshots
5. **Create functional tests** in `tests/test_yoursite_*.py`

Framework components remain unchanged!

### Multi-Site Example

```
src/pages/
├── grocerymate_home_page.py    # Site 1
├── grocerymate_login_page.py
├── amazon_home_page.py         # Site 2
├── amazon_product_page.py
└── github_repo_page.py         # Site 3

tests/
├── test_grocerymate.py
├── test_amazon.py
└── test_github.py
```

### Custom Base Page Extensions

Create site-specific base pages:

```python
from framework.base_page import BasePage

class AmazonBasePage(BasePage):
    """Base page for all Amazon pages."""

    def wait_for_amazon_spinner(self):
        """Wait for Amazon loading spinner to disappear."""
        # Custom wait logic
        pass

    def handle_amazon_popup(self):
        """Dismiss Amazon pop-ups if present."""
        # Custom popup handling
        pass
```

## Performance Tips

### Optimize Test Speed

1. **Use session-scoped driver** for independent tests
2. **Disable headless mode** only when debugging
3. **Reduce implicit waits** for fast pages
4. **Parallel execution**: `pytest -n auto`
5. **Skip HTML snapshots** in CI: Set env var to disable

### Reduce Flakiness

1. **Explicit waits** over sleeps
2. **Retry mechanisms** for unstable elements
3. **Screenshot on failure** for debugging
4. **Proper test isolation** (clean state per test)

## Troubleshooting

### Common Issues

**Driver not found**:
- Ensure `webdriver-manager` is installed
- Check internet connection (downloads driver)

**Element not found**:
- Verify locator in HTML snapshot
- Check timing (add explicit wait)
- Inspect element visibility

**Stale element**:
- Re-locate element after page change
- Use fresh page object instance

**Timeout**:
- Increase `page_load_timeout` in config
- Check network/page load speed

### Debug Mode

Enable verbose logging:
```bash
pytest -v --log-cli-level=DEBUG
```

Or in config:
```yaml
logging:
  level: "DEBUG"
```
