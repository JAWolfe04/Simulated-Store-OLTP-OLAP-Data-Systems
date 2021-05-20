""" Employee Initializer

MySQL login credentials will need to be supplied in an associated text file
name 'DB_Login_Cred.txt' with the first line containing the name or IP address
of the MySQL server host, the second line containing the name of the user to
connect with and the third containing the user's password.

This module contains the following functions:
    * main - the main function of the module
"""
import os

print("cwd: ", os.getcwd())

from src.employee.employee_utilities import employee_utility
from src import settings
import mysql.connector

def main():
    mydb = mysql.connector.connect(
          host = settings.OLTP_HOST,
          user = settings.OLTP_USERNAME,
          password = settings.OLTP_PASSWORD,
          port = settings.OLTP_PORT
        )
    mydb.cursor().execute("USE sim_shop_oltp")
    
    utilities = employee_utility(mydb)
    open_jobs = utilities.get_open_positions()
    for job in open_jobs:
        print(job[0], job[1])

if __name__ == "__main__":
    main()
