import pytest

from bs4 import BeautifulSoup

from src.product.product_utilities import product_utility

@pytest.mark.retrieve_product_links
class Test_Retrieve_Product_Links:
    def get_utility(self, session, browser, tmp_path):
        utility = product_utility(session, browser)
        utility.set_product_links_file_name(
            str(tmp_path / "test_Product_Links.txt"))
        utility.set_previous_links_file_name(
            str(tmp_path / "test_Previous_Links.txt"))
        return utility
    
    def test_smoke_page_link_added_to_previous_links(
            self, session, browser, monkeypatch, tmp_path):    
        def mock_retrieve_body(self, link):
            file_name = "tests/product/test_pages/Category_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body

        def mock_category_links(self, body):
            return []

        monkeypatch.setattr(
            product_utility, "retrieve_category_links", mock_category_links)
        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        
        previous_links = set()
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("test.com", previous_links, set(), set())
        assert previous_links == {"test.com"}

    def test_smoke_recursive_call_attempted_with_stop_criteria(
            self, session, browser, monkeypatch, tmp_path):
        def mock_retrieve_body(self, link):
            file_name = "tests/product/test_pages/Category_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body

        def mock_category_links(self, body):
            return ["test_2.com"]

        monkeypatch.setattr(
            product_utility, "retrieve_category_links", mock_category_links)
        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        
        previous_links = set()
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("test.com", previous_links, set(), set())
        assert previous_links == {"test.com", "test_2.com"}

    def test_smoke_product_list_branch_called_with_product_list_page(
            self, session, browser, tmp_path, monkeypatch):
        def mock_retrieve_body(self, link):
            file_name = "tests/product/test_pages/Product_List_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body
        
        def mock_bestsellers(self, body, product_links):
            return

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        monkeypatch.setattr(
            product_utility, "retrieve_bestseller_links", mock_bestsellers)
        
        previous_lists = set()
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("test.com", set(), previous_lists, set())
        assert previous_lists == {"test.com"}

    def test_smoke_product_list_skipped_when_in_previously_collected_products(
            self, session, browser, monkeypatch, tmp_path):        
        def mock_retrieve_body(self, link):
            file_name = "tests/product/test_pages/Product_List_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body
        
        def mock_bestsellers(self, body, product_links):
            raise AssertionError("Product list was not skipped when it had "
                                 "been already visited")

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        monkeypatch.setattr(
            product_utility, "retrieve_bestseller_links", mock_bestsellers)
        
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("test.com", set(), {"test.com"}, set())

    def test_smoke_correct_product_list_pages_called(
            self, session, browser, monkeypatch, capsys, tmp_path):
        
        def mock_bestsellers(self, body, product_links):
            return

        def mock_retrieve_body(self, url):
            print(url)
            file_name = "tests/product/test_pages/Product_List_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body

        monkeypatch.setattr(
            product_utility, "retrieve_bestseller_links", mock_bestsellers)
        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)

        url_link = "test.com"
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links(url_link, set(), set(), set())

        expected_out = url_link + "\n"
        for page in range (2, utility.get_max_product_list_depth() + 1):
            expected_out += (url_link + "&page={}\n".format(page))
        assert capsys.readouterr().out == expected_out

    def test_smoke_writing_to_Product_Links_file(
            self, session, browser, tmp_path, monkeypatch):
        def mock_retrieve_body(self, url):
            file_name = "tests/product/test_pages/Product_List_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body
        
        def mock_bestsellers(self, body, product_links):
            product_links.add("Test_product.com")

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        monkeypatch.setattr(
            product_utility, "retrieve_bestseller_links", mock_bestsellers)
        
        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("Test.com", set(), set(), set())
        file_name = utility.get_product_links_file_name()
        with open(file_name, "r", encoding="utf8") as file:
            assert file.read() == "Test_product.com"

    def test_smoke_writing_to_Previous_Links_file(
            self, session, browser, monkeypatch, tmp_path):
        def mock_retrieve_body(self, url):
            file_name = "tests/product/test_pages/Product_List_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body
        
        def mock_bestsellers(self, body, product_links):
            return

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)
        monkeypatch.setattr(
            product_utility, "retrieve_bestseller_links", mock_bestsellers)

        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("Test.com", set(), set(), set())
        file_name = utility.get_previous_links_file_name()
        with open(file_name, "r", encoding="utf8") as file:
            assert file.read() == "Test.com"

    def test_smoke_calls_retrieve_catagories(
            self, session, browser, monkeypatch, tmp_path):
        def mock_retrieve_body(self, link):
            file_name = "tests/product/test_pages/Category_Page.html"
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body

        def mock_category_links(self, body):
            raise AssertionError("retrieve_category_links called")

        monkeypatch.setattr(
            product_utility, "retrieve_category_links", mock_category_links)
        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)

        utility = self.get_utility(session, browser, tmp_path)

        with pytest.raises(AssertionError):
            utility.retrieve_product_links("Test.com", set(), set(), set())

    @pytest.mark.parametrize("file_name", [
        ("tests/product/test_pages/Product_Page.html"),
        ("tests/product/test_pages/Page_Not_Found.html")])
    def test_smoke_skips_page_with_unexpected_pages(
            self, session, browser, tmp_path, monkeypatch, file_name):
        def mock_retrieve_body(self, link):
            with open(file_name, "r", encoding="utf8") as file:
                page_soup = BeautifulSoup(file.read(), 'html.parser')
                return page_soup.body

        monkeypatch.setattr(
            product_utility, "retrieve_link_body", mock_retrieve_body)

        utility = self.get_utility(session, browser, tmp_path)
        utility.retrieve_product_links("Test.com", set(), set(), set())

    @pytest.mark.parametrize(
        "link, previous_links, prev_product_lists, product_links", [
            (None, set(), set(), set()),
            ("Test.com", None, set(), set()),
            ("Test.com", set(), None, set()),
            ("Test.com", set(), set(), None)])
    def test_raises_TypeError_when_input_is_None(
            self, session, browser, tmp_path, link, previous_links,
            prev_product_lists, product_links):
        utility = self.get_utility(session, browser, tmp_path)
        with pytest.raises(TypeError):
            utility.retrieve_product_links(
                link, previous_links, prev_product_lists, product_links)

    def test_raises_ValueError_with_undesired_input(
            self, session, browser, tmp_path):
        utility = self.get_utility(session, browser, tmp_path)
        with pytest.raises(ValueError):
            utility.retrieve_product_links(" ", set(), set(), set())
