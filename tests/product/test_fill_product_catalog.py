import pytest

from src.product.product_utilities import product_utility

@pytest.mark.usefixtures("setup_departments")
@pytest.mark.fill_product_catalog
class Test_Fill_Product_Catalog:
    dept_links = {
        "https://www.walmart.com/cp/home/4044": "Home and Office",
        "https://www.walmart.com/cp/office/1229749": "Home and Office",
        "https://www.walmart.com/cp/beauty/1085666": "Beauty, Bath and Health",
        "https://www.walmart.com/cp/health/976760": "Beauty, Bath and Health",
        "https://www.walmart.com/cp/food/976759": "Food",
        "https://www.walmart.com/cp/bath-body/1071969":"Beauty, Bath and Health"
        }
    
    def get_utility(self, session, browser, tmp_path):
        utility = product_utility(session, browser)
        utility.set_product_links_file_name(
            str(tmp_path / "test_Product_Links.txt"))
        utility.set_previous_links_file_name(
            str(tmp_path / "test_Previous_Links.txt"))
        return utility
    
    def test_smoke_reads_Product_Links_file_correctly(
            self, session, browser, monkeypatch, tmp_path, capsys):
        
        def mock_retrieve_product_links(self, link, previous_links,
                                        prev_product_lists, product_links):
            return
        def mock_retrieve_product_catalog(self, product_links):
            print(sorted(product_links))

        monkeypatch.setattr(product_utility,
                            "retrieve_product_links",
                            mock_retrieve_product_links)
        monkeypatch.setattr(product_utility,
                            "retrieve_product_catalog",
                            mock_retrieve_product_catalog)
        
        utility = product_utility(session, browser)
        prod_links_file = tmp_path / "test_Product_Links.txt"
        prod_links = {"test_1.com", "test_2.com", "test_3.com", "test_4.com"}
        content = ""
        for link in prod_links: content += link + "\n"
        prod_links_file.write_text(content)
        
        utility.set_product_links_file_name(str(prod_links_file))
        utility.set_previous_links_file_name(
            str(tmp_path / "test_Previous_Links.txt"))
        utility.fill_product_catalog({"test.com": "Food"})
        assert capsys.readouterr().out == str(sorted(prod_links)) + "\n"

    def test_smoke_read_Previous_Links_file_correctly(
            self, session, browser, monkeypatch, tmp_path, capsys):
        def mock_retrieve_product_links(self, link, previous_links,
                                        prev_product_lists, product_links):
            print(sorted(prev_product_lists))
            
        def mock_retrieve_product_catalog(self, product_links):
            return

        monkeypatch.setattr(product_utility,
                            "retrieve_product_links",
                            mock_retrieve_product_links)
        monkeypatch.setattr(product_utility,
                            "retrieve_product_catalog",
                            mock_retrieve_product_catalog)

        utility = product_utility(session, browser)
        prev_links_file = tmp_path / "test_Previous_Links.txt"
        prev_links = {"test_1.com", "test_2.com", "test_3.com", "test_4.com"}
        content = ""
        for link in prev_links: content += link + "\n"
        prev_links_file.write_text(content)

        utility.set_previous_links_file_name(str(prev_links_file))
        utility.set_product_links_file_name(
            str(tmp_path / "test_Product_Links.txt"))
        utility.fill_product_catalog({"test.com": "Food"})
        assert capsys.readouterr().out == str(sorted(prev_links)) + "\n"

    def test_smoke_cycles_through_departments(
            self, session, browser, monkeypatch, tmp_path, capsys):

        def mock_retrieve_product_links(self, link, previous_links,
                                        prev_product_lists, product_links):
            print(self.get_current_department_name())

        def mock_retrieve_product_catalog(self, product_links):
            return

        monkeypatch.setattr(product_utility,
                            "retrieve_product_links",
                            mock_retrieve_product_links)
        monkeypatch.setattr(product_utility,
                            "retrieve_product_catalog",
                            mock_retrieve_product_catalog)
        
        utility = self.get_utility(session, browser, tmp_path)
        utility.fill_product_catalog(self.dept_links)
        assert capsys.readouterr().out == "\n".join(
            list(self.dept_links.values())) + "\n"

    def test_smoke_sets_appropriate_department_name(
            self, session, browser, monkeypatch, tmp_path):
        
        def mock_retrieve_product_links(self, link, previous_links,
                                        prev_product_lists, product_links):
            return

        def mock_retrieve_product_catalog(self, product_links):
            return

        monkeypatch.setattr(product_utility,
                            "retrieve_product_links",
                            mock_retrieve_product_links)
        monkeypatch.setattr(product_utility,
                            "retrieve_product_catalog",
                            mock_retrieve_product_catalog)
        
        utility = self.get_utility(session, browser, tmp_path)
        test_name = "Food"
        utility.fill_product_catalog({test_name: test_name})
        assert utility.get_current_department_name() == test_name

    def test_smoke_calls_retrieve_product_catalog_once(
            self, session, browser, monkeypatch, tmp_path, capsys):

        def mock_retrieve_product_links(self, link, previous_links,
                                        prev_product_lists, product_links):
            return

        def mock_retrieve_product_catalog(self, product_links):
            print("Test")

        monkeypatch.setattr(product_utility,
                            "retrieve_product_links",
                            mock_retrieve_product_links)
        monkeypatch.setattr(product_utility,
                            "retrieve_product_catalog",
                            mock_retrieve_product_catalog)
        
        utility = self.get_utility(session, browser, tmp_path)
        utility.fill_product_catalog({"Test.com": "Food"})
        assert capsys.readouterr().out == "Test\n"

    def test_raises_TypeError_with_None_input(
            self, session, browser, monkeypatch, tmp_path):
        utility = self.get_utility(session, browser, tmp_path)
        with pytest.raises(TypeError):
            utility.fill_product_catalog(None)
