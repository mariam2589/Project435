"""
Module that contains functions for connecting to and managing an SQLite3 database for recording sales in an ecommerce platform.
"""

import sqlite3

def connect_to_db():
    """
    Establishes a connection to the SQLite3 database 'ecommerce_sales.db'.
    
    :return: The established connection object.
    :rtype: sqlite3.Connection
    """
    conn = sqlite3.connect('ecommerce_sales.db')
    return conn

def create_sales_table():
    """
    Creates a table named 'sales' in the SQLite3 database if it does not already exist.

    The table contains columns for sale_id, customer_id, item_id, sale_date, with foreign key constraints.
    """
    try:
        conn = connect_to_db()
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id INTEGER,
                item_id INTEGER,
                sale_date TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
                FOREIGN KEY (item_id) REFERENCES inventory(item_id)
            );
        ''')
        conn.commit()
        print("Sales table created successfully")
    except Exception as e:
        print(f"Error creating sales table: {e}")
    finally:
        conn.close()

def make_sale(customer_id, item_id):
    """
    Records a sale in the 'sales' table.

    :param customer_id: The unique identifier for the customer making the sale.
    :type customer_id: int

    :param item_id: The unique identifier for the item being sold.
    :type item_id: int

    :raises: Exception if an error occurs during the database operation.
    """
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO sales (customer_id, item_id, sale_date)
            VALUES (?, ?, datetime('now'))
        ''', (customer_id, item_id))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Error making sale: {e}")
    finally:
        conn.close()

def get_customer_sales(customer_id):
    """
    Retrieves sales made by a specific customer.

    :param customer_id: The unique identifier for the customer.
    :type customer_id: int

    :return: A list of dictionaries, where each dictionary represents a sale with sale_id, sale_date, 
             item_name, and price_per_item details.
    :rtype: list

    :raises: Exception if an error occurs during the database operation.
    """
    sales = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute('''
            SELECT sales.sale_id, sales.sale_date, inventory.name, inventory.price_per_item
            FROM sales
            JOIN inventory ON sales.item_id = inventory.item_id
            WHERE sales.customer_id = ?
        ''', (customer_id,))
        rows = cur.fetchall()

        for row in rows:
            sale = dict(row)
            sales.append(sale)

    except Exception as e:
        print(f"Error getting customer sales: {e}")
    finally:
        conn.close()

    return sales
