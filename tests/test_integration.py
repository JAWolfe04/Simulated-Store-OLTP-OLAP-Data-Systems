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
        ("https://www.walmart.com/cp/home/4044"),
        ("https://www.walmart.com/cp/bath-body/1071969")])
    def test_returns_category_body(self, browser, session, url):
        utility = product_utility(session, browser)
        link_body = utility.retrieve_link_body(url)
        category_header = link_body.find("h2", text = "Shop by Category")
        if category_header is None:
            category_header = link_body.find("h2", class_ = "header-title-5DR")
        assert category_header is not None

    @pytest.mark.parametrize("url, count", [
        ("https://www.walmart.com/browse/home/toaster-ovens/4044_90548_90546_90774_3312544",
         4),
        ("https://www.walmart.com/browse/bath-body/bar-soap/1005862_1071969_4735846",
         3)
        ])
    def test_returns_product_list_body(self, browser, session, url, count):
        utility = product_utility(session, browser)
        link_body = utility.retrieve_link_body(url)
        product_list = link_body.find("div",{"class":"search-product-result"})
        assert product_list is not None
        

    @pytest.mark.usefixtures("setup_departments")
    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/ip/Cuisinart-Toaster-Oven-Broilers-Air-Fryer/918908248?wpa_bd=&wpa_pg_seller_id=F55CDC31AB754BB68FE0B39041159D63&wpa_ref_id=wpaqs:40esHkIw5wemZ_brKHrfbg_s-VtEREr1YkwETgaLxcpIYPgQAsp6jmUmkwzZFwGZ9YYJoTUwhNTE3zkULQJUA-rXP11I4yVWE2K4n_1Bj7jrP2u4f2IHpFqKpTV7S9Bv3aFZCMVRxXNGYPCn89XFvf0PXX-NyeepYdxyKh4av-GAOqYiHyUzHCSOiftW_9nClNjY_3WoYkVJIUxhnI3EXQ&wpa_tag=&wpa_aux_info=&wpa_pos=2&wpa_plmt=1145x1145_T-C-IG_TI_1-6_HL-INGRID-GRID-NY&wpa_aduid=8dde032f-b5f2-4db7-ba85-f3a1ffc2577e&wpa_pg=browse&wpa_pg_id=4044_90548_90546_90774_3312544&wpa_st=__searchterms__&wpa_tax=4044_90548_90546_90774_3312544&wpa_bucket=__bkt__"),
        ("https://www.walmart.com/ip/BLACK-DECKER-Crisp-N-Bake-Air-Fry-4-Slice-Toaster-Oven-TO1787SS/354341819"),
        ("https://www.walmart.com/ip/Olay-Moisture-Ribbons-Plus-Body-Wash-Shea-and-Blue-Lotus-18-fl-oz/724204321")
        ])
    def test_returns_product_data_body(self, browser, session, url):
        utility = product_utility(session, browser)
        # The department name is not relevant
        utility.set_current_department_name("Food")
        link_body = utility.retrieve_link_body(url, True)
        product_name = link_body.select_one(
            "h1.prod-ProductTitle.prod-productTitle-buyBox.font-bold")
        assert product_name is not None

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/ip/Gluten-Free-Cinnamon-Buns-Mini-Glazed-Rolls-Breakfast-Pastry-Rugelach-Pastries-Croissants-Dairy-Nut-Soy-Kosher-7-oz-Katz/169182769"),
        ("https://www.walmart.com/ip/Maybelline-Color-Sensational-Shine-Compulsion-Lipstick-Makeup-Taupe-Seduction-0-1-oz/607432038")])
    def test_walmart_product_data_returns_data(self, session, url, browser):
        utility = product_utility(session, browser)
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

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/browse/food/baking-ingredients/976759_976780_9959366?cat_id=976759_976780_9959366_5053287"),
        ("https://www.walmart.com/browse/health/allergy-and-sinus/976760_3771182")
         ])
    def test_walmart_product_list_returns_links(self, session, url, browser):
        utility = product_utility(session, browser)
        browser.get(url)
        time.sleep(3)
        products_html = browser.page_source
        soupPage = BeautifulSoup(products_html, 'html.parser')
        returned_links = set()
        utility.retrieve_bestseller_links(soupPage.body, returned_links)
        assert len(returned_links) > 0

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/cp/bath-body/1071969"),
        ("https://www.walmart.com/cp/furniture/103150"),
        ("https://www.walmart.com/cp/home/4044")])
    def test_walmart_categories_returns_links(self, session, url, browser):
        utility = product_utility(session, browser)
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
