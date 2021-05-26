import pytest

from mysql.connector import errors
from src.product.product_utilities import product_utility
import src.product.constants as constant

@pytest.mark.store_product_data
@pytest.mark.usefixtures("sim_product_data", "setup_product",
                         "reset_products", "reset_shelves")
class Test_Store_Product_Data:        
    def test_enters_data_into_db(
            self, session, browser, cursor, sim_product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        data = sim_product_data
        product_id = utility.store_product_data(data)
        query = ("SELECT product_name, price, brand_name, manufacturer_name, "
                     "shelf_name, aisle_name, department.name "
                 "FROM product AS product "
                     "JOIN shelf AS shelf "
                     "ON product.shelf_id = shelf.shelf_id "
                     "JOIN department AS department "
                     "ON shelf.department_id = department.department_id "
                 "WHERE product.product_id = %s;")
        cursor.execute(query, (product_id,))
        stored_data = cursor.fetchall()[0]
        assert stored_data[0] == data.get("name")
        assert stored_data[1] == data.get("price")
        assert stored_data[2] == data.get("brand_name")
        assert stored_data[3] == data.get("manufacturer_name")
        assert stored_data[4] == data.get("shelf_name")
        assert stored_data[5] == data.get("aisle_name")
        assert stored_data[6] == data.get("department_name")

    def test_uses_existing_shelf(
        self, session, browser, cursor, sim_product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        data = sim_product_data
        query = "SELECT department_id FROM department WHERE name = %s;"
        cursor.execute(query,(data.get("department_name"),))
        dept_id = cursor.fetchall()[0][0]
        query = ("INSERT INTO shelf(department_id, shelf_name, aisle_name)"
                 " VALUES (%s, %s, %s)")
        cursor.execute(query, (dept_id,
                               data.get("shelf_name"),
                               data.get("aisle_name")))
        session.commit()
        product_id = utility.store_product_data(data)
        cursor.execute("SELECT shelf_id FROM shelf")
        assert cursor.fetchall()[0][0] == 1

    def test_raises_IntegrityError_with_repeat_products(
        self, session, browser, sim_product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        data = sim_product_data
        utility.store_product_data(data)
        with pytest.raises(errors.IntegrityError):
            utility.store_product_data(data)

    def test_raises_TypeError_with_None(self, session, browser):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(TypeError):
            utility.store_product_data(None)

    @pytest.mark.parametrize("key", [
        ("name"), ("price"), ("brand_name"), ("manufacturer_name"),
        ("shelf_name"), ("aisle_name"), ("department_name")])
    def test_raises_TypeError_with_None_product_values(
            self, session, browser, key, sim_product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        data = sim_product_data
        data[key] = None
        with pytest.raises(TypeError):
            utility.store_product_data(data)

    @pytest.mark.parametrize("data_key, product_data", [
        ("name", " "), ("price", 0.00), ("brand_name", " "),
        ("manufacturer_name", " "), ("shelf_name", " "),
        ("shelf_name", " "), ("aisle_name", " "),
        ("department_name", " "), ("department_name", "No Department")])
    def test_raises_ValueError_with_undesired_input(
            self, session, browser, sim_product_data, data_key, product_data):
        utility = product_utility(session,
                                  browser,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        data = sim_product_data
        data[data_key] = product_data
        with pytest.raises(ValueError):
            utility.store_product_data(data)
