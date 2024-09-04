import os
import streamlit as st
import mysql.connector
from mysql.connector import Error

st.title("Create New Product")

product_name = st.text_input("Product Name")
category = st.selectbox("Category", ["Pizza", "Drink", "Side", "Dessert"])
price = st.number_input("Price", min_value=0.01, step=0.01, format="%.2f")
size = st.selectbox("Size", ["Small", "Medium", "Large"])

submit = st.button("Create Product")

if submit:
    if product_name and category and price and size:
        st.write(f"Product name is: {product_name}")
        st.write(f"Database name: {os.getenv('DB_NAME')}")
        try:
            connection = mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME")
            )
            if connection.is_connected():
                cursor = connection.cursor(dictionary=True)
                query = """
                INSERT INTO products (product_name, category, price, size)
                VALUES (%s, %s, %s, %s)
                """
                values = (product_name, category, price, size)

                cursor.execute(query, values)
                connection.commit()

                cursor.close()

                st.success("The product has been successfully saved")

        except Error as e:
            st.error(f"Error connecting to database: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
    else:
        st.warning("Please fill in all fields.")