import pytest
import datetime

import mysql.connector
from selenium import webdriver

from src import settings

@pytest.fixture(scope="session")
def browser():
    driver = webdriver.Chrome(
            executable_path = "C:\\WebDriver\\bin\\chromedriver.exe")
    yield driver
    driver.close()

@pytest.fixture(scope="session")
def session():
    connection = mysql.connector.connect(
        host = settings.OLTP_TEST_HOST,
        user = settings.OLTP_TEST_USERNAME,
        password = settings.OLTP_TEST_PASSWORD,
        port = settings.OLTP_TEST_PORT)
    yield connection
    connection.close()

@pytest.fixture(scope="session")
def dev_session():
    connection = mysql.connector.connect(
        host = settings.OLTP_HOST,
        user = settings.OLTP_USERNAME,
        password = settings.OLTP_PASSWORD,
        port = settings.OLTP_PORT)
    yield connection
    connection.close()

@pytest.fixture(scope="session")
def dev_cursor(dev_session):
    cursor = dev_session.cursor()
    cursor.execute("USE sim_shop_oltp")
    yield cursor
    
@pytest.fixture(scope="session")
def cursor(session):
    cursor = session.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS testdb")
    cursor.execute("USE testdb")
    session.commit()
    yield cursor
    cursor.execute("DROP DATABASE IF EXISTS testdb")
    session.commit()

@pytest.fixture(scope="session")
def setup_departments(session, cursor):
    cursor.execute("""CREATE TABLE department (
                       department_id int NOT NULL AUTO_INCREMENT,
                       name varchar(50) NOT NULL,
                       PRIMARY KEY (department_id),
                       UNIQUE KEY department_id (department_id))""")
    session.commit()
    cursor.execute("""INSERT INTO department(name) VALUES 
                       ('Management'),('Home and Office'),
                       ('Beauty, Bath and Health'),('Food')""")
    session.commit()

@pytest.fixture(scope="session")
def setup_jobs(session, cursor, setup_departments):
    cursor.execute("""CREATE TABLE job_position (
                        position_id int NOT NULL AUTO_INCREMENT,
                        department_id int NOT NULL,
                        title varchar(50) NOT NULL,
                        min_salary decimal(10,0) NOT NULL,
                        max_salary decimal(10,0) NOT NULL,
                        PRIMARY KEY (position_id),
                        UNIQUE KEY position_id (position_id),
                        KEY department_id_idx (department_id),
                        CONSTRAINT job_position_ibfk_1 FOREIGN KEY
                        (department_id) REFERENCES
                        department (department_id))""")
    session.commit()
    cursor.execute("""INSERT INTO job_position(department_id, title,
                        min_salary, max_salary) VALUES
                        (1,'Manager',48000,84000),
                        (1,'Assistant Manager',24000,59000),
                        (1,'Merchandiser',29000,86000),
                        (1,'Janitor',24000,42000),
                        (2,'Sales Associate',19000,58000),
                        (2,'Cashier',20000,32000),
                        (2,'Stock Clerk',27000,49000),
                        (3,'Sales Associate',19000,58000),
                        (3,'Cashier',20000,32000),
                        (3,'Stock Clerk',27000,49000),
                        (4,'Sales Associate',19000,58000),
                        (4,'Cashier',20000,32000),
                        (4,'Stock Clerk',27000,49000)""")
    session.commit()

@pytest.fixture(scope="session")
def setup_locations(session, cursor):
    cursor.execute("""CREATE TABLE location (
                        location_id int NOT NULL AUTO_INCREMENT,
                        manager_id int DEFAULT NULL,
                        state_code varchar(2) NOT NULL,
                        city varchar(25) NOT NULL,
                        postal_code varchar(9) NOT NULL,
                        address_line varchar(100) NOT NULL,
                        PRIMARY KEY (location_id),
                        UNIQUE KEY location_id (location_id))""")
    session.commit()
    cursor.execute("""INSERT INTO location(manager_id, state_code, city,
                        postal_code, address_line) VALUES 
                    (NULL,'KS','Overland Park','66210','11701 Metcalf Ave'),
                    (NULL,'AL','Montgomery','36117','6495 Atlanta Hwy'),
                    (NULL,'MO','Kansas City','64133','11601 E Us Highway 40'),
                    (NULL,'AL','Mobile','36606','101 E I65 Service Rd S'),
                    (NULL,'MO','Kansas City','64145','1701 W 133rd St'),
                    (NULL,'DC','Washington','20001','99 H Street Nw'),
                    (NULL,'CA','Burbank','91502','1301 N Victory Pl'),
                    (NULL,'TX','Houston','77081','5405 South Rice Avenue'),
                    (NULL,'FL','North Miami Beach','33162','1425 Ne 163rd St'),
                    (NULL,'NJ','Secaucus','07094','400 Park Pl')""")
    session.commit()

@pytest.fixture(scope="session")
def setup_employees(session, cursor, setup_locations, setup_jobs):
    cursor.execute("""CREATE TABLE employee (
                          employee_id int NOT NULL AUTO_INCREMENT,
                          location_id int NOT NULL,
                          position_id int NOT NULL,
                          name varchar(50) NOT NULL,
                          salary decimal(10,0) NOT NULL,
                          start_date date NOT NULL,
                          end_date date DEFAULT NULL,
                          PRIMARY KEY (employee_id),
                          UNIQUE KEY employee_id (employee_id),
                          KEY location_id (location_id),
                          KEY position_id (position_id),
                          CONSTRAINT employee_ibfk_1 FOREIGN KEY
                          (location_id) REFERENCES location (location_id),
                          CONSTRAINT employee_ibfk_2 FOREIGN KEY
                          (position_id) REFERENCES job_position (position_id)
                          )""")
    session.commit()
    cursor.execute("""ALTER TABLE location ADD CONSTRAINT location_ibfk_1
            FOREIGN KEY (manager_id) REFERENCES employee (employee_id)""")
    session.commit()

@pytest.fixture(scope="session")
def setup_shelf(session, cursor, setup_departments):
    cursor.execute("""CREATE TABLE shelf (
                          shelf_id int NOT NULL AUTO_INCREMENT,
                          department_id int NOT NULL,
                          shelf_name varchar(50) NOT NULL,
                          aisle_name varchar(50) NOT NULL,
                          PRIMARY KEY (shelf_id),
                          UNIQUE KEY shelf_id (shelf_id),
                          KEY department_id (department_id),
                          CONSTRAINT shelf_ibfk_1 FOREIGN KEY
                          (department_id) REFERENCES department (department_id)
                          )""")
    session.commit()

@pytest.fixture(scope="session")
def setup_product(session, cursor, setup_shelf):
    cursor.execute("""CREATE TABLE product (
                        product_id int NOT NULL AUTO_INCREMENT,
                        shelf_id int NOT NULL,
                        product_name varchar(200) NOT NULL,
                        price decimal(6,2) NOT NULL,
                        brand_name varchar(100) NOT NULL,
                        manufacturer_name varchar(100) NOT NULL,
                        PRIMARY KEY (product_id),
                        UNIQUE KEY product_id (product_id),
                        UNIQUE KEY product_name (product_name),
                        KEY shelf_id (shelf_id),
                        CONSTRAINT product_ibfk_1 FOREIGN KEY
                          (shelf_id) REFERENCES shelf (shelf_id)
                        )""")
    session.commit()

@pytest.fixture
def reset_employees(session, cursor):
    cursor.execute("DELETE FROM employee")
    cursor.execute("ALTER TABLE employee AUTO_INCREMENT = 1")
    session.commit()

@pytest.fixture
def reset_shelves(session, cursor):
    cursor.execute("DELETE FROM shelf")
    cursor.execute("ALTER TABLE shelf AUTO_INCREMENT = 1")
    session.commit()

@pytest.fixture
def reset_products(session, cursor):
    cursor.execute("DELETE FROM product")
    cursor.execute("ALTER TABLE product AUTO_INCREMENT = 1")
    session.commit()

@pytest.fixture
def setup_employee(session, cursor):
    add_employee_query = (
        "INSERT INTO employee (location_id, position_id, "
        "name, salary, start_date) VALUES (%s, %s, %s, %s, %s)")
    cursor.execute(
        add_employee_query,
        (1, 1, 'Jane Doe', 50000.00, datetime.datetime.now()))
    session.commit()
    return cursor.lastrowid

@pytest.fixture
def sim_product_data():
    return {"name": "Cuisinart Toaster Oven Broilers Air Fryer",
            "price": 199.00,
            "brand_name": "Cuisinart",
            "manufacturer_name": "Conair",
            "shelf_name": "Toaster Ovens",
            "aisle_name":"Appliances",
            "department_name": "Home and Office"}
