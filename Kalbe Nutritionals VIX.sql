CREATE DATABASE kalbe;
USE kalbe;

CREATE TABLE customer (
CustomerID VARCHAR(20) NOT NULL,
Age INT,
Gender TINYINT(1),
MaritalStatus VARCHAR(30),
Income INT,
primary key (CustomerID));

CREATE TABLE store (
StoreID VARCHAR(20) NOT NULL,
StoreName VARCHAR(100),
GroupStore VARCHAR (100),
Type VARCHAR(20),
Latitude decimal(12,9),
Longitude decimal(12,9),
primary key (StoreID));

CREATE TABLE product (
ProductID VARCHAR(20) NOT NULL,
ProductName VARCHAR(100),
Price INT,
primary key (ProductID));

SELECT * FROM customer;
SELECT * FROM store;
SELECT * FROM product;

CREATE TABLE transaction (
TransactionID VARCHAR(50) NOT NULL,
CustomerID VARCHAR(50) NOT NULL,
Date VARCHAR(50),
ProductID VARCHAR(50) NOT NULL,
Price INT,
Qty INT,
TotalAmount INT,
StoreID VARCHAR(50) NOT NULL);

ALTER TABLE transaction ADD CONSTRAINT FOREIGN KEY (CustomerID) REFERENCES customer (CustomerID);
ALTER TABLE transaction ADD CONSTRAINT FOREIGN KEY (ProductID) REFERENCES product (ProductID);
ALTER TABLE transaction ADD CONSTRAINT FOREIGN KEY (StoreID) REFERENCES store (StoreID);

SET GLOBAL local_infile = 1;
SHOW VARIABLES LIKE 'local_infile';

LOAD DATA LOCAL INFILE 'C:\\ProgramData\\MySQL\\MySQL Server 8.0\\Uploads\\Transaction.csv'
INTO TABLE transaction COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SET sql_safe_updates = 0 ;

UPDATE transaction SET Date = STR_TO_DATE(Date, '%d/%m/%Y');

SELECT * FROM transaction;

SELECT MaritalStatus, AVG(Age) AS Average_Age
FROM customer
GROUP BY MaritalStatus;

SELECT
CASE
	WHEN Gender = 0 THEN 'Female'
	WHEN Gender = 1 THEN 'Male'
		ELSE 'OTHER'
	END AS Gender, ROUND(AVG(Age)) AS Average_Age
FROM customer
WHERE Gender IS NOT NULL
GROUP BY Gender;

SELECT transaction.StoreID, store.StoreName, SUM(transaction.Qty) AS Total_Qty
FROM transaction
LEFT JOIN store ON transaction.StoreID=store.StoreID
GROUP BY StoreID, StoreName
ORDER BY Total_Qty DESC;

SELECT transaction.ProductID, product.ProductName, SUM(transaction.TotalAmount) AS Total_Amount, SUM(transaction.Qty) AS Total_Qty
FROM transaction
LEFT JOIN product ON transaction.ProductID=product.ProductID
GROUP BY ProductID, ProductName
ORDER BY Total_Amount DESC;

SELECT
	transaction.TransactionID,
    transaction.Date,
    transaction.CustomerID,
    customer.Age,
    customer.Gender,
    customer.MaritalStatus,
    customer.Income,
    transaction.ProductID,
    product.ProductName,
    transaction.Price,
    transaction.Qty,
    transaction.TotalAmount,
    transaction.StoreID,
    store.StoreName,
    store.GroupStore,
    store.Type,
    store.Latitude,
    store.Longitude
    
FROM transaction
	LEFT JOIN customer ON customer.CustomerID = transaction.CustomerID
    LEFT JOIN product ON product.ProductID = transaction.ProductID
	LEFT JOIN store ON store.StoreID = transaction.StoreID
ORDER BY transaction.Date;