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
import src.product.constants as constant
from src import settings

def main():
    mydb = mysql.connector.connect(
          host = settings.OLTP_HOST,
          user = settings.OLTP_USERNAME,
          password = settings.OLTP_PASSWORD,
          port = settings.OLTP_PORT
        )
    mydb.cursor().execute("USE sim_shop_oltp")

    browser = webdriver.Chrome(
            executable_path = "C:\\WebDriver\\bin\\chromedriver.exe")

    print("Retrieving {} products' data...").format(constant.MAX_CATALOG_SIZE)
    utility = product_utility(mydb,
                              browser,
                              constant.MAX_CATALOG_SIZE,
                              constant.MAX_PRODUCT_LIST_DEPTH)
    utility.fill_product_catalog(constant.DEPARTMENT_LINKS)
    print("Finished retrieving product data")

    driver.close()

if __name__ == "__main__":
    main()
