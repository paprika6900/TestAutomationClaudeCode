"""
Base Page Object Model class with HTML snapshot capability for Claude Code integration.
"""
import os
import time
import logging
from pathlib import Path
from datetime import datetime
from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from framework.config_manager import config

# Configure logger for this module
logger = logging.getLogger(__name__)


class BasePage:
    """
    Base class for all Page Objects.

    Provides common page interaction methods and manual HTML snapshot capability.
    HTML snapshots can be captured on-demand for Claude Code analysis using the
    save_html_snapshot() method. History is maintained with configurable retention
    (default: 2 versions) to avoid excessive storage overhead.
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize the base page.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver
        timeout = config.get('selenium.page_load_timeout', 30)
        self.wait = WebDriverWait(driver, timeout)
        logger.debug(f"Initialized {self.__class__.__name__} with timeout={timeout}s")

    def save_html_snapshot(self, keep_history: int = 2):
        """
        Manually save the current page HTML to a snapshot file.
        This allows Claude Code to read the HTML and identify accurate locators.

        Args:
            keep_history: Number of historical versions to keep (default: 2)
        """
        page_name = self.__class__.__name__
        logger.info(f"Saving HTML snapshot for {page_name}, keeping {keep_history} historical versions")

        snapshot_dir = self._get_snapshot_directory()
        os.makedirs(snapshot_dir, exist_ok=True)

        # Create filename based on page class name
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{page_name}.html"
        filepath = snapshot_dir / filename

        # Save the page source
        try:
            html_content = self.driver.page_source
            content_size = len(html_content)

            # Save current version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.debug(f"Saved current snapshot: {filepath} ({content_size} bytes)")

            # Save timestamped version for history
            history_dir = snapshot_dir / "history"
            os.makedirs(history_dir, exist_ok=True)
            history_filename = f"{page_name}_{timestamp}.html"
            history_filepath = history_dir / history_filename
            with open(history_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logger.debug(f"Saved historical snapshot: {history_filepath}")

            # Clean up old history files, keeping only the most recent ones
            self._cleanup_history(page_name, history_dir, keep_history)

        except Exception as e:
            logger.error(f"Failed to save HTML snapshot for {page_name}: {e}", exc_info=True)

    def _cleanup_history(self, page_name: str, history_dir: Path, keep_count: int):
        """
        Remove old historical snapshots, keeping only the most recent versions.

        Args:
            page_name: Name of the page class
            history_dir: Directory containing historical snapshots
            keep_count: Number of recent files to keep
        """
        try:
            # Find all history files for this page
            history_files = sorted(
                history_dir.glob(f"{page_name}_*.html"),
                key=lambda p: p.stat().st_mtime,
                reverse=True
            )

            # Delete files beyond the keep_count
            deleted_count = 0
            for old_file in history_files[keep_count:]:
                old_file.unlink()
                deleted_count += 1

            if deleted_count > 0:
                logger.debug(f"Cleaned up {deleted_count} old historical snapshots for {page_name}")

        except Exception as e:
            logger.warning(f"Could not cleanup history files for {page_name}: {e}")

    def _get_snapshot_directory(self) -> Path:
        """Get the directory for storing HTML snapshots."""
        project_root = Path(__file__).parent.parent.parent
        snapshot_dir = config.get('selenium.html_snapshots_dir', 'page_snapshots')
        return project_root / snapshot_dir

    def open(self, url: str = None):
        """
        Open a URL.

        Args:
            url: URL to open. If None, uses base_url from config
        """
        if url is None:
            url = config.get('test_data.base_url')

        logger.info(f"{self.__class__.__name__}: Opening URL: {url}")
        try:
            self.driver.get(url)
            logger.debug(f"Successfully loaded URL: {url}")
        except Exception as e:
            logger.error(f"Failed to open URL '{url}': {e}", exc_info=True)
            raise

    def find_element(self, locator: Tuple[By, str]) -> WebElement:
        """
        Find an element using the specified locator.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            WebElement

        Example:
            element = self.find_element((By.ID, "submit-button"))
        """
        return self.driver.find_element(*locator)

    def find_elements(self, locator: Tuple[By, str]) -> List[WebElement]:
        """
        Find multiple elements using the specified locator.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            List of WebElements
        """
        return self.driver.find_elements(*locator)

    def click(self, locator: Tuple[By, str]):
        """
        Click an element after waiting for it to be clickable.

        Args:
            locator: Tuple of (By, locator_string)

        Raises:
            TimeoutException: If element is not clickable within timeout period
        """
        locator_str = f"{locator[0]}='{locator[1]}'"
        logger.debug(f"Attempting to click element: {locator_str}")

        try:
            element = self.wait.until(EC.element_to_be_clickable(locator))
            element.click()
            logger.debug(f"Successfully clicked element: {locator_str}")
        except TimeoutException:
            current_url = self.driver.current_url
            logger.error(f"Element not clickable within timeout: {locator_str} on page {current_url}")
            raise TimeoutException(
                f"Element with locator {locator_str} was not clickable within timeout. "
                f"Current URL: {current_url}"
            )

    def enter_text(self, locator: Tuple[By, str], text: str):
        """
        Enter text into an input field after waiting for it to be visible.

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to enter

        Raises:
            TimeoutException: If element is not visible within timeout period
        """
        locator_str = f"{locator[0]}='{locator[1]}'"
        # Mask sensitive data in logs (passwords, tokens, etc.)
        display_text = "****" if any(word in locator[1].lower() for word in ['password', 'token', 'secret']) else text
        logger.debug(f"Entering text '{display_text}' into element: {locator_str}")

        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            element.clear()
            element.send_keys(text)
            logger.debug(f"Successfully entered text into element: {locator_str}")
        except TimeoutException:
            current_url = self.driver.current_url
            logger.error(f"Element not visible for text entry: {locator_str} on page {current_url}")
            raise TimeoutException(
                f"Element with locator {locator_str} was not visible for text entry within timeout. "
                f"Current URL: {current_url}"
            )

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get text from an element after waiting for it to be visible.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            Element text

        Raises:
            TimeoutException: If element is not visible within timeout period
        """
        locator_str = f"{locator[0]}='{locator[1]}'"
        logger.debug(f"Getting text from element: {locator_str}")

        try:
            element = self.wait.until(EC.visibility_of_element_located(locator))
            text = element.text
            logger.debug(f"Retrieved text '{text}' from element: {locator_str}")
            return text
        except TimeoutException:
            current_url = self.driver.current_url
            logger.error(f"Element not visible for getting text: {locator_str} on page {current_url}")
            raise TimeoutException(
                f"Element with locator {locator_str} was not visible for getting text within timeout. "
                f"Current URL: {current_url}"
            )

    def is_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if element is visible within the given timeout.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Timeout in seconds. If None, uses default

        Returns:
            True if element is visible, False otherwise
        """
        locator_str = f"{locator[0]}='{locator[1]}'"
        timeout_val = timeout or config.get('selenium.page_load_timeout', 30)
        logger.debug(f"Checking if element is visible: {locator_str} (timeout={timeout_val}s)")

        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.visibility_of_element_located(locator))
            else:
                self.wait.until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element is visible: {locator_str}")
            return True
        except TimeoutException:
            logger.debug(f"Element is not visible: {locator_str}")
            return False

    def wait_for_element(self, locator: Tuple[By, str], timeout: int = None) -> WebElement:
        """
        Wait for element to be present and return it.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Timeout in seconds. If None, uses default

        Returns:
            WebElement
        """
        if timeout:
            wait = WebDriverWait(self.driver, timeout)
            return wait.until(EC.presence_of_element_located(locator))
        return self.wait.until(EC.presence_of_element_located(locator))

    def take_screenshot(self, name: str = None):
        """
        Take a screenshot and save it.

        Args:
            name: Screenshot name. If None, uses timestamp and page name
        """
        screenshot_dir = self._get_screenshot_directory()
        os.makedirs(screenshot_dir, exist_ok=True)

        if name is None:
            page_name = self.__class__.__name__
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            name = f"{page_name}_{timestamp}"

        filepath = screenshot_dir / f"{name}.png"
        try:
            self.driver.save_screenshot(str(filepath))
            logger.info(f"Screenshot saved: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save screenshot '{name}': {e}", exc_info=True)

    def _get_screenshot_directory(self) -> Path:
        """Get the directory for storing screenshots."""
        project_root = Path(__file__).parent.parent.parent
        screenshot_dir = config.get('selenium.screenshots_dir', 'screenshots')
        return project_root / screenshot_dir

    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()

    @property
    def current_url(self) -> str:
        """Get the current URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Get the page title."""
        return self.driver.title
