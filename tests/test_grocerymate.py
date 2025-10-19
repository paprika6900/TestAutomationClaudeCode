"""
GroceryMate Functional Test Suite.

This suite contains functional tests that verify GroceryMate application behavior.
These tests use the page objects built from HTML snapshots.
"""
import pytest
from pages.grocerymate_home_page import GroceryMateHomePage


@pytest.mark.functional
@pytest.mark.ui
class TestGroceryMateHomePage:
    """Functional tests for GroceryMate home page."""

    @pytest.mark.smoke
    def test_home_page_loads(self, driver):
        """
        Test that the GroceryMate home page loads successfully.

        Verifies:
        - Page URL is correct
        - Page title is not empty
        """
        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        assert "grocerymate.masterschool.com" in driver.current_url
        assert home_page.title, "Page title should not be empty"
        print(f"\n✓ Home page loaded: {driver.current_url}")

    @pytest.mark.smoke
    def test_navigation_menu_links(self, driver):
        """
        Test that navigation menu links are present and clickable.

        Verifies all main navigation items exist.
        """
        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        # Test that we can interact with navigation elements
        # (not clicking to avoid navigation, just verifying presence)
        assert home_page.find_element(home_page.NAV_HOME_LINK)
        assert home_page.find_element(home_page.NAV_SHOP_LINK)
        assert home_page.find_element(home_page.NAV_FAVORITES_LINK)
        assert home_page.find_element(home_page.NAV_CONTACT_LINK)
        print("\n✓ All navigation menu links are present")

    def test_search_functionality_exists(self, driver):
        """
        Test that search functionality is present on the page.

        Verifies:
        - Search input field exists
        - Search icon exists
        """
        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        assert home_page.find_element(home_page.SEARCH_INPUT)
        assert home_page.find_element(home_page.SEARCH_ICON)
        print("\n✓ Search functionality is present")

    def test_header_icons_present(self, driver):
        """
        Test that all header icons are present.

        Verifies:
        - User account icon
        - Favorites icon
        - Shopping cart icon
        """
        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        assert home_page.find_element(home_page.USER_ACCOUNT_ICON)
        assert home_page.find_element(home_page.FAVORITES_ICON)
        assert home_page.find_element(home_page.SHOPPING_CART_ICON)
        print("\n✓ All header icons are present")
