""" Employee Utilities

This module contains the employee_utility class with various methods
to interact with employee data.

This module requires 'mysql.connector' to be installed as well as a running
MySQL database.
"""

import mysql.connector
from mysql.connector import errorcode
import datetime
import requests

RAND_USER_URL = "https://randomuser.me/api/?nat=us&exc=login,picture," \
                "registered,id,nat&noinfo"

class employee_utility:
    """
    A class to hire, fire and transfer/promote employees for the Simulated
    Superstore employee database

    Attributes
    ----------
    database_connection (mysql.connector.connection.MySQLConnection):
        - Connection to the working business database
    database_cursor (mysql.connector.cursor.MySQLCursor):
        - Cursor for entering data to the working business database

    Methods
    -------
    check_salary(position_id, salary)
        - Checks if salary is within the min/max salary range for the position
    hire_employee(location_id, position_id, name, salary)
        - Adds employee to the employee database with the current date
          as start date and returns the employee id
    fire_employee(employee_id)
        - Marks employee as no longer employed in the employee database
    transfer_employee(employee_id, location_id, position_id)
        - Change employee's position and/or location
    change_salary(employee_id, salary)
        - Changes the employee's salary
    create_person()
        - Creates employee data by retrieving data from randomuser.me API
    add_person_to_records(personal_data)
        - Adds employee's personal data such as contact and payment information
        to an xml record
    """
    def __init__(self, database_connection):
        """
        Parameters
        ----------
        database_connection (mysql.connector.connection.MySQLConnection):
            Connection to the working business database
        """
        
        if type(database_connection) is not \
           mysql.connector.connection.MySQLConnection:
            raise TypeError('Provided connection is wrong type')

        self.database_connection = database_connection
        self.database_cursor = database_connection.cursor()

    def check_salary(self, position_id, salary):
        """
        Checks if salary is within the min/max salary range for the position

        Parameters
        ----------
        position_id (int): number indicating job position for the employee
        salary (int): salary for the employee
        """
        salary_query ="""SELECT min_salary, max_salary FROM job_position
                            WHERE position_id = %s"""
        self.database_cursor.execute(salary_query, (position_id,))
        salary_result = self.database_cursor.fetchall()
        if not salary_result:
            raise ValueError("Provided position_id does not exist")
        min_salary, max_salary = salary_result[0]
        if salary < min_salary:
            raise ValueError("Provided salary less than minimum allowable " \
                                "salary for this position")
        elif salary > max_salary:
            raise ValueError("Provided salary greater than maximum " \
                                "allowable salary for this position")
        
    def hire_employee(self, location_id, position_id, name, salary):
        """
        Adds employee to the employee database with the current date as start
        date and returns the employee id

        Parameters
        ----------
        location_id (int): number indicating store location for the new employee
        position_id (int): number indicating job position for the new employee
        name (str): full name of the employee
        salary (int): salary for the new employee

        Returns
        -------
        int: employee id
        """
        
        try:
            # Check if arguments fit type and value restrictions
            if type(location_id) is not int:
                raise TypeError('Provided location_id is not an integer')
            elif type(position_id) is not int:
                raise TypeError('Provided position_id is not an integer')
            elif type(name) is not str:
                raise TypeError('Provided name is not a string')
            elif len(name.strip()) == 0:
                raise ValueError('Provided name does not contain a name')
            elif type(salary) is not float:
                raise TypeError('Provided salary is not a decimal number')

            self.check_salary(position_id, salary)

            # Submit employee hire data to database
            query = """INSERT INTO employee (location_id, position_id, name,
                            salary, start_date) VALUES (%s, %s, %s, %s, %s)"""
            hire_data = (location_id, position_id, name, salary,
                         datetime.datetime.now())
            self.database_cursor.execute(query, hire_data)
            self.database_connection.commit()
            
            return self.database_cursor.lastrowid
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError("Provided location_id does not exist")

    def fire_employee(self, employee_id):
        """
        Marks employee as no longer employed in the employee database
        Parameters
        ----------
        employee_id (int): number identifying employee

        Returns
        -------
        int: employee id
        """
        if type(employee_id) is not int:
            raise TypeError('Provided employee_id is not an integer')
        
        query = "UPDATE employee SET end_date = %s WHERE employee_id = %s"
        self.database_cursor.execute(query, (datetime.datetime.now(),
                                             employee_id))
        self.database_connection.commit()
    
        if self.database_cursor.rowcount == 0:
            raise ValueError("Provided employee_id was not found")

        return employee_id

    def transfer_employee(self, employee_id, location_id, position_id):
        """
        Change employee's position and/or location

        Parameters
        ----------
        employee_id (int): number identifying employee
        location_id (int): number indicating new location for the employee
        position_id (int): number indicating new job position for the employee

        Returns
        -------
        int: employee id
        """
        if type(employee_id) is not int:
            raise TypeError('Provided employee_id is not an integer')
        elif type(location_id) is not int:
            raise TypeError('Provided location_id is not an integer')
        elif type(position_id) is not int:
            raise TypeError('Provided position_id is not an integer')
        
        try:
            query = "UPDATE employee SET location_id = %s, position_id = %s" \
                    " WHERE employee_id = %s"
            self.database_cursor.execute(query, (location_id,
                                                 position_id,
                                                 employee_id))
            self.database_connection.commit()

            if self.database_cursor.rowcount == 0:
                raise ValueError("Provided employee_id was not found")

            return employee_id
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError("Provided location_id or position_id does " \
                                 "not exist")

    def change_salary(self, employee_id, salary):
        """
        Changes the employee's salary

        Parameters
        ----------
        employee_id (int): number identifying employee
        salary (float): new salary for the employee

        Returns
        -------
        int: 0 if the salary change was unsuccessful otherwise the employee id >0
        """
        if type(employee_id) is not int:
            raise TypeError('Provided employee_id is not an integer')
        elif type(salary) is not float:
            raise TypeError('Provided salary is not a decimal number')

        # Get employee's position id and check if new salary is in range
        # for their position
        job_query ="SELECT position_id FROM employee WHERE employee_id = %s"
        self.database_cursor.execute(job_query, (employee_id,))
        job_results = self.database_cursor.fetchall()
        if len(job_results) == 0:
            raise ValueError("Provided employee_id was not found")
        
        self.check_salary(job_results[0][0], salary)

        query = "UPDATE employee SET salary = %s WHERE employee_id = %s"
        self.database_cursor.execute(query, (salary, employee_id))
        self.database_connection.commit()

        return employee_id

    def create_person(self):
        """
        Creates employee data by retrieving data from randomuser.me API

        Returns
        -------
        dictionary:  Dictionary containing employee data otherwise None if it
                     was unable to generate the data 
        """
        
        response = requests.get(RAND_USER_URL)
        if response.ok:
            return response
        else:
            return None

    def add_person_to_records(self, personal_data):
        """
        Adds employee's personal data such as contact and payment information
        to an csv record

        Parameters
        ----------
        personal_data (dictionary): Dictionary containing personal data
        
        Returns
        -------
        int: 0 if the insertion was unsuccessful otherwise the employee id >0
        """
        pass
