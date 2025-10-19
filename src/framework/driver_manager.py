"""
WebDriver manager for creating and configuring browser instances.
"""
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from framework.config_manager import config

logger = logging.getLogger(__name__)


class DriverManager:
    """Manages WebDriver creation and configuration."""

    @staticmethod
    def get_driver():
        """
        Create and configure a WebDriver instance based on config settings.

        Returns:
            WebDriver instance configured according to config.yaml

        Raises:
            ValueError: If browser name in config is not supported
        """
        browser_name = config.get('browser.name', 'chrome').lower()
        logger.info(f"Creating WebDriver for browser: {browser_name}")

        try:
            if browser_name == 'chrome':
                driver = DriverManager._create_chrome_driver()
            elif browser_name == 'firefox':
                driver = DriverManager._create_firefox_driver()
            else:
                error_msg = f"Unsupported browser: {browser_name}. Supported browsers: chrome, firefox"
                logger.error(error_msg)
                raise ValueError(error_msg)

            logger.info(f"Successfully created {browser_name} WebDriver")
            return driver

        except Exception as e:
            logger.error(f"Failed to create WebDriver for {browser_name}: {e}", exc_info=True)
            raise

    @staticmethod
    def _create_chrome_driver():
        """
        Create and configure a Chrome WebDriver instance.

        Uses webdriver-manager to automatically download and manage ChromeDriver.
        Works cross-platform (Windows, Linux, macOS).
        """
        headless = config.get('browser.headless', False)
        window_size = config.get('browser.window_size', '1920x1080')

        logger.debug(f"Configuring Chrome driver: headless={headless}, window_size={window_size}")

        options = ChromeOptions()

        # Set headless mode
        if headless:
            options.add_argument('--headless=new')

        # Set window size
        options.add_argument(f'--window-size={window_size}')

        # Common Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

        # Use webdriver-manager to automatically handle driver download/setup
        logger.debug("Installing/updating ChromeDriver via webdriver-manager")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)

        # Set timeouts
        DriverManager._set_timeouts(driver)

        logger.debug("Chrome driver created successfully")
        return driver

    @staticmethod
    def _create_firefox_driver():
        """
        Create and configure a Firefox WebDriver instance.

        Uses webdriver-manager to automatically download and manage GeckoDriver.
        Works cross-platform (Windows, Linux, macOS).
        """
        options = FirefoxOptions()

        # Set headless mode
        if config.get('browser.headless', False):
            options.add_argument('--headless')

        # Set window size
        window_size = config.get('browser.window_size', '1920x1080')
        width, height = window_size.split('x')
        options.set_preference('browser.window.width', int(width))
        options.set_preference('browser.window.height', int(height))

        # Use webdriver-manager to automatically handle driver download/setup
        logger.debug("Installing/updating GeckoDriver via webdriver-manager")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)

        # Set timeouts
        DriverManager._set_timeouts(driver)

        logger.debug("Firefox driver created successfully")
        return driver

    @staticmethod
    def _set_timeouts(driver):
        """
        Set timeouts for the WebDriver instance.

        Args:
            driver: WebDriver instance
        """
        implicit_wait = config.get('browser.implicit_wait', 10)
        page_load_timeout = config.get('browser.page_load_timeout', 30)

        driver.implicitly_wait(implicit_wait)
        driver.set_page_load_timeout(page_load_timeout)

        logger.debug(f"Set timeouts: implicit_wait={implicit_wait}s, page_load_timeout={page_load_timeout}s")

    @staticmethod
    def quit_driver(driver):
        """
        Safely quit the WebDriver instance.

        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                logger.info("Quitting WebDriver")
                driver.quit()
                logger.debug("WebDriver quit successfully")
            except Exception as e:
                logger.error(f"Error quitting driver: {e}", exc_info=True)
