import pytest
import copy

from src.product.product_utilities import product_utility

@pytest.mark.retrieve_product_catalog
class Test_Retrieve_Product_Catalog:
    @pytest.mark.usefixtures("setup_product", "reset_shelves", "reset_products")
    def test_retrieves_and_stores_products_from_links(
        self, session, browser, sim_product_data, monkeypatch, tmp_path, cursor):
        product_links = ["https://www.walmart.com/ip/Hamilton-Beach-Sure-Crisp-Air-Fryer-Toaster-Oven-with-Easy-Reach-Door-6-Slice-Capacity-Stainless-Steel-31523/477178395"]

        def mock_retrieve_link_body(self, link):
            return ""

        def mock_retrieve_product_data(self, body):
            return sim_product_data

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_link_body)
        monkeypatch.setattr(
            product_utility, "retrieve_product_data",
            mock_retrieve_product_data)
        utility = product_utility(session, browser)
        utility.set_product_links_file_name(
            str(tmp_path / "product_links.txt"))
        utility.retrieve_product_catalog(product_links)
        cursor.execute("SELECT product_id FROM product")
        assert len(cursor.fetchall()) == 1

    @pytest.mark.parametrize("amount, is_equal, test", [
        (100, True, 1), (502, False, 2)])
    def test_product_links_rearranging_when_over_max_size(
            self, monkeypatch, tmp_path, session, browser,
            amount, is_equal, test):
        utility = product_utility(session, browser)
        utility.set_product_links_file_name(
            str(tmp_path / "product_links_{}.txt".format(test)))

        def mock_methods(self, data):
            return ""

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_methods)
        monkeypatch.setattr(
            product_utility, "retrieve_product_data", mock_methods)
        monkeypatch.setattr(
            product_utility, "store_product_data", mock_methods)
        product_1 = "https://www.walmart.com/ip/Hamilton-Beach-Sure-Crisp-Air-Fryer-Toaster-Oven-with-Easy-Reach-Door-6-Slice-Capacity-Stainless-Steel-31523/477178395"
        product_2 = "https://www.walmart.com/ip/Beautiful-6-Slice-Touchscreen-Air-Fryer-Toaster-Oven-Black-Sesame-by-Drew-Barrymore/801104369"
        product_links = []
        for x in range(0, amount):
            product_links.append(product_1)
            product_links.append(product_2)
        original_product_links = copy.deepcopy(product_links)
        utility.retrieve_product_catalog(product_links)
        if is_equal:
            assert original_product_links == product_links
        else:
            assert original_product_links != product_links

    def test_links_removed_from_Product_Links_txt(
        self, session, browser, monkeypatch, tmp_path):
        utility = product_utility(session, browser)
        product_links_file = tmp_path / "product_links.txt"
        utility.set_product_links_file_name(str(product_links_file))
        
        def mock_methods(self, data):
            return ""
        
        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_methods)
        monkeypatch.setattr(
            product_utility, "retrieve_product_data", mock_methods)
        monkeypatch.setattr(
            product_utility, "store_product_data", mock_methods)

        product_1 = "https://www.walmart.com/ip/Hamilton-Beach-Sure-Crisp-Air-Fryer-Toaster-Oven-with-Easy-Reach-Door-6-Slice-Capacity-Stainless-Steel-31523/477178395"
        product_2 = "https://www.walmart.com/ip/Beautiful-6-Slice-Touchscreen-Air-Fryer-Toaster-Oven-Black-Sesame-by-Drew-Barrymore/801104369"
        product_links = []
        for x in range(0, 20):
            product_links.append(product_1)
            product_links.append(product_2)
        product_links_file.write_text("\n".join(product_links))
        utility.retrieve_product_catalog(product_links)
        assert len(product_links_file.read_text()) == 0

    def test_with_empty_product_list(self, session, browser):
        utility = product_utility(session, browser)
        utility.retrieve_product_catalog([])

    def test_raises_TypeError_with_None(self, session, browser):
        utility = product_utility(session, browser)
        with pytest.raises(TypeError):
            utility.retrieve_product_catalog(None)
