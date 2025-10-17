"""
GroceryMate Login Page Object.

This page object handles the authentication page at /auth.
Built from HTML snapshot analysis.
"""
from selenium.webdriver.common.by import By
from framework.base_page import BasePage
from framework.config_manager import config


class GroceryMateLoginPage(BasePage):
    """
    Page Object for GroceryMate authentication/login page.

    The login form is located at https://grocerymate.masterschool.com/auth
    """

    # Form Elements
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email'][placeholder='Email address']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password'][placeholder='Password']")
    SIGN_IN_BUTTON = (By.CSS_SELECTOR, "button[type='submit'].submit-btn")

    # Links
    CREATE_ACCOUNT_LINK = (By.CSS_SELECTOR, "a.switch-link")
    HOME_LINK = (By.CSS_SELECTOR, "a.home-link")

    # Header Elements
    LOGO = (By.CSS_SELECTOR, ".auth-form-header img.logo")
    HEADER_TITLE = (By.CSS_SELECTOR, ".header-title")

    # Info Section
    AUTH_INFO = (By.CSS_SELECTOR, ".auth-info")

    def __init__(self, driver):
        """
        Initialize the GroceryMate Login Page.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def navigate_to_login(self):
        """
        Navigate to the authentication page.
        """
        login_url = config.get('test_data.base_url') + 'auth'
        self.driver.get(login_url)

    def is_on_login_page(self):
        """
        Check if currently on the login/auth page.

        Returns:
            True if URL contains 'auth'
        """
        return 'auth' in self.driver.current_url.lower()

    def login(self, username, password):
        """
        Perform login with the provided credentials.

        Args:
            username: Email address for login
            password: Password for login
        """
        self.enter_text(self.EMAIL_INPUT, username)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click(self.SIGN_IN_BUTTON)

    def login_with_config_credentials(self):
        """
        Perform login using credentials from config.yaml.

        Uses test_data.login.username and test_data.login.password from config.
        """
        username = config.get('test_data.login.username')
        password = config.get('test_data.login.password')
        self.login(username, password)

    def click_create_account(self):
        """Click the 'Create a new account' link."""
        self.click(self.CREATE_ACCOUNT_LINK)

    def click_go_to_home(self):
        """Click the 'Go to Home' link."""
        self.click(self.HOME_LINK)

    def get_header_title(self):
        """
        Get the header title text.

        Returns:
            Header title as string (e.g., "We are MarketMate")
        """
        return self.get_text(self.HEADER_TITLE)
