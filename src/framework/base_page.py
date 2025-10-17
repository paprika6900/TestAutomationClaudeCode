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

    Automatically captures and stores HTML snapshots when pages are accessed,
    allowing Claude Code to analyze page structure and suggest accurate locators.
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

        # Automatically save HTML snapshot when page is initialized
        if config.get('selenium.save_html_snapshots', True):
            self._save_html_snapshot()

    def _save_html_snapshot(self):
        """
        Save the current page HTML to a snapshot file.
        This allows Claude Code to read the HTML and identify accurate locators.
        """
        snapshot_dir = self._get_snapshot_directory()
        os.makedirs(snapshot_dir, exist_ok=True)

        # Create filename based on page class name and timestamp
        page_name = self.__class__.__name__
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{page_name}.html"
        filepath = snapshot_dir / filename

        # Save the page source
        try:
            html_content = self.driver.page_source
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

            # Also save a timestamped version for history
            history_filename = f"{page_name}_{timestamp}.html"
            history_filepath = snapshot_dir / "history" / history_filename
            os.makedirs(history_filepath.parent, exist_ok=True)
            with open(history_filepath, 'w', encoding='utf-8') as f:
                f.write(html_content)

        except Exception as e:
            print(f"Warning: Could not save HTML snapshot: {e}")

    def _get_snapshot_directory(self) -> Path:
        """Get the directory for storing HTML snapshots."""
        project_root = Path(__file__).parent.parent.parent
        snapshot_dir = config.get('selenium.html_snapshots_dir', 'page_snapshots')
        return project_root / snapshot_dir

    def open(self, url: str = None):
        """
        Open a URL and save HTML snapshot.

        Args:
            url: URL to open. If None, uses base_url from config
        """
        if url is None:
            url = config.get('test_data.base_url')

        self.driver.get(url)

        # Save snapshot after page loads
        if config.get('selenium.save_html_snapshots', True):
            self._save_html_snapshot()

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
        """Refresh the current page and update HTML snapshot."""
        self.driver.refresh()
        if config.get('selenium.save_html_snapshots', True):
            self._save_html_snapshot()

    @property
    def current_url(self) -> str:
        """Get the current URL."""
        return self.driver.current_url

    @property
    def title(self) -> str:
        """Get the page title."""
        return self.driver.title
