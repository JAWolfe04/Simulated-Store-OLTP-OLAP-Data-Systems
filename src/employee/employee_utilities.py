""" Employee Utilities

This module contains the employee_utility class with various methods
to interact with employee data.

This module requires 'mysql.connector' to be installed as well as a running
MySQL database.
"""

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
import random
import re
import requests
import pandas
from pathlib import Path
from src.constants import RAND_USER_URL, DEFAULT_REPO_NAME

class employee_utility:
    """
    A class to manipulate employee data for the Simulated Superstore
    employee data system

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
    hire_employee(employee_data)
        - Adds employee to the employee database and repository with the current
          date as start date and updates the manager id for a location if the
          hired employee will be a manager
    fire_employee(employee_id)
        - Marks employee as no longer employed by indicating an end_date
    transfer_employee(employee_id, location_id, position_id)
        - Change employee's position and/or location
    change_salary(employee_id, salary)
        - Changes the employee's salary
    get_open_positions()
        - Returns a list of tuples of all unfilled jobs for all locations with
          each tuple containing location_id and position_id for the job
    create_person()
        - Creates employee data by retrieving data from randomuser.me API and
          either randomly generating a value or making the value None
    update_employee_repository(employee_data)
        - Adds employee's data to an csv employee repository
    """
    def __init__(self, database_connection):
        """
        Parameters
        ----------
        database_connection (mysql.connector.connection.MySQLConnection):
            Connection to the working business database
        """
        
        if (type(database_connection) is not
            mysql.connector.connection.MySQLConnection):
            raise TypeError('Provided connection is wrong type')

        self.database_connection = database_connection
        self.database_cursor = database_connection.cursor()
        
    def hire_employee(self, employee_data, path = None):
        """
        Adds employee to the employee database and repository with the current
        date as start date and updates the manager id for a location if the
        hired employee will be a manager

        Parameters
        ----------
        employee_data (dictionary): Dictionary containing keys for
            employee_id, location_id, position_id, salary, start_date,
            end_date, gender, name, address, city, state_code, postal_code,
            email, dob, phone, cell

        Returns
        -------
        int: employee id
        """
        self.location_id_validator(employee_data.get("location_id"))

        self.salary_and_job_validator(employee_data.get("position_id"),
                          employee_data.get("salary"))

        # Submit employee hire data to database
        query = ("INSERT INTO employee (location_id, position_id, name, "
                 "salary, start_date) VALUES (%s, %s, %s, %s, %s)")
        hire_data = (employee_data.get("location_id"),
                     employee_data.get("position_id"),
                     employee_data.get("name"),
                     employee_data.get("salary"),
                     str(datetime.now().date()))
        self.database_cursor.execute(query, hire_data)
        self.database_connection.commit()

        employee_id = self.database_cursor.lastrowid

        employee_data["employee_id"] = employee_id
        employee_data["start_date"] = hire_data[4]

        self.employee_data_validator(employee_data)

        if path is None:
            path = Path.cwd() / DEFAULT_REPO_NAME

        self.update_employee_repository(employee_data, path, False)
        
        return employee_id

    def hire_all_open_positions(self, path = None):
        open_jobs = self.get_open_positions()
        for job in open_jobs:
            self.hire_employee(self.create_person(job[0], job[1]), path)

    def fire_employee(self, employee_id):
        """
        Marks employee as no longer employed by indicating an end_date
        
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
        self.database_cursor.execute(query, (datetime.now(), employee_id))
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
            query = ("UPDATE employee SET location_id = %s, position_id = %s "
                     "WHERE employee_id = %s")
            self.database_cursor.execute(query, (location_id,
                                                 position_id,
                                                 employee_id))
            self.database_connection.commit()

            if self.database_cursor.rowcount == 0:
                raise ValueError("Provided employee_id was not found")

            return employee_id
        
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_NO_REFERENCED_ROW_2:
                raise ValueError("Provided location_id or position_id does "
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
        int: employee id
        """
        if type(employee_id) is not int:
            raise TypeError('Provided employee_id is not an integer')
        elif type(salary) is not float:
            raise TypeError('Provided salary is not a decimal number')

        # Get employee's position id and check if new salary is in range
        # for their position
        job_query = "SELECT position_id FROM employee WHERE employee_id = %s"
        self.database_cursor.execute(job_query, (employee_id,))
        job_results = self.database_cursor.fetchall()
        if len(job_results) == 0:
            raise ValueError("Provided employee_id was not found")
        
        self.salary_and_job_validator(job_results[0][0], salary)

        query = "UPDATE employee SET salary = %s WHERE employee_id = %s"
        self.database_cursor.execute(query, (salary, employee_id))
        self.database_connection.commit()

        return employee_id

    def get_open_positions(self):
        """
        Returns a list of tuples of all unfilled jobs for all locations with
        each tuple containing location_id and position_id for the job
        """
        query = ("SELECT location_id, position_id "
                 "FROM location AS loc CROSS JOIN job_position AS jobs "
                 "LEFT JOIN "
                     "(SELECT location_id as loc_id, position_id as pos_id, "
                     "employee_id FROM employee WHERE end_date is null) AS emp "
                 "ON emp.loc_id = loc.location_id "
                 "AND emp.pos_id = jobs.position_id "
                 "WHERE employee_id is null;")
        self.database_cursor.execute(query)
        return self.database_cursor.fetchall()

    def create_person(self, location_id, position_id):
        """
        Creates employee data by retrieving data from randomuser.me API and
        either randomly generating a value or making the value None

        Parameters
        ----------
        location_id (int): number indicating location for the employee
        position_id (int): number indicating job position for the employee

        Returns
        -------
        dictionary:  None if the generation was unsuccessful otherwise returns
            dictionary containing keys for employee_id, location_id,
            position_id, salary, start_date, end_date, gender, name, address,
            city, state_code, postal_code, email, dob, phone, cell 
        """

        response = requests.get(RAND_USER_URL)
        
        if not response.ok:
            return None

        self.location_id_validator(location_id)

        # Dont use validate function since the method needs to get the
        # min max salaries to generate a salary and calling the validate
        # function will cause 2 database calls
        if type(position_id) is not int:
            raise TypeError('Provided position_id is not an integer')
        
        query = ("SELECT min_salary, max_salary FROM job_position "
                 "WHERE position_id = %s")
        self.database_cursor.execute(query, (position_id,))
        query_result = self.database_cursor.fetchall()
        if len(query_result) == 0:
            raise ValueError('Provided position_id does not exist')

        min_salary, max_salary = query_result[0]
        salary = round(random.uniform(float(min_salary), float(max_salary)), 2)
        
        response_json = response.json().get("results")[0]
        
        emp_name = (response_json.get("name").get("first") + " "
                    + response_json.get("name").get("last"))
        location_dict = response_json.get("location")
        emp_address = (str(location_dict.get("street").get("number")) + " "
                       + location_dict.get("street").get("name"))
        us_state_abbrev = {
            'Alabama': 'AL', 'Alaska': 'AK', 'American Samoa': 'AS',
            'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
            'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE',
            'District of Columbia': 'DC', 'Florida': 'FL', 'Georgia': 'GA',
            'Guam': 'GU', 'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL',
            'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS', 'Kentucky': 'KY',
            'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD',
            'Massachusetts': 'MA', 'Michigan': 'MI', 'Minnesota': 'MN',
            'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
            'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH',
            'New Jersey': 'NJ', 'New Mexico': 'NM', 'New York': 'NY',
            'North Carolina': 'NC', 'North Dakota': 'ND',
            'Northern Mariana Islands':'MP', 'Ohio': 'OH', 'Oklahoma': 'OK',
            'Oregon': 'OR', 'Pennsylvania': 'PA', 'Puerto Rico': 'PR',
            'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD',
            'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
            'Virgin Islands': 'VI', 'Virginia': 'VA', 'Washington': 'WA',
            'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'}
        
        emp_state = us_state_abbrev.get(location_dict.get("state"))
        emp_dob = response_json.get("dob").get("date")[0:10]
        
        employee_data = {"employee_id": None, "location_id": location_id,
                         "position_id": position_id, "salary": salary,
                         "start_date": None, "end_date": None,
                         "gender": response_json.get("gender")[0],
                         "name": emp_name,
                         "address": emp_address,
                         "city": location_dict.get("city"),
                         "state_code": emp_state,
                         "postal_code": str(location_dict.get("postcode")),
                         "email": response_json.get("email"),
                         "dob": emp_dob,
                         "phone":response_json.get("phone"),
                         "cell": response_json.get("cell")}
        
        return employee_data

    def update_employee_repository(self, employee_data, repo_name,
                                   validate = True):
        """
        Adds employee's data to an csv employee repository

        Parameters
        ----------
        employee_data (dictionary): Dictionary containing keys for
            employee_id, location_id, position_id, salary, start_date,
            end_date, gender, name, address, city, state_code, postal_code,
            email, dob, phone, cell

        repo_name (str): Full file path name for the csv employee repository

        validate (bool): Indicates if the employee_data should be validated
        """

        if validate:
            self.employee_data_validator(employee_data)

            self.employee_id_validator(employee_data.get("employee_id"))

            self.location_id_validator(employee_data.get("location_id"))

            self.salary_and_job_validator(employee_data.get("position_id"),
                              employee_data.get("salary"))

        if Path(repo_name).suffix != ".csv":
            raise ValueError("Provided repo_name is not csv")

        try:
            repo_df = pandas.read_csv(repo_name)
            repo_df = repo_df.set_index("employee_id")
            repo_df = repo_df.astype({"postal_code": str})
            new_data_df = pandas.DataFrame.from_dict([employee_data])
            new_data_df = new_data_df.set_index("employee_id")
            if employee_data.get("employee_id") in repo_df.index:
                repo_df.update(new_data_df)
            else:
                repo_df = repo_df.append(new_data_df)
            repo_df.to_csv(repo_name)
        except (pandas.errors.EmptyDataError, FileNotFoundError):
            repo_df = pandas.DataFrame.from_dict([employee_data])
            repo_df = repo_df.set_index("employee_id")
            repo_df.to_csv(repo_name)

    def employee_id_validator(self, employee_id):
        if type(employee_id) is not int:
            raise TypeError("Provided employee_id is not a number")

        query = "SELECT employee_id FROM employee WHERE employee_id = %s"
        self.database_cursor.execute(query, (employee_id,))
        if len(self.database_cursor.fetchall()) == 0:
            raise ValueError("Provided employee_id does not exist")
        pass

    def location_id_validator(self, location_id):
        if type(location_id) is not int:
            raise TypeError("Provided location_id is not a number")
        
        query = "SELECT location_id FROM location WHERE location_id = %s"
        self.database_cursor.execute(query, (location_id,))
        if len(self.database_cursor.fetchall()) == 0:
            raise ValueError("Provided location_id does not exist")
        

    def salary_and_job_validator(self, position_id, salary):
        """
        Checks if position_id exists and if the salary is within the
        min/max salary range for the position

        Parameters
        ----------
        position_id (int): number indicating job position for the employee
        salary (int): salary for the employee
        """

        if type(position_id) is not int:
                raise TypeError('Provided position_id is not an integer')
        elif type(salary) is not float:
                raise TypeError('Provided salary is not a decimal number')
            
        salary_query = ("SELECT min_salary, max_salary FROM job_position "
                        "WHERE position_id = %s")
        self.database_cursor.execute(salary_query, (position_id,))
        salary_result = self.database_cursor.fetchall()
        if not salary_result:
            raise ValueError("Provided position_id does not exist")
        min_salary, max_salary = salary_result[0]
        if salary < min_salary:
            raise ValueError("Provided salary less than minimum allowable "
                             "salary for this position")
        elif salary > max_salary:
            raise ValueError("Provided salary greater than maximum "
                             "allowable salary for this position")

    def employee_data_validator(self, employee_data):
        """
        Verifies certain fields of the employee data

        Parameters
        ----------
        employee_data (dictionary): Dictionary containing keys for
            employee_id, location_id, position_id, salary, start_date,
            end_date, gender, name, address, city, state_code, postal_code,
            email, dob, phone, cell

        Raises:
            TypeError:
              - If employee_data is not a dictionary
              - If start_date, gender, name, address, city, state_code,
                postal_code, email, dob phone or cell fields are not strings
            ValueError:
              - If employee_data does not have the expected keys
              - If start_date or dob is not formatted YYYY-MM-DD
              - If gender is not 'm' or 'f'
              - If name is not a first and last name
              - If address or city is empty or white spaces
              - If state_code is not 2 capital letters
              - If postal_code is not 5 digits
              - If email is not a valid email format
              - If phone or cell are not formatted (###)-###-####
        """
        if type(employee_data) is not dict:
            raise TypeError("Provided employee_data is not a dictionary")

        if(list(employee_data.keys()) != [
            "employee_id", "location_id", "position_id", "salary", "start_date",
            "end_date", "gender", "name", "address", "city", "state_code",
            "postal_code", "email", "dob", "phone", "cell"]):
            raise ValueError("Provided employee_data is formated incorrectly")

        str_checks = ("start_date", "gender", "name", "address",
                      "city", "state_code", "postal_code", "email", "dob",
                      "phone", "cell")
        for key in str_checks:
            if type(employee_data.get(key)) is not str:
                raise TypeError("Provided {} is not a string".format(key))

        phone_regex = r"^\(\d{3}\)-\d{3}-\d{4}$"
        date_regex = r"^[12][90][0-9][0-9]-[01][0-9]-[0-3][0-9]$"
        email_regex = r"^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$"
        postal_regex = r"^\d{5}$"
        state_regex = r"^[A-Z]{2}$"
        
        if not re.search(date_regex, employee_data.get("start_date")):
            raise ValueError("Provided start_date is not formatted: "
                             "YYYY-MM-DD")
        elif (employee_data.get("gender") != "m" and
              employee_data.get("gender") != "f"):
            raise ValueError("Provided gender must be m or f")
        elif len(employee_data.get("name").split()) != 2:
            raise ValueError("Provided name must be first and last names")
        elif len(employee_data.get("address").strip()) == 0:
            raise ValueError("Provided address is invalid")
        elif len(employee_data.get("city").strip()) == 0:
            raise ValueError("Provided city must be a name")
        elif not re.search(state_regex, employee_data.get("state_code")):
            raise ValueError("Provided state_code is not formatted: AZ")
        elif not re.search(postal_regex, employee_data.get("postal_code")):
            raise ValueError("Provided postal_code is not formatted: #####")
        elif not re.search(email_regex, employee_data.get("email")):
            raise ValueError("Provided email is not formatted correctly")
        elif not re.search(date_regex, employee_data.get("dob")):
            raise ValueError("Provided dob is not formatted: YYYY-MM-DD")
        elif not re.search(phone_regex, employee_data.get("phone")):
            raise ValueError("Provided phone number is not formatted: "
                             "(###)-###-####")
        elif not re.search(phone_regex, employee_data.get("cell")):
            raise ValueError("Provided cell number is not formatted: "
                             "(###)-###-####")      
