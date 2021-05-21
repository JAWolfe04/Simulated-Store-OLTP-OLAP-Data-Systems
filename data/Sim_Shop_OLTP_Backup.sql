CREATE DATABASE  IF NOT EXISTS `sim_shop_oltp`
USE `sim_shop_oltp`;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS department;
CREATE TABLE department (
  department_id int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (department_id),
  UNIQUE KEY department_id (department_id)
) AUTO_INCREMENT=5;

INSERT INTO department VALUES 
	(1,'Management'),
	(2,'Home and Office'),
	(3,'Beauty, Bath and Health'),
	(4,'Food');

--
-- Table structure for table `employee`
--

DROP TABLE IF EXISTS employee;
CREATE TABLE employee (
  employee_id int NOT NULL AUTO_INCREMENT,
  location_id int NOT NULL,
  position_id int NOT NULL,
  `name` varchar(50) NOT NULL,
  salary decimal(10,0) NOT NULL,
  start_date date NOT NULL,
  end_date date DEFAULT NULL,
  PRIMARY KEY (employee_id),
  UNIQUE KEY employee_id (employee_id),
  KEY location_id (location_id),
  KEY position_id (position_id),
  CONSTRAINT employee_ibfk_1 FOREIGN KEY (location_id) REFERENCES location (location_id),
  CONSTRAINT employee_ibfk_2 FOREIGN KEY (position_id) REFERENCES job_position (position_id)
) AUTO_INCREMENT=131 ;

--
-- Dumping data for table `employee`
--

INSERT INTO employee VALUES 
	(1,10,1,'Neil Sutton',81259,'2021-05-20',NULL),
	(2,9,1,'Darlene Lewis',66586,'2021-05-20',NULL),
	(3,8,1,'Elmer Douglas',60171,'2021-05-20',NULL),
	(4,7,1,'Juan Russell',81596,'2021-05-20',NULL),
	(5,6,1,'Debbie Morales',54009,'2021-05-20',NULL),
	(6,5,1,'Judith Neal',52553,'2021-05-20',NULL),
	(7,4,1,'Hilda Simpson',69835,'2021-05-20',NULL),
	(8,3,1,'Lance Murray',68577,'2021-05-20',NULL),
	(9,2,1,'Frances Shelton',51540,'2021-05-20',NULL),
	(10,1,1,'Arthur Russell',66490,'2021-05-20',NULL),
	(11,10,2,'Savannah Snyder',39355,'2021-05-20',NULL),
	(12,9,2,'Kaylee Armstrong',25517,'2021-05-20',NULL),
	(13,8,2,'Claude Carr',28789,'2021-05-20',NULL),
	(14,7,2,'Janet Chavez',36238,'2021-05-20',NULL),
	(15,6,2,'Jeffrey Watkins',37313,'2021-05-20',NULL),
	(16,5,2,'Lester Moore',47477,'2021-05-20',NULL),
	(17,4,2,'Brandy Wright',48089,'2021-05-20',NULL),
	(18,3,2,'Harvey George',53371,'2021-05-20',NULL),
	(19,2,2,'Isaiah Carter',52275,'2021-05-20',NULL),
	(20,1,2,'Daniel Ramirez',51229,'2021-05-20',NULL),
	(21,10,3,'Leroy Brewer',76752,'2021-05-20',NULL),
	(22,9,3,'Darryl Wilson',41246,'2021-05-20',NULL),
	(23,8,3,'Harvey Tucker',81311,'2021-05-20',NULL),
	(24,7,3,'Kent Fowler',82181,'2021-05-20',NULL),
	(25,6,3,'Alan Walters',82254,'2021-05-20',NULL),
	(26,5,3,'Anthony Webb',29718,'2021-05-20',NULL),
	(27,4,3,'Lance Griffin',76639,'2021-05-20',NULL),
	(28,3,3,'Thomas Russell',58651,'2021-05-20',NULL),
	(29,2,3,'Kyle Simpson',53427,'2021-05-20',NULL),
	(30,1,3,'Dawn Barrett',41010,'2021-05-20',NULL),
	(31,10,4,'Dan Hale',36395,'2021-05-20',NULL),
	(32,9,4,'Sheila Washington',30890,'2021-05-20',NULL),
	(33,8,4,'Kenzi Jacobs',38055,'2021-05-20',NULL),
	(34,7,4,'Kristina Sullivan',39169,'2021-05-20',NULL),
	(35,6,4,'Hector Reynolds',24670,'2021-05-20',NULL),
	(36,5,4,'Clayton Evans',41866,'2021-05-20',NULL),
	(37,4,4,'Alvin Reynolds',25749,'2021-05-20',NULL),
	(38,3,4,'Yvonne Grant',36491,'2021-05-20',NULL),
	(39,2,4,'Darryl Duncan',40650,'2021-05-20',NULL),
	(40,1,4,'April Douglas',24959,'2021-05-20',NULL),
	(41,10,5,'Emily Dunn',52112,'2021-05-20',NULL),
	(42,9,5,'Wade Cunningham',30728,'2021-05-20',NULL),
	(43,8,5,'Ashley Sanders',26116,'2021-05-20',NULL),
	(44,7,5,'Linda Fox',33214,'2021-05-20',NULL),
	(45,6,5,'Gregory Perry',34952,'2021-05-20',NULL),
	(46,5,5,'Shelly Lawson',57601,'2021-05-20',NULL),
	(47,4,5,'Joel Perez',21814,'2021-05-20',NULL),
	(48,3,5,'Rita Pearson',55682,'2021-05-20',NULL),
	(49,2,5,'Donald Fletcher',33311,'2021-05-20',NULL),
	(50,1,5,'Debra Hunter',53765,'2021-05-20',NULL),
	(51,10,6,'Jessie Kelly',23966,'2021-05-20',NULL),
	(52,9,6,'Tanya Lucas',26843,'2021-05-20',NULL),
	(53,8,6,'Evelyn Webb',21985,'2021-05-20',NULL),
	(54,7,6,'Erin Ward',29276,'2021-05-20',NULL),
	(55,6,6,'Andy Byrd',28198,'2021-05-20',NULL),
	(56,5,6,'Randall Brewer',30631,'2021-05-20',NULL),
	(57,4,6,'Tomothy Adams',28693,'2021-05-20',NULL),
	(58,3,6,'Eileen Torres',21375,'2021-05-20',NULL),
	(59,2,6,'Brittany Mitchelle',26799,'2021-05-20',NULL),
	(60,1,6,'Miriam Moore',27425,'2021-05-20',NULL),
	(61,10,7,'Dolores Bates',33263,'2021-05-20',NULL),
	(62,9,7,'Evan Spencer',45786,'2021-05-20',NULL),
	(63,8,7,'Bernice Wade',45172,'2021-05-20',NULL),
	(64,7,7,'Troy Soto',28815,'2021-05-20',NULL),
	(65,6,7,'Roger Reid',32766,'2021-05-20',NULL),
	(66,5,7,'Debra Morris',27227,'2021-05-20',NULL),
	(67,4,7,'Josephine Medina',39671,'2021-05-20',NULL),
	(68,3,7,'Gordon Fernandez',42759,'2021-05-20',NULL),
	(69,2,7,'Brianna Wheeler',41425,'2021-05-20',NULL),
	(70,1,7,'Kenneth Carlson',31853,'2021-05-20',NULL),
	(71,10,8,'Bessie Bates',48646,'2021-05-20',NULL),
	(72,9,8,'Judd Frazier',20964,'2021-05-20',NULL),
	(73,8,8,'Eleanor Perry',42576,'2021-05-20',NULL),
	(74,7,8,'Charlotte Hale',44028,'2021-05-20',NULL),
	(75,6,8,'Jenny Holland',23088,'2021-05-20',NULL),
	(76,5,8,'Phillip Vasquez',30599,'2021-05-20',NULL),
	(77,4,8,'Aiden Lucas',34350,'2021-05-20',NULL),
	(78,3,8,'Sharlene Porter',37283,'2021-05-20',NULL),
	(79,2,8,'Joann Turner',21297,'2021-05-20',NULL),
	(80,1,8,'Dwayne Holt',36192,'2021-05-20',NULL),
	(81,10,9,'Debbie Castro',20701,'2021-05-20',NULL),
	(82,9,9,'Sophie Duncan',27241,'2021-05-20',NULL),
	(83,8,9,'Leslie Shelton',26778,'2021-05-20',NULL),
	(84,7,9,'Kristina Garrett',24561,'2021-05-20',NULL),
	(85,6,9,'Robin Newman',28327,'2021-05-20',NULL),
	(86,5,9,'Alberto Reid',29257,'2021-05-20',NULL),
	(87,4,9,'Tammy Austin',23516,'2021-05-20',NULL),
	(88,3,9,'Dora Mccoy',21603,'2021-05-20',NULL),
	(89,2,9,'Roberta Evans',22201,'2021-05-20',NULL),
	(90,1,9,'Melvin Olson',22599,'2021-05-20',NULL),
	(91,10,10,'Hailey Butler',45945,'2021-05-20',NULL),
	(92,9,10,'Tonya Johnston',32527,'2021-05-20',NULL),
	(93,8,10,'Carlos Bishop',27135,'2021-05-20',NULL),
	(94,7,10,'Scott Lee',47754,'2021-05-20',NULL),
	(95,6,10,'Charlie Cook',34641,'2021-05-20',NULL),
	(96,5,10,'Lance Lewis',47494,'2021-05-20',NULL),
	(97,4,10,'Vera Hernandez',44820,'2021-05-20',NULL),
	(98,3,10,'Regina Holt',37095,'2021-05-20',NULL),
	(99,2,10,'Ian Reed',30506,'2021-05-20',NULL),
	(100,1,10,'Tanya Parker',43203,'2021-05-20',NULL),
	(101,10,11,'Becky Fisher',43173,'2021-05-20',NULL),
	(102,9,11,'Becky Brewer',36179,'2021-05-20',NULL),
	(103,8,11,'Ross Roberts',40429,'2021-05-20',NULL),
	(104,7,11,'Antonio Webb',25648,'2021-05-20',NULL),
	(105,6,11,'Courtney Chambers',30467,'2021-05-20',NULL),
	(106,5,11,'Sharlene Craig',36108,'2021-05-20',NULL),
	(107,4,11,'Marilyn Kennedy',47788,'2021-05-20',NULL),
	(108,3,11,'Edwin Butler',25768,'2021-05-20',NULL),
	(109,2,11,'Beverly Rodriguez',34406,'2021-05-20',NULL),
	(110,1,11,'Jose Ellis',57904,'2021-05-20',NULL),
	(111,10,12,'Erika Gutierrez',31440,'2021-05-20',NULL),
	(112,9,12,'Joann Brooks',31042,'2021-05-20',NULL),
	(113,8,12,'Liam Mitchell',25633,'2021-05-20',NULL),
	(114,7,12,'Max Weaver',20520,'2021-05-20',NULL),
	(115,6,12,'Lester Gregory',30109,'2021-05-20',NULL),
	(116,5,12,'Antonio Webb',24219,'2021-05-20',NULL),
	(117,4,12,'Jessica Harris',26988,'2021-05-20',NULL),
	(118,3,12,'Shawn Rogers',20048,'2021-05-20',NULL),
	(119,2,12,'Everett Lopez',28933,'2021-05-20',NULL),
	(120,1,12,'Bertha Stewart',23261,'2021-05-20',NULL),
	(121,10,13,'Gene Lawrence',37044,'2021-05-20',NULL),
	(122,9,13,'Brett Ross',30673,'2021-05-20',NULL),
	(123,8,13,'Erik Elliott',47414,'2021-05-20',NULL),
	(124,7,13,'Frances Hoffman',33330,'2021-05-20',NULL),
	(125,6,13,'Kelly Miller',42956,'2021-05-20',NULL),
	(126,5,13,'Erin Campbell',46549,'2021-05-20',NULL),
	(127,4,13,'Russell Davis',40312,'2021-05-20',NULL),
	(128,3,13,'Gabriel Johnson',46946,'2021-05-20',NULL),
	(129,2,13,'Mathew Thompson',30476,'2021-05-20',NULL),
	(130,1,13,'Irma Sanders',42444,'2021-05-20',NULL);

--
-- Table structure for table `inventory`
--

DROP TABLE IF EXISTS inventory;
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

--
-- Table structure for table `job_position`
--

DROP TABLE IF EXISTS job_position;
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
) AUTO_INCREMENT=14;

--
-- Dumping data for table `job_position`
--

INSERT INTO job_position VALUES 
	(1,1,'Manager',48000,84000),
	(2,1,'Assistant Manager',24000,59000),
	(3,1,'Merchandiser',29000,86000),
	(4,1,'Janitor',24000,42000),
	(5,2,'Sales Associate',19000,58000),
	(6,2,'Cashier',20000,32000),
	(7,2,'Stock Clerk',27000,49000),
	(8,3,'Sales Associate',19000,58000),
	(9,3,'Cashier',20000,32000),
	(10,3,'Stock Clerk',27000,49000),
	(11,4,'Sales Associate',19000,58000),
	(12,4,'Cashier',20000,32000),
	(13,4,'Stock Clerk',27000,49000);

--
-- Table structure for table `location`
--

DROP TABLE IF EXISTS location;
CREATE TABLE location (
  location_id int NOT NULL AUTO_INCREMENT,
  manager_id int DEFAULT NULL,
  state_code varchar(2) NOT NULL,
  city varchar(25) NOT NULL,
  postal_code varchar(9) NOT NULL,
  address_line varchar(100) NOT NULL,
  PRIMARY KEY (location_id),
  UNIQUE KEY location_id (location_id),
  KEY location_ibfk_1 (manager_id),
  CONSTRAINT location_ibfk_1 FOREIGN KEY (manager_id) REFERENCES employee (employee_id)
) AUTO_INCREMENT=11;

--
-- Dumping data for table `location`
--

INSERT INTO location VALUES 
	(1,NULL,'KS','Overland Park','66210','11701 Metcalf Ave'),
	(2,NULL,'AL','Montgomery','36117','6495 Atlanta Hwy'),
	(3,NULL,'MO','Kansas City','64133','11601 E Us Highway 40'),
	(4,NULL,'AL','Mobile','36606','101 E I65 Service Rd S'),
	(5,NULL,'MO','Kansas City','64145','1701 W 133rd St'),
	(6,NULL,'DC','Washington','20001','99 H Street Nw'),
	(7,NULL,'CA','Burbank','91502','1301 N Victory Pl'),
	(8,NULL,'TX','Houston','77081','5405 South Rice Avenue'),
	(9,NULL,'FL','North Miami Beach','33162','1425 Ne 163rd St'),
	(10,NULL,'NJ','Secaucus','07094','400 Park Pl');

--
-- Table structure for table `payment`
--

DROP TABLE IF EXISTS payment;
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

--
-- Table structure for table `payment_item`
--

DROP TABLE IF EXISTS payment_item;
CREATE TABLE payment_item (
  payment_item_id int NOT NULL AUTO_INCREMENT,
  payment_id int NOT NULL,
  product_id int NOT NULL,
  quantity int NOT NULL,
  PRIMARY KEY (payment_item_id),
  UNIQUE KEY payment_item_id (payment_item_id),
  KEY payment_id (payment_id),
  KEY product_id (product_id),
  CONSTRAINT payment_item_ibfk_1 FOREIGN KEY (payment_id) REFERENCES payment (payment_id),
  CONSTRAINT payment_item_ibfk_2 FOREIGN KEY (product_id) REFERENCES product (product_id)
);

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS product;
CREATE TABLE product (
  product_id int NOT NULL AUTO_INCREMENT,
  shelf_id int NOT NULL,
  product_name varchar(100) NOT NULL,
  price decimal(10,0) NOT NULL
  brand_name varchar(100) NOT NULL,
  manufacturer_name varchar(100) NOT NULL,
  PRIMARY KEY (product_id),
  UNIQUE KEY product_id (product_id),
  UNIQUE KEY product_name_UNIQUE (product_name),
  KEY shelf_id (shelf_id),
  CONSTRAINT product_ibfk_1 FOREIGN KEY (shelf_id) REFERENCES shelf (shelf_ID)
);

--
-- Table structure for table `shelf`
--

DROP TABLE IF EXISTS shelf;
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