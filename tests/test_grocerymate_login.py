"""
GroceryMate Login Functional Tests.

This suite contains functional tests for the GroceryMate authentication/login feature.
"""
import pytest
import time
from pages.grocerymate_login_page import GroceryMateLoginPage
from framework.config_manager import config


@pytest.mark.functional
@pytest.mark.ui
class TestGroceryMateLogin:
    """Functional tests for GroceryMate login functionality."""

    @pytest.mark.smoke
    def test_login_with_valid_credentials(self, driver):
        """
        Test login with valid credentials from config.

        This test:
        1. Navigates to the auth page
        2. Enters email and password from config.yaml
        3. Clicks Sign In button
        4. Verifies successful login (URL change away from /auth)

        Credentials used:
        - Username: user@user.com
        - Password: user123
        """
        login_page = GroceryMateLoginPage(driver)
        login_page.navigate_to_login()

        # Verify we're on the login page
        assert login_page.is_on_login_page(), "Should be on the login page"

        # Perform login with configured credentials
        login_page.login_with_config_credentials()

        # Wait a moment for login to process
        time.sleep(2)

        # Verify we've navigated away from auth page (successful login)
        current_url = driver.current_url
        print(f"\n✓ Login attempted, current URL: {current_url}")

        # After successful login, we should no longer be on /auth
        assert 'auth' not in current_url.lower(), "Should have navigated away from auth page after login"
        print("✓ Successfully logged in and redirected")

    def test_login_page_elements_present(self, driver):
        """
        Test that all login page elements are present.

        Verifies:
        - Email input field
        - Password input field
        - Sign In button
        - Create account link
        - Home link
        - Logo and header title
        """
        login_page = GroceryMateLoginPage(driver)
        login_page.navigate_to_login()

        # Verify form elements
        assert login_page.find_element(login_page.EMAIL_INPUT), "Email input should be present"
        assert login_page.find_element(login_page.PASSWORD_INPUT), "Password input should be present"
        assert login_page.find_element(login_page.SIGN_IN_BUTTON), "Sign In button should be present"

        # Verify links
        assert login_page.find_element(login_page.CREATE_ACCOUNT_LINK), "Create account link should be present"
        assert login_page.find_element(login_page.HOME_LINK), "Home link should be present"

        # Verify header
        assert login_page.find_element(login_page.LOGO), "Logo should be present"
        assert login_page.find_element(login_page.HEADER_TITLE), "Header title should be present"

        print("\n✓ All login page elements are present")

    def test_login_page_header_title(self, driver):
        """
        Test that the login page displays the correct header title.

        Verifies the header title text is "We are MarketMate"
        """
        login_page = GroceryMateLoginPage(driver)
        login_page.navigate_to_login()

        header_title = login_page.get_header_title()
        assert header_title == "We are MarketMate", f"Expected 'We are MarketMate', got '{header_title}'"
        print(f"\n✓ Header title correct: {header_title}")

    def test_navigate_to_login_from_home(self, driver):
        """
        Test navigating to login page from home page via user account icon.

        This test:
        1. Opens home page
        2. Clicks user account icon
        3. Verifies navigation to auth page
        """
        from pages.grocerymate_home_page import GroceryMateHomePage

        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        # Click user account icon
        home_page.click_user_account_icon()

        # Wait for navigation
        time.sleep(2)

        # Verify we navigated to auth page
        assert 'auth' in driver.current_url.lower(), "Should navigate to auth page when clicking user account icon"
        print(f"\n✓ Navigated to login from home page: {driver.current_url}")
