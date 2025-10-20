# CLAUDE.md - Workflow Instructions

**Purpose**: Process and workflow guidance for Claude Code when working in this repository.

**CRITICAL - READ THIS FIRST**:
- When user asks about **project setup, architecture, features, or how to use the framework** → Read `README.md` FIRST
- For **current tasks and session context** → Check `NOTEPAD.md`
- For **detailed technical architecture** → See `docs/ARCHITECTURE.md`

## Quick Reference

| Topic | Action |
|-------|--------|
| New session starts | Pull main, update NOTEPAD.md current session |
| User asks "how does X work?" | Read README.md or docs/ARCHITECTURE.md |
| Implementing feature | Use TodoWrite + update NOTEPAD.md |
| Need logging example | See docs/ARCHITECTURE.md → Logging section |
| Creating PR | Follow Git Workflow below, STOP and wait |
| Context > 150K tokens | Request `/compact` from user |

## Session Start Checklist

Every new session, run through this:

```bash
# 1. Pull latest from main
git checkout main && git pull origin main

# 2. Update NOTEPAD.md
# - Clear "Current Session Notes"
# - Move completed tasks to "Session History"
# - Set new session date

# 3. Check context window
# - If approaching limits, warn user

# 4. Review pending tasks
# - Check NOTEPAD.md "Pending Tasks"
```

## Git Workflow (CRITICAL)

### Before Any Work
```bash
git checkout main
git pull origin main
# NEVER skip this step!
```

### Development Flow
1. **Create branch**: `git checkout -b feature/name`
2. **Work & commit**: Regular commits with clear messages
3. **Push**: `git push -u origin feature/name`
4. **Create PR**: `gh pr create --base main --title "..." --body "..."`
5. **🛑 STOP**: Wait for user confirmation PR is merged
6. **After merge**: `git checkout main && git pull origin main`
7. **Repeat** from step 1 for next task

**NEVER** continue work on branch after creating PR!

## Context Window Management

| Tokens Used | Action |
|-------------|--------|
| < 100K | Continue normally |
| 100-150K | Warn user context filling up |
| 150-180K | Strongly recommend `/compact` |
| > 180K | STOP - request `/compact` before continuing |

## NOTEPAD.md Management

**Update these sections actively**:
- **Current Session Notes**: Date, branch, active work
- **Active Tasks**: What you're working on NOW
- **Important Notes**: Key decisions, discoveries
- **Session History**: Completed work (archive after 5 sessions)

**Archive trigger**: When NOTEPAD.md > 300 lines, move old sessions to `docs/SESSION_HISTORY.md`

## Code Quality Checklist

When writing code, ensure:
- [ ] Logging added (DEBUG/INFO/WARNING/ERROR levels)
- [ ] Sensitive data masked in logs
- [ ] Clear assertion messages with context
- [ ] Docstrings for all methods
- [ ] Error messages include URL + locator
- [ ] No hardcoded values (use config.yaml)

## Logging Quick Reference

```python
import logging
logger = logging.getLogger(__name__)

# Use appropriate levels
logger.debug(f"Element found: {locator}")  # Diagnostic detail
logger.info(f"Page loaded: {url}")          # General flow
logger.warning(f"Element slow: {locator}")  # Unexpected but handled
logger.error(f"Failed: {e}", exc_info=True) # Errors with stack trace

# Mask sensitive data
display = "****" if 'password' in field.lower() else value
```

## POM Standards Quick Reference

```python
# Page Object Structure
class ExamplePage(BasePage):
    # 1. Locators at top (grouped by section)
    LOGIN_BUTTON = (By.CSS_SELECTOR, ".login-btn")

    # 2. Methods with docstrings
    def click_login(self):
        """Click the login button."""
        logger.info("Clicking login button")
        self.click(self.LOGIN_BUTTON)

# Locator preference: CSS > ID > data-testid > XPath
```

## PR Template

```markdown
## Summary
[What changed and why]

## Changes
- Item 1
- Item 2

## Test Plan
- [ ] Test 1
- [ ] Test 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## When to Read Other Docs

**README.md** - Read when:
- User asks "how do I setup/install/run?"
- Need to understand project features
- Explaining framework to user
- User asks "what does this project do?"

**docs/ARCHITECTURE.md** - Read when:
- Implementing new framework components
- Need detailed logging examples
- Understanding BasePage or DriverManager
- Working with HTML snapshots

**NOTEPAD.md** - Read when:
- Starting new session
- Need context on previous work
- Checking what's pending
- Adding new tasks

## Git Safety Rules

**NEVER**:
- Update git config
- Force push to main
- Skip pre-commit hooks
- Amend commits (unless pre-commit fix)
- Push without pulling first

## Common Commands

```bash
# Run tests
pytest -m smoke -v
pytest tests/test_file.py -v

# HTML snapshot capture
pytest tests/test_html_snapshots.py -m html_capture

# Create PR
gh pr create --base main --title "..." --body "..."

# Check PR status
gh pr view <number>
```

---

**Remember**: This file is for WORKFLOW. For WHAT and HOW, read README.md or docs/ARCHITECTURE.md.
