import pytest

from bs4 import BeautifulSoup

from src.product.product_utilities import product_utility
import src.product.constants as constant

@pytest.mark.retrieve_bestseller_links
class Test_Retrieve_Bestseller_Links:
    best_seller_links = {
        "https://www.walmart.com/ip/Cuisinart-Toaster-Oven-Broilers-Air-Fryer/918908248?wpa_bd=&wpa_pg_seller_id=F55CDC31AB754BB68FE0B39041159D63&wpa_ref_id=wpaqs:40esHkIw5wemZ_brKHrfbg_s-VtEREr1YkwETgaLxcpIYPgQAsp6jmUmkwzZFwGZ9YYJoTUwhNTE3zkULQJUA-rXP11I4yVWE2K4n_1Bj7jrP2u4f2IHpFqKpTV7S9Bv3aFZCMVRxXNGYPCn89XFvf0PXX-NyeepYdxyKh4av-Gh2s6NBVKzbPImvj_6G7jelNjY_3WoYkVJIUxhnI3EXQ&wpa_tag=&wpa_aux_info=&wpa_pos=2&wpa_plmt=1145x1145_T-C-IG_TI_1-6_HL-INGRID-GRID-NY&wpa_aduid=3f9b816d-9a1a-4128-b4bf-8307215bafee&wpa_pg=browse&wpa_pg_id=4044_90548_90546_90774_3312544&wpa_st=Toaster%2BOvens&wpa_tax=4044_90548_90546_90774_3312544&wpa_bucket=__bkt__",
        "https://www.walmart.com/ip/Mainstays-4-Slice-Black-Toaster-Oven-with-Dishwasher-Safe-Rack-Pan-3-Piece/110482692",
        "https://www.walmart.com/ip/BLACK-DECKER-Crisp-N-Bake-Air-Fry-4-Slice-Toaster-Oven-TO1787SS/354341819",
        "https://www.walmart.com/ip/Hamilton-Beach-XL-Convection-Oven-with-Rotisserie/120169727"
            }
    
    def get_body(self, file_name):
        with open(file_name, "r", encoding = "utf8") as file:
            page_html = file.read()
            page_soup = BeautifulSoup(page_html, 'html.parser')
            return page_soup.body
        
    @pytest.mark.parametrize("file_name, has_bestsellers", [
        ("tests/product/test_pages/Product_List_Page.html", True),
        ("tests/product/test_pages/Product_List_No_Bestsellers.html", False)])
    def test_smoke_returns_expected_links(
        self, session, browser, file_name, has_bestsellers):
        # First test runs a normal product list html body with bestsellers
        # Second test runs a normal product list html body without bestsellers
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        product_links = set()
        utility.retrieve_bestseller_links(self.get_body(file_name),
                                          product_links)
        expected_links = set()
        if has_bestsellers:
            expected_links = self.best_seller_links
            assert len(product_links) == len(expected_links)
        assert product_links == expected_links

    def test_smoke_previously_recorded_links_not_duplicated(self, session,
                                                            browser):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        product_links = {"https://www.walmart.com/ip/Hamilton-Beach-XL-Convection-Oven-with-Rotisserie/120169727"}
        file_name = "tests/product/test_pages/Product_List_Page.html"
        utility.retrieve_bestseller_links(self.get_body(file_name),
                                          product_links)
        assert len(product_links) > 0
        assert product_links == self.best_seller_links

    @pytest.mark.parametrize("has_body, product_list", [
        (False, set()),
        (True, None)])
    def test_raises_TypeError_with_None(self, session, browser,
                                        has_body, product_list):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(TypeError):
            if has_body:
                file_name = "tests/product/test_pages/Product_List_Page.html"
                utility.retrieve_bestseller_links(self.get_body(file_name),
                                                  product_list)
            else:
                utility.retrieve_bestseller_links(None, product_list)

    @pytest.mark.parametrize("file_name", [
        ("tests/product/test_pages/Product_List_Page_Empty_Body.html"),
        ("tests/product/test_pages/Product_List_Page_No_Links.html"),
        ("tests/product/test_pages/Category_Page.html")])
    def test_raises_ValueError_with_bad_content(self, session,
                                                browser, file_name):
        # First test passes an empty product list html body
        # Second test pass a product list html with items with no link
        # Third test passes a page that does not have the required html
        # elements
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(ValueError):
            utility.retrieve_bestseller_links(self.get_body(file_name), set())
