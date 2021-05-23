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
        
        
        
