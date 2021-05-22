import pytest

from src.product.product_utilities import product_utility
from src.product.constants import MAX_CATALOG_SIZE, MAX_PRODUCT_LIST_DEPTH

@pytest.mark.product_class_init
class Test_Product_Utility_Class_Initialization:
    def test_smoke_init(self, session):
        assert product_utility(session,
                               MAX_CATALOG_SIZE,
                               MAX_PRODUCT_LIST_DEPTH)

    def test_smoke_instance_attributes(self, session, cursor):
        utility = product_utility(session, 1, 1)
        assert utility.database_connection == session
        assert type(utility.database_cursor) == type(cursor)
        assert utility.max_catalog_size == 1
        assert utility.max_product_list_depth == 1

    @pytest.mark.parametrize(
        "db_connection, max_catalog_size, max_product_list_depth",
        [(None, MAX_CATALOG_SIZE, MAX_PRODUCT_LIST_DEPTH),
         (True, None, MAX_PRODUCT_LIST_DEPTH),
         (True, MAX_CATALOG_SIZE, None)])
    def test_init_with_None_raises_TypeError(self,
                                             session,
                                             db_connection,
                                             max_catalog_size,
                                             max_product_list_depth):
        # No need to test every type, simply test the type it cannot be
        with pytest.raises(TypeError):
            if db_connection:
                db_connection = session

            assert product_utility(db_connection,
                                   max_catalog_size,
                                   max_product_list_depth)
                
            

    @pytest.mark.parametrize("max_catalog_size, max_product_list_depth",
                             [(0, MAX_PRODUCT_LIST_DEPTH),
                             (MAX_CATALOG_SIZE, 0)])
    def test_non_positive_number_input_raises_ValueError(
            self, session, max_catalog_size, max_product_list_depth):
        with pytest.raises(ValueError):
            assert product_utility(session,
                                   max_catalog_size,
                                   max_product_list_depth)
