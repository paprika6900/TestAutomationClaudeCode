"""
GroceryMate Test Suite.

This test demonstrates the framework usage with the GroceryMate application.
HTML snapshots will be automatically saved for Claude Code to analyze.
"""
import pytest
from pages.grocerymate_home_page import GroceryMateHomePage


@pytest.mark.ui
class TestGroceryMate:
    """Test suite for GroceryMate application."""

    def test_open_grocerymate_home_page(self, driver):
        """
        Test opening the GroceryMate home page.

        This test will:
        1. Create a GroceryMateHomePage object
        2. Navigate to the GroceryMate home page
        3. Automatically save HTML snapshot to page_snapshots/GroceryMateHomePage.html

        After running this test, you can ask Claude Code to:
        - Read the HTML snapshot
        - Identify elements on the page
        - Suggest accurate locators
        - Help create additional page methods

        Args:
            driver: WebDriver fixture from conftest.py
        """
        # Create page object
        home_page = GroceryMateHomePage(driver)

        # Open the GroceryMate home page
        # HTML snapshot will be automatically saved
        home_page.open_home_page()

        # Basic assertion to verify page loaded
        assert driver.current_url is not None
        print(f"\nNavigated to: {driver.current_url}")
        print("HTML snapshot saved to: page_snapshots/GroceryMateHomePage.html")
        print("You can now ask Claude Code to analyze the snapshot and suggest locators!")

    @pytest.mark.smoke
    def test_grocerymate_page_title(self, driver_with_screenshots):
        """
        Test to verify the GroceryMate page title.

        This test uses driver_with_screenshots fixture to automatically
        capture screenshots on failure.

        Args:
            driver_with_screenshots: WebDriver fixture that captures screenshots on failure
        """
        home_page = GroceryMateHomePage(driver_with_screenshots)
        home_page.open_home_page()

        # Get the page title
        page_title = home_page.title
        print(f"\nPage title: {page_title}")

        # Assert that the title is not empty
        assert page_title, "Page title should not be empty"
