"""
HTML Snapshot Capture Tests.

This test suite is dedicated to capturing HTML snapshots of pages for Claude Code
to analyze. These tests navigate to pages and save HTML without performing
functional testing.

Run these tests when:
- Adding a new page to test
- The UI has changed and you need updated HTML
- Building new page objects with Claude Code assistance
"""
import pytest
from pages.grocerymate_home_page import GroceryMateHomePage
from pages.grocerymate_login_page import GroceryMateLoginPage


@pytest.mark.html_capture
class TestHTMLSnapshots:
    """
    Test suite for capturing HTML snapshots.

    These tests are NOT functional tests - they simply navigate to pages
    to trigger HTML snapshot capture for Claude Code analysis.
    """

    def test_capture_home_page_html(self, driver):
        """
        Capture HTML snapshot of the GroceryMate home page.

        After running this test:
        - HTML saved to: page_snapshots/GroceryMateHomePage.html
        - Historical versions: page_snapshots/history/GroceryMateHomePage_*.html (keeps 2)
        - Ask Claude Code to analyze the HTML and update page object
        """
        home_page = GroceryMateHomePage(driver)
        home_page.open_home_page()

        # Manually save HTML snapshot with 2-version history
        home_page.save_html_snapshot(keep_history=2)

        # Basic verification that page loaded
        assert driver.current_url is not None
        print(f"\n✓ Home page HTML captured: {driver.current_url}")
        print("  Current snapshot: page_snapshots/GroceryMateHomePage.html")
        print("  History (keeps 2): page_snapshots/history/")

    def test_capture_login_page_html(self, driver):
        """
        Capture HTML snapshot of the GroceryMate authentication page.

        After running this test:
        - HTML saved to: page_snapshots/GroceryMateLoginPage.html
        - Historical versions: page_snapshots/history/GroceryMateLoginPage_*.html (keeps 2)
        - Ask Claude Code to analyze and build login page object with form locators
        """
        login_page = GroceryMateLoginPage(driver)
        login_page.navigate_to_login()

        # Manually save HTML snapshot with 2-version history
        login_page.save_html_snapshot(keep_history=2)

        # Basic verification that page loaded
        assert login_page.is_on_login_page()
        print(f"\n✓ Login page HTML captured: {driver.current_url}")
        print("  Current snapshot: page_snapshots/GroceryMateLoginPage.html")
        print("  History (keeps 2): page_snapshots/history/")

    # Add more HTML capture tests here as you explore new pages:
    # def test_capture_shop_page_html(self, driver):
    #     """Capture HTML snapshot of the shop page."""
    #     pass

    # def test_capture_product_details_page_html(self, driver):
    #     """Capture HTML snapshot of a product details page."""
    #     pass
