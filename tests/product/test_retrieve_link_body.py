import pytest

from src.product.product_utilities import product_utility

@pytest.mark.retrieve_link_body
class Test_Retrieve_Link_Body:

    @pytest.mark.parametrize("url, is_product_data", [
        (None, False), ("https://www.walmart.com/cp/home/4044", None)])
    def test_raises_TypeError_with_None(self, session, browser,
                                        url, is_product_data):
        utility = product_utility(session, browser)
        with pytest.raises(TypeError):
            utility.retrieve_link_body(url, is_product_data)

    @pytest.mark.parametrize("url", [
        ("https://www.walmart.com/browse/food/extracts-colorings/976759_976780_2881195_1092369")
        ])
    def test_raises_ValueError_with_page_not_found(self, browser, session,
                                                    url):
        with pytest.raises(ValueError):
            product_utility(session, browser).retrieve_link_body(url)
