import pytest

from src.product.product_utilities import product_utility
import src.product.constants as constant

@pytest.mark.retrieve_link_body
class Test_Retrieve_Link_Body:

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/cp/home/4044"),
        ("https://www.walmart.com/cp/bath-body/1071969")])
    def test_returns_category_body(self, browser, session, url):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        link_body = utility.retrieve_link_body(url)
        returned_links = utility.retrieve_category_links(link_body)
        assert len(returned_links) > 0

    @pytest.mark.parametrize("url, count", [
        ("https://www.walmart.com/browse/home/toaster-ovens/4044_90548_90546_90774_3312544",
         4),
        ("https://www.walmart.com/browse/bath-body/bar-soap/1005862_1071969_4735846",
         3)
        ])
    def test_returns_product_list_body(self, browser, session, url, count):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        link_body = utility.retrieve_link_body(url)
        returned_links = set()
        utility.retrieve_bestseller_links(link_body, returned_links)
        assert len(returned_links) == count

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/ip/Cuisinart-Toaster-Oven-Broilers-Air-Fryer/918908248?wpa_bd=&wpa_pg_seller_id=F55CDC31AB754BB68FE0B39041159D63&wpa_ref_id=wpaqs:40esHkIw5wemZ_brKHrfbg_s-VtEREr1YkwETgaLxcpIYPgQAsp6jmUmkwzZFwGZ9YYJoTUwhNTE3zkULQJUA-rXP11I4yVWE2K4n_1Bj7jrP2u4f2IHpFqKpTV7S9Bv3aFZCMVRxXNGYPCn89XFvf0PXX-NyeepYdxyKh4av-GAOqYiHyUzHCSOiftW_9nClNjY_3WoYkVJIUxhnI3EXQ&wpa_tag=&wpa_aux_info=&wpa_pos=2&wpa_plmt=1145x1145_T-C-IG_TI_1-6_HL-INGRID-GRID-NY&wpa_aduid=8dde032f-b5f2-4db7-ba85-f3a1ffc2577e&wpa_pg=browse&wpa_pg_id=4044_90548_90546_90774_3312544&wpa_st=__searchterms__&wpa_tax=4044_90548_90546_90774_3312544&wpa_bucket=__bkt__"),
        ("https://www.walmart.com/ip/BLACK-DECKER-Crisp-N-Bake-Air-Fry-4-Slice-Toaster-Oven-TO1787SS/354341819"),
        ("https://www.walmart.com/ip/Olay-Moisture-Ribbons-Plus-Body-Wash-Shea-and-Blue-Lotus-18-fl-oz/724204321")
        ])
    def test_returns_product_data_body(self, browser, session, url):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        utility.department_name = "Food"
        link_body = utility.retrieve_link_body(url, True)
        product_data = utility.retrieve_product_data(link_body)
        assert len(product_data["name"]) > 0
        assert product_data["price"] > 0.00
        assert len(product_data["brand_name"]) > 0
        assert len(product_data["manufacturer_name"]) > 0
        assert len(product_data["shelf_name"]) > 0
        assert len(product_data["aisle_name"]) > 0
        assert len(product_data["department_name"]) > 0

    @pytest.mark.parametrize("url, is_product_data", [
        (None, False), ("https://www.walmart.com/cp/home/4044", None)])
    def test_raises_TypeError_with_None(self, session, browser,
                                        url, is_product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(TypeError):
            utility.retrieve_link_body(url, is_product_data)

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/browse/food/extracts-colorings/976759_976780_2881195_1092369")
        ])
    def test_raises_ValueError_with_page_not_found(self, browser, session,
                                                    url):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(ValueError):
            utility.retrieve_link_body(url)
