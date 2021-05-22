""" Product Retriever

MySQL login credentials will need to be supplied in an associated text file
name 'DB_Login_Cred.txt' with the first line containing the name or IP address
of the MySQL server host, the second line containing the name of the user to
connect with and the third containing the user's password.

This module contains the following functions:
    * main - the main function of the module
"""

import mysql.connector

from src.product.product_utilities import product_utility
from src.product.constants import MAX_CATALOG_SIZE, MAX_PRODUCT_LIST_DEPTH
from src import settings

def main():
    mydb = mysql.connector.connect(
          host = settings.OLTP_HOST,
          user = settings.OLTP_USERNAME,
          password = settings.OLTP_PASSWORD,
          port = settings.OLTP_PORT
        )
    mydb.cursor().execute("USE sim_shop_oltp")

    department_links = ['https://www.walmart.com/cp/home/4044',
                       'https://www.walmart.com/cp/office/1229749',
                       'https://www.walmart.com/cp/beauty/1085666',
                       'https://www.walmart.com/cp/health/976760',
                       'https://www.walmart.com/cp/food/976759',
                       'https://www.walmart.com/cp/bath-body/1071969']

    print("Retrieving {} products' data...").format(max_catalog_size)
    utility = product_utility(mydb,
                              MAX_CATALOG_SIZE,
                              MAX_PRODUCT_LIST_DEPTH)
    utility.fill_product_catalog(department_links)
    print("Finished retrieving product data")

if __name__ == "__main__":
    main()
