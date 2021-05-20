""" Employee Initializer

MySQL login credentials will need to be supplied in an associated text file
name 'DB_Login_Cred.txt' with the first line containing the name or IP address
of the MySQL server host, the second line containing the name of the user to
connect with and the third containing the user's password.

This module contains the following functions:
    * main - the main function of the module
"""
import mysql.connector

from src.employee.employee_utilities import employee_utility
from src import settings

def main():
    mydb = mysql.connector.connect(
          host = settings.OLTP_HOST,
          user = settings.OLTP_USERNAME,
          password = settings.OLTP_PASSWORD,
          port = settings.OLTP_PORT
        )
    mydb.cursor().execute("USE sim_shop_oltp")

    print("Generating employees...")
    employee_utility(mydb).hire_all_open_positions()
    print("All open positions filled")

if __name__ == "__main__":
    main()
