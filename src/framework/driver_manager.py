"""
WebDriver manager for creating and configuring browser instances.
"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from framework.config_manager import config


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

        if browser_name == 'chrome':
            return DriverManager._create_chrome_driver()
        elif browser_name == 'firefox':
            return DriverManager._create_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

    @staticmethod
    def _create_chrome_driver():
        """
        Create and configure a Chrome WebDriver instance.

        Uses system-installed chromedriver. Make sure chromedriver is installed:
        sudo apt install chromium-chromedriver
        """
        options = ChromeOptions()

        # Set headless mode
        if config.get('browser.headless', False):
            options.add_argument('--headless=new')

        # Set window size
        window_size = config.get('browser.window_size', '1920x1080')
        options.add_argument(f'--window-size={window_size}')

        # Common Chrome options for stability
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)

        # Use system chromedriver with explicit path
        service = ChromeService('/usr/bin/chromedriver')
        driver = webdriver.Chrome(service=service, options=options)

        # Set timeouts
        DriverManager._set_timeouts(driver)

        return driver

    @staticmethod
    def _create_firefox_driver():
        """
        Create and configure a Firefox WebDriver instance.

        Uses system-installed geckodriver. Make sure geckodriver is installed:
        sudo apt install firefox-geckodriver
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

        # Use system geckodriver
        driver = webdriver.Firefox(options=options)

        # Set timeouts
        DriverManager._set_timeouts(driver)

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

    @staticmethod
    def quit_driver(driver):
        """
        Safely quit the WebDriver instance.

        Args:
            driver: WebDriver instance to quit
        """
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
