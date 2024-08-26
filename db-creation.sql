CREATE DATABASE IF NOT EXISTS telepizza_db;

USE telepizza_db;

CREATE TABLE
    IF NOT EXISTS products (
        product_id INT AUTO_INCREMENT PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL,
        category VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL,
        size VARCHAR(255) NOT NULL
    );

CREATE TABLE
    IF NOT EXISTS orders (
        order_id INT AUTO_INCREMENT PRIMARY KEY,
        product_id INT,
        order_date DATETIME NOT NULL,
        quantity INT NOT NULL,
        customer_name VARCHAR(255) NOT NULL,
        delivery_address VARCHAR(255) NOT NULL,
        FOREIGN KEY (product_id) REFERENCES products (product_id) ON DELETE CASCADE
    );