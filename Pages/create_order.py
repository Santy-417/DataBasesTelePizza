import streamlit as st
import mysql.connector
import pandas as pd
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

# Function to get products from database
def get_products():
    connection = create_connection()
    if connection:
        try:
            query = "SELECT * FROM products"
            df = pd.read_sql(query, connection)
            return df
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    return pd.DataFrame()

# Function to insert a new order
def insert_order(customer_name, product_id, quantity, total_price):
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO orders (customer_name, product_id, quantity, total_price) 
                    VALUES (%s, %s, %s, %s)"""
            values = (customer_name, product_id, quantity, total_price)
            cursor.execute(query, values)
            connection.commit()
            st.success("Order created successfully!")
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

# Load product data
products_df = get_products()

# Streamlit UI
st.title("Create New Order")

customer_name = st.text_input("Customer Name")
product = st.selectbox("Select Product", products_df['product_name'].tolist())
quantity = st.number_input("Quantity", min_value=1, step=1)

if product:
    product_price = products_df[products_df['product_name'] == product]['price'].values[0]
    total_price = quantity * product_price
    st.write(f"Total Price: ${total_price:.2f}")

if st.button("Create Order"):
    if customer_name and product and quantity:
        product_id = products_df[products_df['product_name'] == product]['id'].values[0]
        insert_order(customer_name, product_id, quantity, total_price)
    else:
        st.warning("Please fill in all fields.")
