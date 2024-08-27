import streamlit as st
import mysql.connector
from mysql.connector import Error

# Function to create database connection
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='telepizza_db',
            user='root',
            password=''
        )
        if connection.is_connected():
            return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Function to insert a new product
def insert_product(product_name, category, price, size):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO products (product_name, category, price, size) 
                    VALUES (%s, %s, %s, %s)"""
            values = (product_name, category, price, size)
            cursor.execute(query, values)
            connection.commit()
            st.success("Product created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Streamlit UI
st.title("Create New Product")

product_name = st.text_input("Product Name")
category = st.selectbox("Category", ["Pizza", "Drink", "Side", "Dessert"])
price = st.number_input("Price", min_value=0.01, step=0.01, format="%.2f")
size = st.selectbox("Size", ["Small", "Medium", "Large"])

if st.button("Create Product"):
    if product_name and category and price and size:
        insert_product(product_name, category, price, size)
    else:
        st.warning("Please fill in all fields.")