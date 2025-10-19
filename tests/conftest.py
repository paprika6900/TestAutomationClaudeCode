"""
Pytest configuration and fixtures for selenium tests.
"""
import pytest
from pathlib import Path
from framework.driver_manager import DriverManager
from framework.config_manager import config


@pytest.fixture(scope="function")
def driver():
    """
    Pytest fixture that provides a WebDriver instance for each test.

    Scope: function - creates a new driver for each test function.

    Yields:
        WebDriver instance

    After test:
        - Takes screenshot on failure if configured
        - Quits the driver
    """
    # Create driver
    driver_instance = DriverManager.get_driver()

    yield driver_instance

    # Teardown
    DriverManager.quit_driver(driver_instance)


@pytest.fixture(scope="function")
def driver_with_screenshots(request, driver):
    """
    Pytest fixture that provides a WebDriver instance and automatically
    takes screenshots on test failure.

    Scope: function - creates a new driver for each test function.

    Yields:
        WebDriver instance

    After test:
        - Takes screenshot on failure
        - Quits the driver
    """
    yield driver

    # Take screenshot on failure
    if request.node.rep_call.failed and config.get('selenium.screenshots_on_failure', True):
        _take_failure_screenshot(driver, request.node.nodeid)


@pytest.fixture(scope="session")
def driver_session():
    """
    Pytest fixture that provides a WebDriver instance for the entire test session.

    Scope: session - creates one driver for all tests (faster but less isolated).

    Use with caution as state may carry over between tests.

    Yields:
        WebDriver instance
    """
    driver_instance = DriverManager.get_driver()

    yield driver_instance

    DriverManager.quit_driver(driver_instance)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook to make test results available to fixtures.

    This allows the driver_with_screenshots fixture to know if a test failed.
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


def _take_failure_screenshot(driver, test_name: str):
    """
    Take a screenshot when a test fails.

    Args:
        driver: WebDriver instance
        test_name: Name/ID of the failed test
    """
    try:
        # Create screenshots directory
        project_root = Path(__file__).parent.parent
        screenshot_dir = project_root / config.get('selenium.screenshots_dir', 'screenshots') / "failures"
        screenshot_dir.mkdir(parents=True, exist_ok=True)

        # Clean up test name for filename
        safe_name = test_name.replace("::", "_").replace("/", "_").replace("\\", "_")
        screenshot_path = screenshot_dir / f"{safe_name}.png"

        # Take screenshot
        driver.save_screenshot(str(screenshot_path))
        print(f"\nScreenshot saved: {screenshot_path}")

    except Exception as e:
        print(f"\nFailed to take screenshot: {e}")


# Configuration for pytest
def pytest_configure(config):
    """Add custom markers to pytest."""
    config.addinivalue_line(
        "markers", "ui: mark test as a UI test using selenium"
    )
    config.addinivalue_line(
        "markers", "smoke: mark test as a smoke test"
    )
    config.addinivalue_line(
        "markers", "regression: mark test as a regression test"
    )
