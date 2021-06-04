""" Product Utilities

This module contains the product_utility class with various methods to interact
with product data

This module requires 'mysql.connector' to be installed as well as a running
MySQL database.
"""
import time
import random
from os import path

import mysql.connector
from bs4 import BeautifulSoup, element
from selenium import webdriver, common

from src import settings

class product_utility:
    """
    A class for manipulating product data the Simulated Superstore data system

    Attributes
    ----------
    database_connection (mysql.connector.connection.MySQLConnection):
        - Connection to the working business database
    database_cursor (mysql.connector.cursor.MySQLCursor):
        - Cursor for entering data to the working business database
    browser (selenium.webdriver.chrome.webdriver.WebDriver):
        - Webdriver to emulate a browser for fetching data from Walmart.com
    max_catalog_size (int):
        - Number indicating the maximum size of the product catalog, must
          be a number greater than 0
    max_product_list_depth (int):
        - Number indicating the maximum number of pages to cycle through
          a product list in Walmart.com to find products, must be a number
          greater than 0
    department_name (str):
        - String representing the currently active department item retrieval

    Methods
    -------
    """
    def __init__(self, database_connection, browser):
        """
        Parameters
        ----------
        database_connection (mysql.connector.connection.MySQLConnection):
            Connection to the working business database
        browser (selenium.webdriver.chrome.webdriver.WebDriver): Webdriver
            to emulate a browser for fetching data from Walmart.com
        """
        if settings.STAGE == "prod":
            print("Initializing class")
        if (type(database_connection) is not
            mysql.connector.connection.MySQLConnection):
            raise TypeError("Provided connection is wrong type")
        elif (type(browser) is not
              webdriver.chrome.webdriver.WebDriver):
            raise TypeError("Provided browser is wrong type")

        self.database_connection = database_connection
        self.database_cursor = database_connection.cursor()
        self.browser = browser
        self.max_catalog_size = 1000
        self.max_product_list_depth = 3
        self.department_name = None
        self.product_links_file_name = "data//Product_Links.txt"
        self.finished_links_file_name = "data//Previous_Links.txt"

    def set_max_catalog_size(self, size):
        if type(size) is not int:
            raise TypeError("Provided max catalog size is not a number")
        elif size < 1:
            raise ValueError("Provided max catalog size cannot be less than 1")
        self.max_catalog_size = size

    def get_max_catalog_size(self):
        return self.max_catalog_size
        
    def set_max_product_list_depth(self, depth):
        if type(depth) is not int:
            raise TypeError("Provided max product list depth is not a number")

        elif depth < 1:
            raise ValueError("Provided max product list depth cannot be less "
                             "than 1")
        self.max_product_list_depth = depth

    def get_max_product_list_depth(self):
        return self.max_product_list_depth

    def set_current_department_name(self, dept_name):
        if type(dept_name) is not str:
            raise TypeError("Provided department name is not a string")
        elif len(dept_name.strip()) == 0:
            raise ValueError("Provided department name must contain a name")
        query = "SELECT department_id FROM department WHERE name = %s"
        self.database_cursor.execute(query, (dept_name,))
        if len(self.database_cursor.fetchall()) == 0:
            raise ValueError("Provided department does not exist")
        self.department_name = dept_name

    def get_current_department_name(self):
        return self.department_name

    def set_product_links_file_name(self, file_name):
        if type(file_name) is not str:
            raise TypeError("Provided product links file name is not a string")
        elif len(file_name.strip()) == 0:
            raise ValueError("Provided product links file department name "
                             "must contain a name")
        
        self.product_links_file_name = file_name

    def get_product_links_file_name(self):
        return self.product_links_file_name

    def set_finished_links_file_name(self, file_name):
        if type(file_name) is not str:
            raise TypeError("Provided previous links file name is not a string")
        elif len(file_name.strip()) == 0:
            raise ValueError("Provided previous links file department name "
                             "must contain a name")
        
        self.finished_links_file_name = file_name

    def get_finished_links_file_name(self):
        return self.finished_links_file_name

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
        if category_header is None:
            category_header = body.find("h2", text = "Shop by category")

        # The heading can occasionally take the for of 'Shop X' category but
        # this have the following class
        if category_header is None:
            category_header = body.find("h2", class_ = "header-title-5DR")

        if category_header is None:
            raise ValueError("Provided body does not contain category list")

        # From the Shop by element, it has an ancester that has 'featured'
        # in its class name
        category_ancestor = category_header.parent
        is_Featured = True
        while(True):
            ancestor_class = category_ancestor.get("class")
            if ancestor_class is None:
                category_ancestor = None
                break
            
            if "featured" in ".".join(ancestor_class).lower():
                break
            
            if "curated" in ".".join(ancestor_class).lower():
                is_Featured = False
                break
                
            category_ancestor = category_ancestor.parent

        if category_ancestor is None:
            raise ValueError("Provided body does not follow expected format")

        # The second child divider of the ancestor class divider contains
        # children with the links for each category
        category_section = None
        child_divs = category_ancestor.find_all("div", recursive = False)
        if child_divs is not None and len(child_divs) > 1:
            category_section = child_divs[1]

        if category_section is None:
            raise ValueError("Provided body does not contain a category "
                             "section")

        if not is_Featured:
            category_section = category_section.ul
        
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
                    print("Warning: Best Seller flag does not have the "
                                     "expected parent format")
                    continue
                link = flag_li_parent.a
                if (link is None or " ".join(link["class"])
                    != "search-result-productimage gridview display-block"):
                    print("Warning: Unable to find expected link to flag")
                    continue
                
                prod_link = link.get("href")
                ext_link_idx = prod_link.find("?")
                if ext_link_idx != -1:
                    prod_link = prod_link[:ext_link_idx]
                    
                if prod_link[0] == "/":
                    prod_link = "https://www.walmart.com" + prod_link
                elif prod_link[0] == "w":
                    prod_link = "https://www." + prod_link
                product_links.add(prod_link)
        
    def retrieve_product_data(self, body):
        """
        Retrieves product data: name, price, brand name, manufacturer name,
        shelf name, aisle name and department name from the provided body
        containing a Walmart.com product page

        Parameters
        ----------
        body (bs4.element.tag): BeautifulSoup body tag for a html Walmart.com
        page containing a list of products to browse

        Returns
        -------
        (dict): Dictionary with name, price, brand_name, manufacturer_name,
                shelf_name, aisle_name and department_name
        """
        if type(body) is not element.Tag:
            raise TypeError("Provided body is not a bs4.element.Tag")

        if type(self.department_name) is not str:
            raise TypeError("Department name is not a string or the "
                            "department name has not been set")
        
        product_name = body.select_one(
            "h1.prod-ProductTitle.prod-productTitle-buyBox.font-bold")
        if product_name is None:
            raise ValueError("Product name could not be found")

        price_section = body.select_one("div.prod-PriceHero")
        if price_section is None:
            raise ValueError("Price could not be found")
        
        dollar_amount = price_section.select_one("span.price-characteristic")
        if dollar_amount is None:
            raise ValueError("Product dollar amount could not be found")
        
        cents_amount  = price_section.select_one("span.price-mantissa")
        if cents_amount is None:
            raise ValueError("Product cent amount could not be found")
        
        price = (dollar_amount.text + '.' + cents_amount.text).replace(",", "")

        breadcrumb_element = body.select_one("ol.breadcrumb-list")
        if breadcrumb_element is None:
            raise ValueError("Breadcrumb could not be found")
        
        breadcrumb_list = breadcrumb_element.contents        
        if len(breadcrumb_list) <= 2:
            raise ValueError("Too few Breadcrumbs, must be at least 3")
        
        aisle_name = breadcrumb_list[1].a.span.text
        shelf_name = None
        if len(breadcrumb_list) > 3:
            shelf_name = breadcrumb_list[-2].a.span.text
        else:
            shelf_name = breadcrumb_list[-1].a.span.text
        
        brand = None
        manufacturer = None
        spec_table = body.select_one(
            "table.product-specification-table.table-striped")
        if spec_table is not None:
            spec_tbody = spec_table.tbody
            spec_rows = spec_tbody.find_all('tr')
            for row in spec_rows:
                cols = row.find_all('td')
                if cols[0].text == 'Brand':
                    if len(cols) == 1:
                        raise ValueError("Brand name could not be found")
                    brand = cols[1].text
                elif cols[0].text == 'Manufacturer':
                    if len(cols) > 1:
                        manufacturer = cols[1].text

        if brand is None:
            brand = body.select_one("a.prod-brandName")
            if brand is not None:
                brand = brand.span.text

        if brand is None:
            raise ValueError("Brand name row could not be found")
        # If a manufacturer is not found, the brand name is usually the
        # manufacturer name as well
        if manufacturer is None:
            manufacturer = brand
        
        return {
            "name": product_name.text,
            "price": float(price),
            "brand_name": brand,
            "manufacturer_name": manufacturer,
            "shelf_name": shelf_name,
            "aisle_name": aisle_name,
            "department_name": self.department_name}

    def retrieve_link_body(self, url, is_product_data = False):
        """
        Retrieves the body of a url from Walmart.com, if the url is for a
        product page the is_product_data flag will need to be set to True
        to retrieve the required specifications table

        Parameters
        ----------
        url (str): URL to be retrieved
        is_product_data (bool): Flag indicating whether a product
            specifications tab needs to be activated to get the specifications
            table

        Returns
        -------
        (bs4.element.tag): BeautifulSoup body tag for the Walmart.com URL
        """
        if type(url) is not str:
            raise TypeError("Provided URL is not a string")
        if type(is_product_data) is not bool:
            raise TypeError("Provided is_product_data is not True/False")

        # loop is to keep waiting 10 seconds for a timeout
        while(True):
            try:
                self.browser.get(url)
                self.browser.set_page_load_timeout(90)
                # Running the scrapper faster triggers a re-captcha
                time.sleep(3)

                page_html = self.browser.page_source
                soupPage = BeautifulSoup(page_html, "html.parser")

                # Handling re-captchas if they do occur
                if soupPage.find("div", {"class": "re-captcha"}):
                    input("Press enter if re-captcha is clear")
                    page_html = self.browser.page_source
                    soupPage = BeautifulSoup(page_html, "html.parser")

                # Status codes are not easily handled by a webdriver, so
                # to handle a 404 from Walmart simply look for a zero results
                if soupPage.find("span", {"class": "zero-results-message "
                                          "message active message-warning "
                                          "message-block"}):
                    raise ValueError("Warning: Returned no results: {}".format(url))

                # Product pages need additional interaction to get the product
                # specifications by clicking on a specifications tab, which
                # reveals a specifications table creation
                if is_product_data:
                    specs_element = self.browser.find_elements_by_xpath(
                        "//*[contains(text(), 'Specifications')]")
                    # Product does not have a Spec table, no need to
                    # activate the table
                    if len(specs_element) == 0:
                        return soupPage.body

                    while(True):                         
                        try:
                            specs_element[0].click()
                            break
                        except common.exceptions.StaleElementReferenceException:
                            specs_element = self.browser.find_elements_by_xpath(
                            "//*[contains(text(), 'Specifications')]")
                        except common.exceptions.ElementNotInteractableException:
                            return soupPage.body
                        except common.exceptions.ElementClickInterceptedException:
                            specs_element = self.browser.find_elements_by_xpath(
                            "//*[contains(text(), 'Specifications')]")
                        
                    time.sleep(2)
                    try:
                        nav = self.browser.find_element_by_class_name(
                                'persistent-subnav-list')
                        new_element = nav.find_elements_by_xpath(
                            "//*[contains(text(), 'Specifications')]")
                        new_element[0].click()
                    except common.exceptions.NoSuchElementException:
                        # Some product detail pages are formatted differently
                        new_element = self.browser.find_elements_by_xpath(
                            "//*[contains(text(), 'Specifications')]")
                        new_element[0].click()

                    page_html = self.browser.page_source
                    soupPage = BeautifulSoup(page_html, "html.parser")

                return soupPage.body
            
            # Handling for a timeout
            except common.exceptions.TimeoutException:
                print("Timout occured for {}".format(url))
                time.sleep(10)
    
    def store_product_data(self, product_data):
        """
        Stores input product_data in the product database

        Parameters
        ----------
        product_data(dict): Dictionary with name, price, brand_name,
                manufacturer_name, shelf_name, aisle_name and department_name

        Returns
        -------
        (int): Product number id for the entered product data
        """
        if type(product_data) is not dict:
            raise TypeError("Provided product data is not a dictionary")

        string_keys = ["name", "brand_name", "manufacturer_name", "shelf_name",
                       "aisle_name", "department_name"]
        for key in string_keys:
            if type(product_data.get(key)) is not str:
                raise TypeError(
                    "Provided product data {} is not a string".format(key))
            if len(product_data.get(key).strip()) == 0:
                raise ValueError(
                    "Provided product data {} must contain a name".format(key))

        if type(product_data.get("price")) is not float:
            raise TypeError("Provided product data price is not a decimal")
        if product_data.get("price") <= 0:
            raise ValueError("Provided product price must be greater than 0")

        query = "SELECT shelf_id FROM shelf WHERE shelf_name = %s;"
        self.database_cursor.execute(query, (product_data.get("shelf_name"),))
        shelf_id_result = self.database_cursor.fetchall()

        shelf_id = None
        if len(shelf_id_result) == 0:
            query = "SELECT department_id FROM department WHERE name = %s;"
            self.database_cursor.execute(query,
                                         (product_data.get("department_name"),))
            dept_id_result = self.database_cursor.fetchall()
            if len(dept_id_result) == 0:
                raise ValueError("Provided department name does not exist")
            
            dept_id = dept_id_result[0][0]
            query = ("INSERT INTO shelf(department_id, shelf_name, aisle_name)"
                     " VALUES (%s, %s, %s);")
            self.database_cursor.execute(query, (
                dept_id,
                product_data.get("shelf_name"),
                product_data.get("aisle_name")))
            self.database_connection.commit()
            shelf_id = self.database_cursor.lastrowid
        else:
            shelf_id = shelf_id_result[0][0]

        try:
            query = ("INSERT INTO product(shelf_id, product_name, price, "
                     "brand_name, manufacturer_name) "
                     "VALUES (%s, %s, %s, %s, %s);")
            self.database_cursor.execute(
                query, (shelf_id,
                        product_data.get("name"),
                        product_data.get("price"),
                        product_data.get("brand_name"),
                        product_data.get("manufacturer_name")))
            self.database_connection.commit()
        except mysql.connector.errors.IntegrityError:
            print("Warning: {} already exists in system".format(
                product_data.get("name")))
        except mysql.connector.errors.DataError:
            name = product_data.get("name")
            print("Warning: Name {} is too long with {} characters".format(
                name, len(name)))
        
        return self.database_cursor.lastrowid

    def retrieve_product_catalog(self, product_links):
        """
        Takes a list of product links, retrieves the product data
        for each link then stores the product data in a product database.
        The number of products is limited by the max_catalog_size specified
        for the class. Remaining product links to be added are entered in the
        product_links_file_name for the class.
    
        Parameters
        ----------
        product_links (set): Set of product links
        """
        product_links = list(product_links)
        catalog_size = len(product_links)
        if len(product_links) > self.max_catalog_size:
            if settings.STAGE == "prod":
                print("Scambleing products")
            catalog_size = self.max_catalog_size
            random.shuffle(product_links)
            with open(self.product_links_file_name, "w") as file:
                for link in product_links:
                    file.write("{}".format(link))
        if settings.STAGE == "prod":
            print("Collecting product data...")
        batch_removal_counter = 0
        for idx in range(0, catalog_size):
            try:
                page_body = self.retrieve_link_body(product_links[idx], True)
                product_data = self.retrieve_product_data(page_body)
                self.store_product_data(product_data)
                batch_removal_counter += 1
                if batch_removal_counter == 40:
                    if settings.STAGE == "prod":
                        print("Removing batched {} links".format(
                            batch_removal_counter))
                    with open(self.product_links_file_name, "w") as file:
                        for link in product_links[idx + 1:]:
                            file.write("{}\n".format(link))
                    batch_removal_counter = 0
            except ValueError as error:
                self.log_error(error, product_links[idx])
            except TypeError as error:
                print("Warning: {} for {}".format(
                        error, product_links[idx]))
                
        print("Product data collection complete")

    def retrieve_product_links(
        self, link, previous_links, finished_links, product_links):
        """
        Collects links of bestseller products from all subcategories following
        the provided link without revisiting categories

        Parameters
        ----------
        link (str): URL to be retrieved
        previous_links (set): Set of previously visited pages
        prev_product_lists (set): Set of previously visited product list links
        product_links (set): Set of product links
        """
        if type(link) is not str:
            raise TypeError("Provided link is not a string")
        elif len(link.strip()) == 0:
            raise ValueError("Provided link must contain a link")
        elif type(previous_links) is not set:
            raise TypeError("Provided previous_links is not a set")
        elif type(finished_links) is not set:
            raise TypeError("Provided finished_links is not a set")
        elif type(product_links) is not set:
            raise TypeError("Provided product_links is not a set")

        previous_links.add(link)
        try:
            page_body = self.retrieve_link_body(link)
        except ValueError as error:
                self.log_error(error, link)
        else:
            prod_list_tag = page_body.find("div",{
                "class":"search-product-result"})
            if prod_list_tag is not None:
                if link not in finished_links:
                    finished_links.add(link)
                    try:
                        self.retrieve_bestseller_links(
                            page_body, product_links)
                    except ValueError as error:
                        self.log_error(error, link)
                    for page in range(2, self.get_max_product_list_depth() + 1):
                        page_link = link + "&page={}".format(page)
                        try:
                            prod_body = self.retrieve_link_body(page_link)
                            self.retrieve_bestseller_links(
                                prod_body, product_links)
                        except ValueError as error:
                            self.log_error(error, link)
                    with open(self.get_product_links_file_name(),
                              "w") as file:
                        for line in product_links:
                            file.write(line + "\n")
            else:
                try:
                    category_links = self.retrieve_category_links(page_body)
                    for category_link in category_links:
                        if (category_link not in previous_links
                                and category_link not in finished_links):
                            self.retrieve_product_links(category_link,
                                                        previous_links,
                                                        finished_links,
                                                        product_links)
                except ValueError as error:
                    self.log_error(error, link)
                
        finished_links.add(link)
        with open(self.get_finished_links_file_name(), "a") as file:
            file.write(link + "\n")

    def fill_product_catalog(self, dept_list):
        """
        Populates a product database with bestselling products from Walmart

        Parameters
        ----------
        dept_list (dict): List of Walmart product department links
        """
        if type(dept_list) is not dict:
            raise TypeError("Provided department list is not a dictionary")
        
        previous_links = set()
        prev_product_lists = set()
        product_links = set()
        
        if path.isfile(self.get_product_links_file_name()):
            with open(self.get_product_links_file_name(), "r") as file:
                for line in file.readlines():
                    product_links.add(line.strip())
                
        if path.isfile(self.get_finished_links_file_name()):
            with open(self.get_finished_links_file_name(), "r") as file:
                for line in file.readlines():
                    prev_product_lists.add(line.strip())


        for dept_link in dept_list.keys():
            if settings.STAGE == "prod":
                print("Collecting product links for {}".format(dept_link))
            self.set_current_department_name(dept_list.get(dept_link))
            self.retrieve_product_links(
                dept_link, previous_links, prev_product_lists, product_links)
            self.retrieve_product_catalog(product_links)
            product_links = set()

    def log_error(self, error, link):
        """
        Prints errors to the console in a unified manner

        Parameters
        ----------
        error(Exception): the exception instance
        link(str): link that raised the error 
        """
        if str(error)[0:4] == "Warn":
            print(error)
        else:
            print("Warning: {} for {}".format(error, link))
            
