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
    dept_links = ["https://www.walmart.com/cp/home/4044",
                  "https://www.walmart.com/cp/office/1229749",
                  "https://www.walmart.com/cp/beauty/1085666",
                  "https://www.walmart.com/cp/health/976760",
                  "https://www.walmart.com/cp/food/976759",
                  "https://www.walmart.com/cp/bath-body/1071969"]
    
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
    utility = product_utility(mydb, browser)
    utility.fill_product_catalog(dept_links)
    print("Finished retrieving product data")

    driver.close()

if __name__ == "__main__":
    main()
