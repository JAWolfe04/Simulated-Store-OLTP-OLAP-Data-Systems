""" Product Utilities

This module contains the product_utility class with various methods to interact
with product data

This module requires 'mysql.connector' to be installed as well as a running
MySQL database.
"""

import mysql.connector
from bs4 import BeautifulSoup, element

class product_utility:
    """
    A class for manipulating product data the Simulated Superstore data system

    Attributes
    ----------
    database_connection (mysql.connector.connection.MySQLConnection):
        - Connection to the working business database
    database_cursor (mysql.connector.cursor.MySQLCursor):
        - Cursor for entering data to the working business database
    max_catalog_size
        - Number indicating the maximum size of the product catalog, must
          be a number greater than 0
    max_product_list_depth
        - Number indicating the maximum number of pages to cycle through
          a product list in Walmart.com to find products, must be a number
          greater than 0

    Methods
    -------
    """
    def __init__(self, database_connection,
                 max_catalog_size,
                 max_product_list_depth):
        """
        Parameters
        ----------
        database_connection (mysql.connector.connection.MySQLConnection):
            Connection to the working business database
        database_cursor (mysql.connector.cursor.MySQLCursor): Cursor for
            entering data to the working business database
        max_catalog_size (int): Indicates the maximum size of the product
            catalog, must be greater than 0
        max_product_list_depth (int): Indicates the maximum number of pages
            to cycle through a product list in Walmart.com to find products,
            must be greater than 0
        """

        if (type(database_connection) is not
            mysql.connector.connection.MySQLConnection):
            raise TypeError("Provided connection is wrong type")
        elif type(max_catalog_size) is not int:
            raise TypeError("Provided max catalog size is not a number")
        elif type(max_product_list_depth) is not int:
            raise TypeError("Provided max product list depth is not a number")

        if max_catalog_size < 1:
            raise ValueError("Provided max catalog size cannot be less than 1")
        elif max_product_list_depth < 1:
            raise ValueError("Provided max product list depth cannot be less "
                             "than 1")
        
        self.database_connection = database_connection
        self.database_cursor = database_connection.cursor()
        self.max_catalog_size = max_catalog_size
        self.max_product_list_depth = max_product_list_depth
        self.department_name = None

    def retrieve_category_links(self, body):
        """
        Returns a list of category links found within the provided body

        Parameters
        ----------
        body (bs4.element.tag): BeautifulSoup body tag for a html Walmart.com
        page containing a list of categories to browse

        Returns
        -------
        list: List of category links
        """
        if type(body) is not element.Tag:
            raise TypeError("Provided body is not a bs4.element.Tag")

        # The most characteristic part of the category list is the
        # shop by heading, so it is probably best to start therre
        category_header = body.find("h2", text = "Shop by Category")

        # The heading can occasionally take the for of 'Shop X' category but
        # this have the following class
        if category_header is None:
            category_header = body.find("h2", class_ = "header-title-5DR")

        if category_header is None:
            raise ValueError("Provided body does not contain category list")

        # From the Shop by element, it has an ancester that has 'featured'
        # in its class name
        category_ancestor = category_header.parent
        while("featured" not in "".join(category_ancestor['class']).lower()):
            category_ancestor = category_ancestor.parent

        # The second child divider of the featured class divider contains
        # children with the links for each category
        category_section = None
        div_counter = 0
        for sibling in category_ancestor.children:
            if sibling.name == "div":
                if div_counter == 1:
                    category_section = sibling
                    break
                else:
                    div_counter += 1

        if category_section is None:
            raise ValueError("Provided body does not contain a category "
                             "section")
        
        category_links = []
        for category in category_section.children:
            try:
                category_link = category.a.get("href")
                if len(category_link) == 0:
                    continue
                elif category_link[0] == "/":
                    category_link = "https://www.walmart.com" + category_link
                elif category_link[0] == "w":
                    category_link = "https://www." + category_link
                    
                category_links.append(category_link)
            except AttributeError as e:
                if e == "'NavigableString' object has no attribute 'a'":
                    continue
                
            
        return category_links

    def retrieve_bestseller_links(self, body, product_links):
        """
        Retrieves links of products flagged as Best Sellers from the provided
        body and adds them to a set of provided product_links

        Parameters
        ----------
        body (bs4.element.tag): BeautifulSoup body tag for a html Walmart.com
        page containing a list of products to browse
        product_links (set): Set of product links
        """
        if type(body) is not element.Tag:
            raise TypeError("Provided body is not a bs4.element.Tag")
        
        product_list = body.find("div",{"class":"search-product-result"})

        if type(product_links) is not set:
            raise TypeError("Provided product_links is not a set")

        if product_list is None:
            raise ValueError("Provided body does is not a product list")

        flagged_products = product_list.find_all(
            "span", {"class": "flag-angle__content"})

        for flag in flagged_products:
            if flag.text == "Best Seller":
                flag_li_parent = flag.find_parent("li")
                if flag_li_parent is None:
                    raise ValueError("Best Seller flag does not have the "
                                     "expected parent format")
                link = flag_li_parent.a
                if (link is None or " ".join(link["class"])
                    != "search-result-productimage gridview display-block"):
                    raise ValueError("Unable to find expected link to flag")
                product_links.add(link.get("href"))
        
    def retrieve_product_data(self, body):
        """
        Retrieves product data: name, price, brand name, manufacturer name,
        shelf name, aisle name and department name from the provided body
        containing a Walmart.com product page

        Parameters
        ----------
        body (bs4.element.tag): BeautifulSoup body tag for a html Walmart.com
        page containing a list of products to browse

        Returns
        -------
        (dict): Dictionary with name, price, brand_name, manufacturer_name,
                shelf_name, aisle_name and department_name
        """
        if type(body) is not element.Tag:
            raise TypeError("Provided body is not a bs4.element.Tag")

        if type(self.department_name) is not str:
            raise TypeError("Department name is not a string or the "
                            "department name has not been set")
        
        product_name = body.select_one(
            "h1.prod-ProductTitle.prod-productTitle-buyBox.font-bold")
        if product_name is None:
            raise ValueError("Product name could not be found")

        price_section = body.select_one("div.prod-PriceHero")
        if price_section is None:
            raise ValueError("Price could not be found")
        
        dollar_amount = price_section.select_one("span.price-characteristic")
        if dollar_amount is None:
            raise ValueError("Product dollar amount could not be found")
        
        cents_amount  = price_section.select_one("span.price-mantissa")
        if cents_amount is None:
            raise ValueError("Product cent amount could not be found")
        
        price = dollar_amount.text + '.' + cents_amount.text

        breadcrumb_element = body.select_one("ol.breadcrumb-list")
        if breadcrumb_element is None:
            raise ValueError("Breadcrumb could not be found")
        
        breadcrumb_list = breadcrumb_element.contents        
        if len(breadcrumb_list) <= 2:
            raise ValueError("Too few Breadcrumbs, must be at least 3")
        
        aisle_name = breadcrumb_list[1].a.span.text
        shelf_name = None
        if len(breadcrumb_list) > 3:
            shelf_name = breadcrumb_list[-2].a.span.text
        else:
            shelf_name = breadcrumb_list[-1].a.span.text
        
        brand = None
        manufacturer = None
        spec_table = body.select_one(
            "table.product-specification-table.table-striped")
        if spec_table is None:
            raise ValueError("Specification Table could not be found")
        spec_tbody = spec_table.tbody
        spec_rows = spec_tbody.find_all('tr')
        for row in spec_rows:
            cols = row.find_all('td')
            if cols[0].text == 'Brand':
                if len(cols) == 1:
                    raise ValueError("Brand name could not be found")
                brand = cols[1].text
            elif cols[0].text == 'Manufacturer':
                if len(cols) == 1:
                    raise ValueError("Manufacturer name could not be found")
                manufacturer = cols[1].text

        if brand is None:
            raise ValueError("Brand name row could not be found")
        if manufacturer is None:
            manufacturer = brand
        
        return {
            "name": product_name.text,
            "price": float(price),
            "brand_name": brand,
            "manufacturer_name": manufacturer,
            "shelf_name": shelf_name,
            "aisle_name": aisle_name,
            "department_name": self.department_name}
