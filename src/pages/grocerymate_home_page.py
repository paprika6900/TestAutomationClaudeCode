"""
GroceryMate Home Page Object.

This page object contains locators and methods for interacting with the
GroceryMate home page. HTML snapshots are automatically saved for analysis.
"""
from selenium.webdriver.common.by import By
from framework.base_page import BasePage


class GroceryMateHomePage(BasePage):
    """
    Page Object for GroceryMate home page.

    Contains locators for all major interactive elements including navigation,
    search, user account icons, and call-to-action buttons.
    """

    # Header - Search Section
    SEARCH_INPUT = (By.CSS_SELECTOR, "input[type='text'][placeholder='Search Products']")
    SEARCH_ICON = (By.CSS_SELECTOR, ".search-cont .icon")

    # Header - Contact Info
    CONTACT_PHONE = (By.CSS_SELECTOR, ".contact span")

    # Header - User Icons
    USER_ACCOUNT_ICON = (By.CSS_SELECTOR, ".social-icon-cont .headerIcon:nth-child(1) svg")
    FAVORITES_ICON = (By.CSS_SELECTOR, ".social-icon-cont .headerIcon:nth-child(2) svg")
    SHOPPING_CART_ICON = (By.CSS_SELECTOR, ".social-icon-cont .headerIcon:nth-child(3) svg")

    # Navigation Menu
    NAV_HOME_LINK = (By.CSS_SELECTOR, ".anim-nav a[href='/']")
    NAV_SHOP_LINK = (By.CSS_SELECTOR, ".anim-nav a[href='/store']")
    NAV_FAVORITES_LINK = (By.CSS_SELECTOR, ".anim-nav a[href='/store/favs']")
    NAV_CONTACT_LINK = (By.CSS_SELECTOR, ".anim-nav a[href='#!']")

    # Main Banner - Delicious Salad Section
    SALAD_SHOP_NOW_BUTTON = (By.CSS_SELECTOR, ".content-sec-one .shop-now-btn button")

    # Secondary Sections
    VEGETABLES_SHOP_NOW_BUTTON = (By.CSS_SELECTOR, ".content-section-two .shop-now-btn button")
    WEEK_FRENZY_SHOP_NOW_BUTTON = (By.CSS_SELECTOR, ".content-section-three .shop-now-btn button")

    # Logo
    LOGO_IMAGE = (By.CSS_SELECTOR, ".logo-search-cont img[alt='Logo']")

    def __init__(self, driver):
        """
        Initialize the GroceryMate Home Page.

        Args:
            driver: WebDriver instance
        """
        super().__init__(driver)

    def open_home_page(self):
        """
        Open the GroceryMate home page using the base_url from config.

        The HTML snapshot will be automatically saved after the page loads.
        """
        self.open()

    # Search Methods
    def search_for_product(self, product_name):
        """
        Search for a product by entering text in the search box.

        Args:
            product_name: Name of the product to search for
        """
        self.enter_text(self.SEARCH_INPUT, product_name)
        self.click(self.SEARCH_ICON)

    def enter_search_text(self, text):
        """
        Enter text in the search input field without submitting.

        Args:
            text: Text to enter in search box
        """
        self.enter_text(self.SEARCH_INPUT, text)

    # Navigation Methods
    def click_home_nav(self):
        """Navigate to Home page."""
        self.click(self.NAV_HOME_LINK)

    def click_shop_nav(self):
        """Navigate to Shop page."""
        self.click(self.NAV_SHOP_LINK)

    def click_favorites_nav(self):
        """Navigate to Favorites page."""
        self.click(self.NAV_FAVORITES_LINK)

    def click_contact_nav(self):
        """Navigate to Contact page."""
        self.click(self.NAV_CONTACT_LINK)

    # Header Icon Methods
    def click_user_account_icon(self):
        """Click the user account icon."""
        self.click(self.USER_ACCOUNT_ICON)

    def click_favorites_icon(self):
        """Click the favorites (heart) icon in header."""
        self.click(self.FAVORITES_ICON)

    def click_shopping_cart_icon(self):
        """Click the shopping cart icon."""
        self.click(self.SHOPPING_CART_ICON)

    # Shop Now Button Methods
    def click_salad_shop_now(self):
        """Click the Shop Now button in the main Delicious Salad banner."""
        self.click(self.SALAD_SHOP_NOW_BUTTON)

    def click_vegetables_shop_now(self):
        """Click the Shop Now button in the Fresh Vegetables section."""
        self.click(self.VEGETABLES_SHOP_NOW_BUTTON)

    def click_week_frenzy_shop_now(self):
        """Click the Shop Now button in the Week Frenzy section."""
        self.click(self.WEEK_FRENZY_SHOP_NOW_BUTTON)

    # Info Getter Methods
    def get_contact_phone(self):
        """
        Get the contact phone number displayed in header.

        Returns:
            Contact phone number as string
        """
        return self.get_text(self.CONTACT_PHONE)
