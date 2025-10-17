"""
Base Page Object Model class with HTML snapshot capability for Claude Code integration.
"""
import os
import time
from pathlib import Path
from datetime import datetime
from typing import Tuple, List
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from framework.config_manager import config


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
        self.wait = WebDriverWait(
            driver,
            config.get('selenium.page_load_timeout', 30)
        )

    def save_html_snapshot(self, keep_history: int = 2):
        """
        Manually save the current page HTML to a snapshot file.
        This allows Claude Code to read the HTML and identify accurate locators.

        Args:
            keep_history: Number of historical versions to keep (default: 2)
        """
        snapshot_dir = self._get_snapshot_directory()
        os.makedirs(snapshot_dir, exist_ok=True)

        # Create filename based on page class name
        page_name = self.__class__.__name__
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{page_name}.html"
        filepath = snapshot_dir / filename

        # Save the page source
        try:
            html_content = self.driver.page_source

            # Save current version
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Save timestamped version for history
            history_dir = snapshot_dir / "history"
            os.makedirs(history_dir, exist_ok=True)
            history_filename = f"{page_name}_{timestamp}.html"
            history_filepath = history_dir / history_filename
            with open(history_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Clean up old history files, keeping only the most recent ones
            self._cleanup_history(page_name, history_dir, keep_history)

        except Exception as e:
            print(f"Warning: Could not save HTML snapshot: {e}")

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
            for old_file in history_files[keep_count:]:
                old_file.unlink()

        except Exception as e:
            print(f"Warning: Could not cleanup history files: {e}")

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

        self.driver.get(url)

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
        """
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()

    def enter_text(self, locator: Tuple[By, str], text: str):
        """
        Enter text into an input field after waiting for it to be visible.

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to enter
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Get text from an element after waiting for it to be visible.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            Element text
        """
        element = self.wait.until(EC.visibility_of_element_located(locator))
        return element.text

    def is_element_visible(self, locator: Tuple[By, str], timeout: int = None) -> bool:
        """
        Check if element is visible within the given timeout.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Timeout in seconds. If None, uses default

        Returns:
            True if element is visible, False otherwise
        """
        try:
            if timeout:
                wait = WebDriverWait(self.driver, timeout)
                wait.until(EC.visibility_of_element_located(locator))
            else:
                self.wait.until(EC.visibility_of_element_located(locator))
            return True
        except:
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
        self.driver.save_screenshot(str(filepath))

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
