# CLAUDE.md

This file provides workflow and process guidance to Claude Code (claude.ai/code) when working with code in this repository.

**IMPORTANT**: For project documentation, architecture, and usage instructions, see `README.md`. For current tasks and notes, see `NOTEPAD.md`.

## Table of Contents

- [Note-Taking Process](#note-taking-process)
- [Context Window Management](#context-window-management)
- [Git Workflow](#git-workflow)
- [Logging Standards](#logging-standards)
- [Code Quality Standards](#code-quality-standards)

## Note-Taking Process

**CRITICAL**: Claude Code MUST use `NOTEPAD.md` to track all tasks, notes, and session information.

### When to Update NOTEPAD.md

Update `NOTEPAD.md` at these key moments:

1. **At the start of each new session**:
   - Update "Current Session Notes" with date and current branch
   - Review and update "Active Tasks" section
   - Clear out completed tasks from previous sessions

2. **When receiving new tasks from the user**:
   - Add tasks to "Active Tasks" or "Pending Tasks"
   - Use checkbox format: `- [ ] Task description`
   - Mark completed with: `- [x] Task description`

3. **During work**:
   - Update task status as you progress
   - Add important notes, decisions, or discoveries to "Important Notes"
   - Document any issues encountered

4. **When completing work**:
   - Mark tasks as complete
   - Move relevant information to "Session History"
   - Update "Known Issues" if applicable

5. **When blocked or have questions**:
   - Add to "Questions for User" section
   - Document blocking issues in "Known Issues"

### NOTEPAD.md Structure

The file should maintain these sections:

- **Current Session Notes**: Date, branch, active work
- **Active Tasks**: Tasks currently in progress (use TodoWrite tool in parallel)
- **Pending Tasks**: Tasks queued for future work
- **Future Tasks**: Long-term improvements and ideas
- **Important Notes**: Key decisions, discoveries, configuration details
- **Session History**: Summary of completed sessions and PRs
- **Known Issues**: Open and resolved issues
- **Questions for User**: Items requiring user input
- **Useful Commands**: Frequently used commands for this project
- **Code Review Checklist**: Standard checklist for PRs

### Integration with TodoWrite Tool

- **TodoWrite tool**: For immediate, current task tracking (short-term memory)
- **NOTEPAD.md**: For session notes, context, and cross-session tracking (long-term memory)

Both should be used together:
```
User: "Add feature X, Y, and Z"

Claude:
1. Uses TodoWrite to create immediate task list
2. Updates NOTEPAD.md "Active Tasks" with the same tasks
3. Works on tasks, updating both TodoWrite and NOTEPAD.md as progress is made
4. Marks tasks complete in both places
5. Moves completed work to "Session History" in NOTEPAD.md
```

## Context Window Management

**CRITICAL**: Before starting ANY new task, Claude Code MUST check the context window usage and manage it proactively.

### When to Check Context Window

- **At the start of EVERY new user prompt**: Before beginning work on any task
- **When approaching 100,000 tokens**: Proactively warn the user
- **Before reading large files**: Especially HTML snapshots or log files

### How to Check Context Window

Monitor the token usage displayed in system warnings:
```
<system_warning>Token usage: 85000/200000; 115000 remaining</system_warning>
```

### Action Thresholds

| Token Usage | Remaining | Action Required |
|------------|-----------|-----------------|
| < 100,000  | > 100,000 | Continue normally |
| 100,000-150,000 | 50,000-100,000 | **Warn user** - Context getting full, may need compaction soon |
| 150,000-180,000 | 20,000-50,000 | **Strongly recommend** user runs `/compact` command |
| > 180,000  | < 20,000  | **STOP and request** user runs `/compact` before continuing |

### Compact Command

When context is too full, ask the user to run:
```
/compact
```

This will:
- Summarize the conversation history
- Reset the context window
- Allow Claude Code to continue with a fresh context

### Example Workflow

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

## Git Workflow

**IMPORTANT**: When requested to commit and push changes, always follow this workflow.

### Standard Feature Development Workflow

1. **Create a new feature branch** with a clear, descriptive name
   ```bash
   git checkout -b feature/descriptive-name
   ```

   Or for bug fixes:
   ```bash
   git checkout -b fix/descriptive-name
   ```

2. **Stage and commit changes** with a clear commit message explaining all changes
   ```bash
   git add .
   git commit -m "Clear description of changes"
   ```

   For multi-line commit messages with details:
   ```bash
   git commit -m "$(cat <<'EOF'
   Summary line describing the change

   Detailed explanation of what changed and why.

   Changes:
   - Item 1
   - Item 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude <noreply@anthropic.com>
   EOF
   )"
   ```

3. **Push the feature branch** to remote
   ```bash
   git push -u origin feature/descriptive-name
   ```

4. **Create a Pull Request targeting main/master branch**
   - **CRITICAL**: ALWAYS target main/master branch (NOT feature branches)
   - Use `gh pr create --base main` command
   - Include summary of changes and test plan

   Example:
   ```bash
   gh pr create --base main --title "Add feature X" --body "$(cat <<'EOF'
   ## Summary
   Description of changes

   ## Changes
   - Item 1
   - Item 2

   ## Test Plan
   - [ ] Test 1
   - [ ] Test 2

   🤖 Generated with [Claude Code](https://claude.com/claude-code)
   EOF
   )"
   ```

5. **Wait for code review** - Do NOT merge or checkout main until the user completes their review and gives approval

### Why Always Target Main/Master

- This is a **solo developer project** - no need for intermediate feature branches
- Direct PRs to main simplify the workflow
- Easier to track what's in production (main branch)
- Reduces unnecessary branch management overhead

### Creating Pull Requests

When creating PRs, include:
- **Title**: Clear, concise description of the change
- **Summary**: What changed and why
- **Changes**: Bullet list of specific changes
- **Test Plan**: How to verify the changes work
- **Claude Code attribution**: Footer with generation note

### Git Safety

- **NEVER** update git config
- **NEVER** run destructive/irreversible git commands (like `push --force`, `hard reset`) unless explicitly requested
- **NEVER** skip hooks (`--no-verify`, `--no-gpg-sign`) unless explicitly requested
- **NEVER** force push to main/master - warn the user if they request it
- **Avoid** `git commit --amend` unless explicitly requested or fixing pre-commit hook issues

## Logging Standards

All framework components, page objects, and tests MUST implement comprehensive logging following these standards.

### Logging Levels

Use appropriate logging levels for different types of messages:

| Level | When to Use | Examples |
|-------|------------|----------|
| **DEBUG** | Detailed diagnostic information | Element located, method entry/exit, configuration values |
| **INFO** | General informational messages about program execution | Page loaded, action completed, test started |
| **WARNING** | Warning messages for unexpected but handled situations | Element not found (but handled), deprecated usage |
| **ERROR** | Error messages for failures that don't stop execution | Element timeout, assertion failure, screenshot save failure |
| **CRITICAL** | Critical errors that may cause program termination | Driver creation failure, config file missing |

### Framework Component Logging

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

### Page Object Logging

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

### Test Logging

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

### Assertion Messages

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

### Sensitive Data Masking

**ALWAYS** mask sensitive data in logs:

```python
# Mask passwords, tokens, API keys, etc.
display_text = "****" if any(word in locator[1].lower()
                             for word in ['password', 'token', 'secret', 'api_key'])
                else text
logger.debug(f"Entering text '{display_text}' into element: {locator_str}")
```

### Exception Logging

When logging exceptions, ALWAYS include the stack trace:

```python
try:
    # Some operation
except Exception as e:
    logger.error(f"Operation failed: {e}", exc_info=True)  # exc_info=True includes stack trace
    raise
```

### Log File Organization

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

## Code Quality Standards

### Page Object Model (POM) Standards

When creating or modifying page objects:

1. **Inherit from BasePage**: All page objects must extend `BasePage`
2. **Locator Constants**: Define all locators as class constants at the top
   ```python
   ELEMENT_NAME = (By.CSS_SELECTOR, "css.selector")
   ```
3. **Semantic Naming**: Use descriptive names that reflect the element's purpose
4. **Group Locators**: Organize locators by page section with comments
5. **Method Names**: Use clear, action-based method names (`click_submit_button`, not `click_button1`)
6. **Documentation**: Include docstrings for all methods
7. **Logging**: Add appropriate logging to all interactions

### Locator Strategy

Prefer locators in this order:
1. **CSS Selectors** (most stable, readable)
2. **IDs** (if unique and semantic)
3. **Data attributes** (if available, e.g., `data-testid`)
4. **XPath** (last resort, harder to maintain)

### Test Organization

1. **One test class per page**: Group related tests in classes named `TestPageName`
2. **Use markers**: Apply appropriate markers (`@pytest.mark.ui`, `@pytest.mark.smoke`, etc.)
3. **Descriptive test names**: `test_login_with_valid_credentials` not `test_1`
4. **Arrange-Act-Assert**: Structure tests clearly
5. **Independent tests**: Each test should be able to run independently
6. **Use fixtures**: Leverage pytest fixtures from `conftest.py`

### Configuration

- **Never hardcode**: Use `config.yaml` for all configurable values
- **No secrets in code**: Credentials should be in `config.yaml` (gitignored in production)
- **Environment-specific**: Support different configs for dev/test/prod

### Error Handling

1. **Let exceptions bubble**: Don't catch and swallow exceptions unless you have a specific reason
2. **Add context**: When catching exceptions, add context before re-raising
3. **Log before raising**: Use `logger.error()` with `exc_info=True` before raising
4. **Clear messages**: Assertion and exception messages should clearly state what went wrong

## Summary

- **README.md**: Project documentation (what, how, architecture)
- **CLAUDE.md**: Process instructions (workflow, standards, how to work)
- **NOTEPAD.md**: Task tracking and session notes (current state, todos, history)

Claude Code should:
1. **Check context window** before starting work
2. **Update NOTEPAD.md** throughout the session
3. **Follow Git workflow** for all changes
4. **Apply logging standards** to all code
5. **Follow POM standards** for page objects and tests
6. **Create PRs to main** with clear descriptions
7. **Wait for review** before merging
