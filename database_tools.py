import genai

def execute_query(sql: str) -> list[list[str]]:
    """Execute an SQL statement, returning the results."""
    print(' - DB CALL: execute_query')
    cursor = genai.db_conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    if result == []:
        genai.db_conn.commit()
    cursor.close()
    return result

def create_new_menuitem(menu_name : str, menu_description : str, price : float) -> str:
    print('Create new menu item...')
    all_menu_items = execute_query(f"select * from menuitem where menu_name = '{menu_name}'")
    if len(all_menu_items) > 0:
        return "Item already exists!"
    execute_query(f"INSERT INTO menuitem (menu_name, menu_description, price) VALUES ('{menu_name}', '{menu_description}', {price});")
    return "Menu item has been created!"

def create_new_customer(customer_name : str) -> str:
    print('Create new customer...')
    all_customers = execute_query(f"select * from customer where customer_name = '{customer_name}'")
    if len(all_customers) > 0:
       return "Customer already exists!"
    execute_query(f"INSERT INTO customer (customer_name) VALUES ('{customer_name}');")
    return "Customer has been registered!"

def create_new_order(customer_name : str, menu_items_quantity : list[list[str,str]]) -> str:
    print('Create new order...')
    all_customers = execute_query(f"select * from customer where customer_name = '{customer_name}'")
    customer_id = -1
    if len(all_customers) > 0:
        customer_id = all_customers[0][0]
    else:
        create_new_customer(customer_name)
    execute_query(f"INSERT INTO orders (customer_id) VALUES ({customer_id});")
    order_id = execute_query("SELECT * FROM orders ORDER BY id DESC LIMIT 1;")[0][0]
    for menu_item in menu_items_quantity:
        menu_item_data = execute_query(f"SELECT * FROM menuitem WHERE menu_name = '{menu_item[0]}';")
        if len(menu_item_data) == 0:
            return f"Menu item '{menu_item[0]}' does not exist!"
        menu_item_id = menu_item_data[0][0]
        item_quantity = int(menu_item[1])
        if item_quantity <= 0:
            return f"Invalid quantity for menu item '{menu_item[0]}'. Quantity must be greater than 0."
        execute_query(f"INSERT INTO orderdetails (order_id, menu_id, quantity) VALUES ({order_id}, {menu_item_id}, {menu_item[1]});")
    return f"Order has been created for customer '{customer_name}' with order ID {order_id}."

def show_all_menu_items() -> str:
    print('Show all menu items...')
    all_menu_items = execute_query("SELECT * FROM menuitem;")
    if len(all_menu_items) == 0:
        return "No menu items available."
    result = "Menu Items:\n"
    for item in all_menu_items:
        result += f"ID: {item[0]}, Name: {item[1]}, Description: {item[2]}, Price: ${item[3]:.2f}\n"
    return result

def get_menu_item_price(menu_item : str) -> str:
    print('Show that menu item price...')
    all_menu_items = execute_query(f"SELECT * FROM menuitem WHERE menu_name = '{menu_item}';")
    if len(all_menu_items) == 0:
        return f"Menu item '{menu_item}' does not exist!"
    return f"The price of '{menu_item}' is ${all_menu_items[0][3]:.2f}."

db_tools = [create_new_menuitem, create_new_customer, create_new_order, show_all_menu_items, get_menu_item_price]