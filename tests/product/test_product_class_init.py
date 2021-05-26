import pytest

from src.product.product_utilities import product_utility

@pytest.mark.product_class_init
class Test_Product_Utility_Class_Initialization:
    def test_smoke_init(self, session, browser):
        assert product_utility(session, browser)

    def test_smoke_instance_attributes(self, session, browser, cursor):
        utility = product_utility(session, browser)
        assert utility.database_connection == session
        assert type(utility.database_cursor) == type(cursor)
        assert type(utility.browser) == type(browser)

    @pytest.mark.parametrize( "has_db, has_browser", [
        (False, True), (True, False)])
    def test_init_with_None_raises_TypeError(
            self, session, has_db, browser, has_browser):
        # No need to test every type, simply test the type it cannot be
        with pytest.raises(TypeError):
            db_connection = None
            browser_driver = None
            
            if has_db:
                db_connection = session
            if has_browser:
                browser_driver = browser               

            assert product_utility(db_connection, browser_driver)

    def test_get_set_max_catalog_size_returns_value(self, session, browser):
        utility = product_utility(session, browser)
        utility.set_max_catalog_size(100)
        assert utility.get_max_catalog_size() == 100

    @pytest.mark.parametrize("size, error", [
        (None, TypeError), (0, ValueError)])
    def test_set_max_catalog_size_raises_Errors(
        self, session, browser, size, error):
        with pytest.raises(error):
            product_utility(session, browser).set_max_catalog_size(size)

    def test_get_set_max_product_list_depth_returns_value(
            self, session, browser):
        utility = product_utility(session, browser)
        utility.set_max_product_list_depth(1)
        assert utility.get_max_product_list_depth() == 1

    @pytest.mark.parametrize("depth, error", [
        (None, TypeError), (0, ValueError)])
    def test_set_max_product_list_depth_raises_Errors(
            self, session, browser, depth, error):
        utility = product_utility(session, browser)
        with pytest.raises(error):
            utility.set_max_product_list_depth(depth)

    @pytest.mark.usefixtures("setup_departments")
    def test_get_set_current_department_name_returns_value(
            self, session, browser):
        utility = product_utility(session, browser)
        utility.set_current_department_name("Food")
        assert utility.get_current_department_name() == "Food"

    @pytest.mark.usefixtures("setup_departments")
    @pytest.mark.parametrize("name, error", [
        (None, TypeError), (" ", ValueError),
        ("Not Department", ValueError)])
    def test_set_current_department_name_raises_Errors(
            self, session, browser, name, error):
        utility = product_utility(session, browser)
        with pytest.raises(error):
            utility.set_current_department_name(name)

    def test_get_set_product_links_file_name_returns_value(
            self, session, browser):
        utility = product_utility(session, browser)
        file_name = "test.txt"
        utility.set_product_links_file_name(file_name)
        assert utility.get_product_links_file_name() == file_name

    @pytest.mark.parametrize("file_name, error", [
        (None, TypeError), (" ", ValueError)])
    def test_set_product_links_file_name_raises_Errors(
            self, session, browser, file_name, error):
        utility = product_utility(session, browser)
        with pytest.raises(error):
            utility.set_product_links_file_name(file_name)

    def test_get_set_previous_links_file_name_returns_value(
            self, session, browser):
        utility = product_utility(session, browser)
        file_name = "test.txt"
        utility.set_previous_links_file_name(file_name)
        assert utility.get_previous_links_file_name() == file_name

    @pytest.mark.parametrize("file_name, error", [
        (None, TypeError), (" ", ValueError)])
    def test_set_previous_links_file_name_raises_Errors(
            self, session, browser, file_name, error):
        utility = product_utility(session, browser)
        with pytest.raises(error):
            utility.set_previous_links_file_name(file_name)
