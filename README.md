# TestAutomationClaudeCode

**Selenium + Pytest + Page Object Model + Claude Code Integration**

A Python test automation framework designed for Claude Code collaboration. Automatically captures HTML snapshots for AI-assisted page object creation.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run smoke tests
pytest -m smoke -v

# 3. Capture HTML snapshots for new pages
pytest tests/test_html_snapshots.py -m html_capture
```

**First time using this framework?** See [Complete Setup Guide](#development-setup) below.

---

## 📋 Table of Contents

- [Key Features](#key-features)
- [Project Structure](#project-structure)
- [Development Setup](#development-setup)
- [Running Tests](#running-tests)
- [Claude Code Workflow](#claude-code-workflow)
- [Framework Extensibility](#framework-extensibility)
- [Documentation](#documentation)

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **🎯 Page Object Model** | Clean separation of test logic and page interactions |
| **📸 Auto HTML Snapshots** | Captures page HTML for Claude Code to analyze and build locators |
| **🌐 Cross-Platform** | Works on Windows, Linux, and macOS (auto-downloads drivers) |
| **📝 Comprehensive Logging** | Debug-friendly logging at all levels with sensitive data masking |
| **⚙️ YAML Configuration** | Easy customization without code changes |
| **🔄 Multi-Browser** | Chrome and Firefox supported out of the box |

---

## 📁 Project Structure

```
TestAutomationClaudeCode/
├── src/
│   ├── framework/           # Core framework (reusable for any website)
│   │   ├── base_page.py     # Base page object with HTML snapshots
│   │   ├── driver_manager.py # WebDriver factory
│   │   ├── config_manager.py # Config access
│   │   └── logger.py        # Logging utilities
│   └── pages/               # Page objects (website-specific)
│       ├── grocerymate_home_page.py    # Example
│       └── grocerymate_login_page.py   # Example
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_grocerymate.py  # Functional tests (example)
│   └── test_html_snapshots.py # HTML capture tests
├── docs/
│   └── ARCHITECTURE.md      # Detailed technical docs
├── config.yaml              # Configuration file
├── CLAUDE.md                # Claude Code workflow instructions
├── NOTEPAD.md               # Task tracking
└── README.md                # This file
```

**Auto-generated directories** (gitignored):
- `page_snapshots/` - HTML snapshots
- `screenshots/failures/` - Failure screenshots
- `logs/` - Test execution logs

---

## 🛠️ Development Setup

### Prerequisites

- **Python 3.8+**
- **Chrome or Firefox browser**
- **No manual driver installation needed!** (auto-managed)

### Installation

**Option 1: pip (Recommended)**
```bash
pip install -r requirements.txt
```

**Option 2: apt (Linux)**
```bash
sudo apt update
sudo apt install -y python3-pytest python3-selenium python3-yaml
```

### Browser Setup

**No manual driver installation required!** The framework uses `webdriver-manager` to automatically download the correct driver for your OS.

- **Chrome**: Install Google Chrome → framework auto-downloads ChromeDriver on first run
- **Firefox**: Install Firefox → framework auto-downloads GeckoDriver on first run

### Configuration

Edit `config.yaml` to customize:

```yaml
browser:
  name: "chrome"              # or "firefox"
  headless: false             # true for CI/headless mode
  window_size: "1920x1080"

test_data:
  base_url: "https://your-site.com/"
  login:
    username: "your_user"
    password: "your_password"
```

---

## 🧪 Running Tests

### Quick Commands

```bash
# Run all UI tests
pytest -m ui -v

# Run smoke tests only
pytest -m smoke -v

# Run specific test file
pytest tests/test_grocerymate.py -v

# Run with debug logging
pytest -v --log-cli-level=DEBUG
```

### Test Markers

| Marker | Description | Command |
|--------|-------------|---------|
| `@pytest.mark.ui` | All UI tests | `pytest -m ui` |
| `@pytest.mark.smoke` | Critical tests | `pytest -m smoke` |
| `@pytest.mark.functional` | Functional tests | `pytest -m functional` |
| `@pytest.mark.html_capture` | HTML snapshots | `pytest -m html_capture` |

### Combine Markers

```bash
pytest -m "ui and smoke"           # UI smoke tests only
pytest -m "functional and not smoke" # Functional except smoke
```

---

## 🤖 Claude Code Workflow

**This framework is designed for AI-assisted test creation using Claude Code.**

### Step-by-Step Process

#### 1️⃣ Capture HTML Snapshot

Create a test that navigates to your target page:

```python
# In tests/test_html_snapshots.py
@pytest.mark.html_capture
def test_capture_login_page(driver):
    """Capture HTML snapshot of login page."""
    page = LoginPage(driver)
    page.navigate_to_login()
    page.save_html_snapshot(keep_history=2)
    assert driver.current_url is not None
```

Run it:
```bash
pytest tests/test_html_snapshots.py::test_capture_login_page -v
```

#### 2️⃣ Ask Claude Code to Build Page Object

Provide this prompt to Claude Code:

```
"Read page_snapshots/LoginPage.html and build a complete Page Object Model
with locators for all interactive elements (forms, buttons, links, etc.)"
```

#### 3️⃣ Claude Code Creates Page Object

Claude Code will:
- ✅ Analyze the HTML structure
- ✅ Identify all interactive elements
- ✅ Create semantic CSS selectors
- ✅ Generate a complete page object class with methods
- ✅ Add proper logging and documentation

#### 4️⃣ Write Functional Tests

Now use the page object in your tests:

```python
@pytest.mark.functional
@pytest.mark.smoke
def test_login_success(driver):
    """Test successful login."""
    page = LoginPage(driver)
    page.navigate_to_login()
    page.login("user@example.com", "password123")

    assert 'dashboard' in driver.current_url, "Should redirect to dashboard"
```

### Why This Works

- **Accurate Locators**: Claude analyzes actual HTML, not assumptions
- **Fast Development**: No manual DevTools inspection
- **Always Up-to-Date**: Re-run HTML capture after UI changes
- **Complete Coverage**: Claude identifies ALL elements, not just obvious ones

---

## 🔧 Framework Extensibility

**GroceryMate is just an example!** This framework works with ANY website.

### Adding a New Website

1. **Update config.yaml**:
   ```yaml
   test_data:
     base_url: "https://your-new-site.com/"
   ```

2. **Create page objects** in `src/pages/yoursite_*.py`:
   ```python
   from framework.base_page import BasePage

   class YourSiteHomePage(BasePage):
       # Claude Code will fill this in!
       pass
   ```

3. **Capture HTML** → **Ask Claude** → **Build Page Objects** → **Write Tests**

4. **Framework components stay unchanged!** Only add new page objects and tests.

### Multi-Website Example

```
src/pages/
├── grocerymate_*.py      # Website 1 (example)
├── amazon_*.py           # Website 2 (your site)
└── github_*.py           # Website 3 (your site)

tests/
├── test_grocerymate.py   # Tests for site 1
├── test_amazon.py        # Tests for site 2
└── test_github.py        # Tests for site 3
```

---

## 📚 Documentation

| Document | Purpose | When to Read |
|----------|---------|--------------|
| **README.md** (this file) | Quick start, overview, setup | Getting started, explaining to others |
| **[CLAUDE.md](CLAUDE.md)** | Workflow instructions for Claude Code | Working with Claude Code |
| **[NOTEPAD.md](NOTEPAD.md)** | Task tracking and session notes | Checking current tasks/context |
| **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** | Detailed technical reference | Implementing features, debugging |

### Quick Links

- **Need help with setup?** → This README (Development Setup section)
- **Working with Claude Code?** → Read [CLAUDE.md](CLAUDE.md)
- **Want technical details?** → Read [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- **What's being worked on?** → Check [NOTEPAD.md](NOTEPAD.md)

---

## 🎯 Example: GroceryMate

The GroceryMate page objects demonstrate the framework in action:

- **10 passing tests** across home and login pages
- **Page objects built from HTML snapshots** using Claude Code
- **Complete logging** and error handling
- **Production-ready code** with documentation

View the examples:
- [grocerymate_home_page.py](src/pages/grocerymate_home_page.py) - 12 locators, 14 methods
- [grocerymate_login_page.py](src/pages/grocerymate_login_page.py) - 7 locators, 8 methods
- [test_grocerymate.py](tests/test_grocerymate.py) - Functional tests
- [test_html_snapshots.py](tests/test_html_snapshots.py) - HTML capture workflow

---

## 🤝 Contributing

This project is designed for Claude Code collaboration. See [CLAUDE.md](CLAUDE.md) for workflow instructions.

---

## 📄 License

Provided as-is for educational and testing purposes.

---

**Questions?** Check [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed technical documentation.
