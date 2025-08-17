import google.generativeai as genai
import os
import sqlite3
import database_tools as db_tools
from google.api_core import retry

db_conn = None
retry_policy = None
tools = db_tools.db_tools
model = None
chat_model = None

instructions = """You are a assistant handling customer queries for drive through ordering. Using the provided tools, you are to help guide the user perform a purchase.
You are to use the following step by step guide when aiding user in a purchase:
- Retrieve their customer id using their name from the database. If not, kindly register them using the tools available
- Provide the user with the restaurant menu. You may suggest menu for the user to order.
- Take note of user orders. Ensure that you ask the user if they would like to add more menus until they are satisfied
- Submit user order using `create_new_order` tool and instruct the user to wait 10-15 minutes for their order.
"""

def initialize():
    global db_conn, retry_policy, model, chat_model
    my_api_key = API_KEY
    os.environ["GOOGLE_API_KEY"] = my_api_key
    genai.configure(api_key=my_api_key)
    db_file = "sample.db"
    db_conn = sqlite3.connect(db_file, check_same_thread=False)
    model = genai.GenerativeModel("models/gemini-1.5-flash-latest", tools=db_tools.db_tools, system_instruction=instructions)
    retry_policy = {"retry": retry.Retry(predicate=retry.if_transient_error)}
    chat_model = model.start_chat(enable_automatic_function_calling=True)
    create_database()

def create_database():
    drop_all_tables()
    create_menuitem_database()
    create_customer_database()
    create_orders_database()
    create_orderdetails_database()
    insert_default_menuitem()
    insert_default_customer()

def drop_all_tables():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS menuitem;")
    cursor.execute("DROP TABLE IF EXISTS orders;")
    cursor.execute("DROP TABLE IF EXISTS orderdetails;")
    cursor.execute("DROP TABLE IF EXISTS customer;")
    db_conn.commit()
    cursor.close()

def create_menuitem_database():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS menuitem (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        menu_name VARCHAR(255) NOT NULL,
        menu_description VARCHAR(255) NOT NULL,
        price DECIMAL(10, 2) NOT NULL
    );
    """)
    cursor.close()
    db_conn.commit()

def create_orders_database():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_datetime DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
        customer_id INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customer(id)
    );
    """)
    cursor.close()
    db_conn.commit()

def create_orderdetails_database():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS orderdetails (
        order_id INTEGER NOT NULL,
        menu_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        PRIMARY KEY (order_id, menu_id),
        FOREIGN KEY (order_id) REFERENCES orders(id),
        FOREIGN KEY (menu_id) REFERENCES menuitem(id)
    );
    """)
    cursor.close()
    db_conn.commit()

def create_customer_database():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name VARCHAR(255) NOT NULL DEFAULT "anonymous"
    );
    """)
    cursor.close()
    db_conn.commit()

def insert_default_menuitem():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    INSERT INTO menuitem (menu_name, menu_description, price) VALUES
        ('Beef Burger', "Delicious burger with meat" , 12.99),
        ('Cheese Burger', "Delicious burger with meat and cheese" , 13.99),
        ('Deluxe Burger', "Delicious burger with meat, cheese, lettuce, and tomato" , 16.99),
        ('French Fries', "Fried chips and salted" , 4.99),
        ('Coca Cola', "Cola drink" , 2.99),
        ('Milkshake', "Sweet and delicious drink" , 29.99);
""")
    cursor.close()
    db_conn.commit()

def insert_default_customer():
    global db_conn
    cursor = db_conn.cursor()
    cursor.execute("""
    INSERT INTO customer (customer_name) VALUES
        ('David Lee'),
        ('Emily Chen'),
        ('Frank Brown'),
        ('anonymous');
""")
    cursor.close()
    db_conn.commit()

def chat(prompt):
    return chat_model.send_message(prompt, request_options=retry_policy).text