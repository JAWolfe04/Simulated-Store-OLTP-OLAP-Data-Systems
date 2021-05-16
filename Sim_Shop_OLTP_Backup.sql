CREATE DATABASE  IF NOT EXISTS `sim_shop_oltp`;
USE `sim_shop_oltp`;

CREATE TABLE department (
  department_id int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (department_id),
  UNIQUE KEY department_id (department_id)
);

INSERT INTO department(`name`) VALUES 
	('Management'),
	('Home and Office'),
	('Beauty, Bath and Health'),
	('Food');
	
CREATE TABLE job_position (
  position_id int NOT NULL AUTO_INCREMENT,
  department_id int NOT NULL,
  title varchar(50) NOT NULL,
  min_salary decimal(10,0) NOT NULL,
  max_salary decimal(10,0) NOT NULL,
  PRIMARY KEY (position_id),
  UNIQUE KEY position_id (position_id),
  KEY department_id_idx (department_id),
  CONSTRAINT job_position_ibfk_1 FOREIGN KEY (department_id) REFERENCES department (department_id)
);

INSERT INTO job_position(department_id, title, min_salary, max_salary) VALUES 
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
	(4,'Stock Clerk',27000,49000);
	
CREATE TABLE location (
  location_id int NOT NULL AUTO_INCREMENT,
  manager_id int DEFAULT NULL,
  state_code varchar(2) NOT NULL,
  city varchar(25) NOT NULL,
  postal_code varchar(9) NOT NULL,
  address_line varchar(100) NOT NULL,
  PRIMARY KEY (location_id),
  UNIQUE KEY location_id (location_id),
);

INSERT INTO location(manager_id, state_code, city, postal_code, address_line) VALUES 
	(NULL,'KS','Overland Park','66210','11701 Metcalf Ave'),
	(NULL,'AL','Montgomery','36117','6495 Atlanta Hwy'),
	(NULL,'MO','Kansas City','64133','11601 E Us Highway 40'),
	(NULL,'AL','Mobile','36606','101 E I65 Service Rd S'),
	(NULL,'MO','Kansas City','64145','1701 W 133rd St'),
	(NULL,'DC','Washington','20001','99 H Street Nw'),
	(NULL,'CA','Burbank','91502','1301 N Victory Pl'),
	(NULL,'TX','Houston','77081','5405 South Rice Avenue'),
	(NULL,'FL','North Miami Beach','33162','1425 Ne 163rd St'),
	(NULL,'NJ','Secaucus','07094','400 Park Pl');

CREATE TABLE employee (
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
  CONSTRAINT employee_ibfk_1 FOREIGN KEY (location_id) REFERENCES location (location_id),
  CONSTRAINT employee_ibfk_2 FOREIGN KEY (position_id) REFERENCES job_position (position_id)
);

ALTER TABLE location ADD CONSTRAINT location_ibfk_1
FOREIGN KEY (manager_id) REFERENCES employee (employee_id);

CREATE TABLE shelf (
  shelf_ID int NOT NULL AUTO_INCREMENT,
  department_id int NOT NULL,
  shelf_name varchar(50) NOT NULL,
  aisle_name varchar(50) NOT NULL,
  PRIMARY KEY (shelf_ID),
  UNIQUE KEY shelf_ID (shelf_ID),
  KEY department_id (department_id),
  CONSTRAINT shelf_ibfk_1 FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE product (
  product_id int NOT NULL AUTO_INCREMENT,
  shelf_id int NOT NULL,
  product_name varchar(100) NOT NULL,
  brand_name varchar(100) NOT NULL,
  manufacturer_name varchar(100) NOT NULL,
  PRIMARY KEY (product_id),
  UNIQUE KEY product_id (product_id),
  UNIQUE KEY product_name_UNIQUE (product_name),
  KEY shelf_id (shelf_id),
  CONSTRAINT product_ibfk_1 FOREIGN KEY (shelf_id) REFERENCES shelf (shelf_ID)
);

CREATE TABLE inventory (
  inventory_id int NOT NULL AUTO_INCREMENT,
  product_id int NOT NULL,
  location_id int NOT NULL,
  quantity_in_storage int NOT NULL,
  quantity_on_shelf int NOT NULL,
  PRIMARY KEY (inventory_id),
  UNIQUE KEY inventory_id (inventory_id),
  KEY product_id (product_id),
  KEY location_id (location_id),
  CONSTRAINT inventory_ibfk_1 FOREIGN KEY (product_id) REFERENCES product (product_id),
  CONSTRAINT inventory_ibfk_2 FOREIGN KEY (location_id) REFERENCES location (location_id)
);

CREATE TABLE payment (
  payment_id int NOT NULL AUTO_INCREMENT,
  location_id int NOT NULL,
  cashier_id int NOT NULL,
  payment_date date NOT NULL,
  amount_paid decimal(10,0) NOT NULL,
  payment_type varchar(6) NOT NULL,
  PRIMARY KEY (payment_id),
  UNIQUE KEY payment_id (payment_id),
  KEY location_id (location_id),
  KEY cashier_id (cashier_id),
  CONSTRAINT payment_ibfk_1 FOREIGN KEY (location_id) REFERENCES location (location_id),
  CONSTRAINT payment_ibfk_2 FOREIGN KEY (cashier_id) REFERENCES employee (employee_id)
);

CREATE TABLE payment_item (
  payment_item_id int NOT NULL AUTO_INCREMENT,
  payment_id int NOT NULL,
  product_id int NOT NULL,
  price decimal(10,0) NOT NULL,
  quantity int NOT NULL,
  PRIMARY KEY (payment_item_id),
  UNIQUE KEY payment_item_id (payment_item_id),
  KEY payment_id (payment_id),
  KEY product_id (product_id),
  CONSTRAINT payment_item_ibfk_1 FOREIGN KEY (payment_id) REFERENCES payment (payment_id),
  CONSTRAINT payment_item_ibfk_2 FOREIGN KEY (product_id) REFERENCES product (product_id)
);