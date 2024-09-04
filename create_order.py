import streamlit as st
import mysql.connector
import pandas as pd
from mysql.connector import Error
import openpyxl
from openpyxl import load_workbook

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
            query = "SELECT * FROM products"  # Select all columns
            df = pd.read_sql(query, connection)
            return df
        except Error as e:
            st.error(f"Error: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    return pd.DataFrame()

# New function to update Excel file
def update_excel_file(order_id, product_id, order_date, quantity, customer_name, delivery_address, total_price):
    try:
        wb = load_workbook('orders.xlsx')
        ws = wb.active
        new_row = [order_id, product_id, order_date, quantity, customer_name, delivery_address, total_price]
        ws.append(new_row)
        wb.save('orders.xlsx')
        st.success("Excel file updated successfully!")
    except Exception as e:
        st.error(f"Error updating Excel file: {e}")

# Modify the insert_order function
def insert_order(customer_name, product_id, quantity, total_price, delivery_address):
    connection = create_connection()
    
    if connection:
        try:
            cursor = connection.cursor()
            query = """INSERT INTO orders (customer_name, product_id, quantity, total_price, delivery_address) 
                    VALUES (%s, %s, %s, %s, %s)"""
            values = (customer_name, int(product_id), int(quantity), float(total_price), delivery_address)
            cursor.execute(query, values)
            connection.commit()
            
            # Get the last inserted order ID
            order_id = cursor.lastrowid
            
            # Get the current date
            order_date = pd.Timestamp.now().strftime('%Y-%m-%d')
            
            # Update Excel file
            update_excel_file(order_id, product_id, order_date, quantity, customer_name, delivery_address, total_price)
            
            st.success("Order created successfully and Excel file updated!")
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

# Add delivery address input
delivery_address = st.text_input("Delivery Address")

if st.button("Create Order"):
    if customer_name and product and quantity and delivery_address:
        product_id = products_df[products_df['product_name'] == product].iloc[0].name
        insert_order(customer_name, product_id, quantity, total_price, delivery_address)
    else:
        st.warning("Please fill in all fields.")
