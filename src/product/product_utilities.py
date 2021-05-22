""" Product Utilities

This module contains the product_utility class with various methods to interact
with product data

This module requires 'mysql.connector' to be installed as well as a running
MySQL database.
"""

import mysql.connector

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
