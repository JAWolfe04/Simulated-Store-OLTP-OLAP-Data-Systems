import pytest

from bs4 import BeautifulSoup

from src.product.product_utilities import product_utility
import src.product.constants as constant

@pytest.mark.retrieve_category_links
class Test_Retrieve_Category_Links:
    category_links = [
        "https://www.walmart.com/cp/kitchen-dining/623679",
        "https://www.walmart.com/cp/furniture/103150",
        "https://www.walmart.com/cp/bedding/539103",
        "https://www.walmart.com/cp/appliances/90548",
        "https://www.walmart.com/cp/decor/133012",
        "https://www.walmart.com/cp/bath-accessories/539095",
        "https://www.walmart.com/cp/storage-organization/90828",
        "https://www.walmart.com/cp/curtains-window-treatments/539105",
        "https://www.walmart.com/cp/patio-garden/5428",
        "https://www.walmart.com/cp/rugs/110892",
        "https://www.walmart.com/cp/candles-home-fragrance/2622648",
        "https://www.walmart.com/cp/wall-decor/5208936"]

    @pytest.mark.parametrize("file_name, empty_result", [
        ("tests/product/test_pages/Category_Page.html", False),
        ("tests/product/test_pages/Category_Page_Empty_Categories.html", True),
        ("tests/product/test_pages/Category_Page_Bad_Prefix.html", False)])
    def test_smoke_returns_expected_links(
            self, session, browser, file_name, empty_result):
        # First test runs an average expected category html page
        # Second test runs the same page but with categories removed
        # Third test runs the same page as the first test but with one
        # category containing nothing and three other categories with altered
        # links: one with the 'https://www.walmart.com' prefix missing,
        # another with the 'https://www.' prefix missing and another with an
        # empty link
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with open(file_name, "r", encoding="utf8") as file:
            category_html = file.read()
            page_soup = BeautifulSoup(category_html, 'html.parser')
            returned_links = utility.retrieve_category_links(page_soup.body)
            if empty_result:
                assert returned_links == []
            else:
                assert returned_links == self.category_links

    def test_raises_TypeError_with_None(self, session, browser):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(TypeError):
            utility.retrieve_category_links(None)

    @pytest.mark.parametrize("file_name", [
        ("tests/product/test_pages/Category_Page_Empty_Body.html"),
        ("tests/product/test_pages/Category_Page_No_Categories.html")])
    def test_raises_ValueError_with_missing_content(self, session,
                                                    browser, file_name):
        # First test passes a category html with an empty body
        # Second test passes a category html with the category div removed
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with open(file_name, "r", encoding="utf8") as file:
            category_html = file.read()
            page_soup = BeautifulSoup(category_html, 'html.parser')
            with pytest.raises(ValueError):
                utility.retrieve_category_links(page_soup.body)

