import pytest

from bs4 import BeautifulSoup

from src.product.product_utilities import product_utility
import src.product.constants as constant

@pytest.mark.retrieve_product_data
class Test_Retrieve_Product_Data:
    def get_body(self, file_name):
        with open(file_name, "r", encoding = "utf8") as file:
            page_html = file.read()
            page_soup = BeautifulSoup(page_html, 'html.parser')
            return page_soup.body
        
    @pytest.mark.parametrize("file_name, expected_data", [
        ("tests/product/test_pages/Product_Page.html",
         {"name": "Cuisinart Toaster Oven Broilers Air Fryer",
          "price": 199.00,
          "brand_name": "Cuisinart",
          "manufacturer_name": "Conair",
          "shelf_name": "Toaster Ovens",
          "aisle_name":"Appliances",
          "department_name": "Home and Office"}),
        ("tests/product/test_pages/Product_Page_2.html",
         {"name": ("Olay Moisture Ribbons Plus Body Wash, "
                   "Shea and Blue Lotus, 18 fl oz"),
          "price": 5.97,
          "brand_name": "Olay",
          "manufacturer_name": "Procter & Gamble",
          "shelf_name": "Body Wash & Shower Gel",
          "aisle_name": "Bath & Body",
          "department_name": "Beauty, Bath and Health"})])
    def test_smoke_returns_expected_data(
            self, session, file_name, expected_data):
        utility = product_utility(session,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        utility.department_name = expected_data.get("department_name")
        product_data = utility.retrieve_product_data(self.get_body(file_name))
        assert product_data == expected_data

    @pytest.mark.parametrize("has_body", [(True), (False)])
    def test_raises_TypeError_with_None(self, session, has_body):
        utility = product_utility(session,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(TypeError):
            if has_body:
                utility.retrieve_product_data(self.get_body(
                    "tests/product/test_pages/Product_Page.html"))
            else:
                utility.department_name = "Home and Office"
                utility.retrieve_product_data(None)
        
    @pytest.mark.parametrize("file_name", [
        ("tests/product/test_pages/Product_Page_No_Name.html"),
        ("tests/product/test_pages/Product_Page_No_Price.html"),
        ("tests/product/test_pages/Product_Page_No_Dollar.html"),
        ("tests/product/test_pages/Product_Page_No_Cents.html"),
        ("tests/product/test_pages/Product_Page_No_Breadcrumb.html"),
        ("tests/product/test_pages/Product_Page_1_Breadcrumb_Item.html"),
        ("tests/product/test_pages/Product_Page_2_Breadcrumb_Item.html"),
        ("tests/product/test_pages/Product_Page_No_Spec.html"),
        ("tests/product/test_pages/Product_Page_No_Brand_Row.html"),
        ("tests/product/test_pages/Product_Page_No_Brand_Name.html"),
        ("tests/product/test_pages/Product_Page_No_Mfr_Row.html"),
        ("tests/product/test_pages/Product_Page_No_Mfr_Name.html")])
    def test_raises_ValueError_with_Missing_Tags(self, session, file_name):
        #1st test is missing the product name tag
        #2nd test is missing the price section
        #3rd test is missing the dollar amount tag
        #4th test is missing the cent amount tag
        #5th test is missing the breadcrumb list
        #6th test the breadcrumb list contains 1 items
        #7th test the breadcrumb list contains 2 items
        #8th test is missing the spec table
        #9th test is missing the brand row
        #10th test is missing the brand value
        #11th test is missing the manufacturer row
        #12th test is missing the manufacturer value
        
        utility = product_utility(session,
                                  constant.MAX_CATALOG_SIZE,
                                  constant.MAX_PRODUCT_LIST_DEPTH)
        with pytest.raises(ValueError):
            utility.department_name = "Home and Office"
            utility.retrieve_product_data(self.get_body(file_name))
