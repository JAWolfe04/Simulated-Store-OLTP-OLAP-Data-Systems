import pytest
import requests
import time

from bs4 import BeautifulSoup

from src.product.product_utilities import product_utility
from src.employee.constants import RAND_USER_URL
from tests.employee.constants import MOCK_JSON

@pytest.mark.integration_tests
class Test_Integration:
    def test_randomuser_api(self):
        # Tests if the API's response json mirrors the mock json used in tests
        response = requests.get(RAND_USER_URL)
        response_keys = response.json().get("results")[0].keys()
        mock_keys = MOCK_JSON.get("results")[0].keys()
        assert response_keys == mock_keys

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/ip/Gluten-Free-Cinnamon-Buns-Mini-Glazed-Rolls-Breakfast-Pastry-Rugelach-Pastries-Croissants-Dairy-Nut-Soy-Kosher-7-oz-Katz/169182769"),
        ("https://www.walmart.com/ip/Maybelline-Color-Sensational-Shine-Compulsion-Lipstick-Makeup-Taupe-Seduction-0-1-oz/607432038")])
    def test_walmart_product_data_returns_data(self, session, url, browser):
        utility = product_utility(session,
                                  browser,
                                  product_constant.MAX_CATALOG_SIZE,
                                  product_constant.MAX_PRODUCT_LIST_DEPTH)
        utility.department_name = "Food"
        browser.get(url)
        time.sleep(3)
        element = browser.find_elements_by_xpath(
            "//*[contains(text(), 'Specifications')]")
        element[0].click()
        time.sleep(2)
        nav = browser.find_element_by_class_name('persistent-subnav-list')
        new_element = nav.find_elements_by_xpath(
            "//*[contains(text(), 'Specifications')]")
        new_element[0].click()
        products_html = browser.page_source
        soupPage = BeautifulSoup(products_html, 'html.parser')
        product_data = utility.retrieve_product_data(soupPage.body)
        assert len(product_data["name"]) > 0
        assert product_data["price"] > 0.00
        assert len(product_data["brand_name"]) > 0
        assert len(product_data["manufacturer_name"]) > 0
        assert len(product_data["shelf_name"]) > 0
        assert len(product_data["aisle_name"]) > 0
        assert len(product_data["department_name"]) > 0

    @pytest.mark.parametrize("url, count", [
        ("https://www.walmart.com/browse/food/baking-ingredients/976759_976780_9959366?cat_id=976759_976780_9959366_5053287",
         4),
        ("https://www.walmart.com/browse/health/allergy-and-sinus/976760_3771182",
         8),
        ("https://www.walmart.com/browse/office-supplies/notebooks-pads/1229749_4796182",
         1)])
    def test_walmart_product_list_returns_links(self, session,
                                                url, count, browser):
        utility = product_utility(session,
                                  browser,
                                  product_constant.MAX_CATALOG_SIZE,
                                  product_constant.MAX_PRODUCT_LIST_DEPTH)
        browser.get(url)
        time.sleep(3)
        products_html = browser.page_source
        soupPage = BeautifulSoup(products_html, 'html.parser')
        returned_links = set()
        utility.retrieve_bestseller_links(soupPage.body, returned_links)
        assert len(returned_links) == count

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/cp/bath-body/1071969"),
        ("https://www.walmart.com/cp/furniture/103150"),
        ("https://www.walmart.com/cp/home/4044")])
    def test_walmart_categories_returns_links(self, session, url, browser):
        utility = product_utility(session,
                                  browser,
                                  product_constant.MAX_CATALOG_SIZE,
                                  product_constant.MAX_PRODUCT_LIST_DEPTH)
        browser.get(url)
        time.sleep(3)
        category_html = browser.page_source
        soupPage = BeautifulSoup(category_html, 'html.parser')
        
        returned_links = utility.retrieve_category_links(soupPage.body)
        assert len(returned_links) > 0

    def test_dev_database_connection(self, dev_session):
        assert dev_session.is_connected()

    def get_queries(self, dev_cursor, cursor, table_query):
        # Runs a query and returns lists of the first item of each
        # row of the resulting query for the dev and test databases
        dev_cursor.execute(table_query)
        dev_col_names = [col[0] for col in dev_cursor.fetchall()]
        cursor.execute(table_query)
        test_col_names = [col[0] for col in cursor.fetchall()]
        return (dev_col_names, test_col_names)

    @pytest.mark.parametrize("cols, table", [
        ("name", "department"), ("title", "job_position")])
    @pytest.mark.usefixtures("setup_departments", "setup_jobs")
    def test_positions(self, dev_cursor, cursor, cols, table):
        dev_jobs, test_jobs = self.get_queries(
            dev_cursor, cursor, "SELECT {} FROM {}".format(cols, table))
        assert dev_jobs == test_jobs

    @pytest.mark.usefixtures("setup_locations")
    def test_locations(self, dev_cursor, cursor):
        dev_locations, test_locations = self.get_queries(
            dev_cursor, cursor, "SELECT location_id FROM location")
        assert len(dev_locations) == len(test_locations)

    @pytest.mark.parametrize("table", [
        ("shelf"), ("employee"), ("location"), ("job_position"),
        ("department"), ("product")])
    @pytest.mark.usefixtures(
        "setup_departments", "setup_locations", "setup_jobs",
        "setup_employees", "setup_shelf", "setup_product")
    def test_tables(self, dev_cursor, cursor, table):
        dev_col_names, test_col_names = self.get_queries(
            dev_cursor, cursor, "DESCRIBE {}".format(table))
        assert test_col_names == dev_col_names
