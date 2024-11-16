import mysql.connector
from mysql.connector import Error

# Function to create the necessary tables and insert initial data

# Step 1: Database Setup - SQL Queries
def create_connection():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="restaurant"
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error: '{e}' occurred")
        return None
    
def setup_database():
    conn = create_connection()
    cursor = conn.cursor()

    # Drop existing tables to avoid conflicts
    cursor.execute("DROP TABLE IF EXISTS Payments;")
    cursor.execute("DROP TABLE IF EXISTS Order_Items;")
    cursor.execute("DROP TABLE IF EXISTS Orders;")
    cursor.execute("DROP TABLE IF EXISTS Menu;")
    cursor.execute("DROP TABLE IF EXISTS Category;")
    cursor.execute("DROP TABLE IF EXISTS Users;")
    
    # Users Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Users (
                        user_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        username NVARCHAR(50) NOT NULL,
                        password NVARCHAR(50) NOT NULL,
                        email NVARCHAR(100),
                        phone_number VARCHAR(15),
                        user_role VARCHAR(50) DEFAULT 'user'
                    )''')
    
    # Category Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Category (
                        category_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        category_name NVARCHAR(50) NOT NULL
                    )''')
    
    # Menu Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Menu (
                        item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        item_name NVARCHAR(50) NOT NULL,
                        category_id BIGINT,
                        price VARCHAR(50),
                        FOREIGN KEY (category_id) REFERENCES Category(category_id)
                    )''')
    
    # Orders Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        order_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        user_id BIGINT,
                        item_id BIGINT,
                        total_price VARCHAR(50),
                        status VARCHAR(20) DEFAULT 'Pending',
                        FOREIGN KEY (user_id) REFERENCES Users(user_id)
                    )''')
    
    # Order_Items Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Order_Items (
                        order_item_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        order_id BIGINT,
                        item_id BIGINT,
                        quantities BIGINT,
                        each_price VARCHAR(50),
                        FOREIGN KEY (order_id) REFERENCES Orders(order_id),
                        FOREIGN KEY (item_id) REFERENCES Menu(item_id)
                    )''')
    
    # Payments Table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Payments (
                        payment_id BIGINT AUTO_INCREMENT PRIMARY KEY,
                        order_id BIGINT,
                        amount_paid BIGINT,
                        payment_method NVARCHAR(50),
                        payment_status NVARCHAR(50),
                        FOREIGN KEY (order_id) REFERENCES Orders(order_id)
                    )''')
    
    # Insert initial data into Category table
    cursor.execute("INSERT INTO Category (category_id, category_name) VALUES ('9283287649', 'Appetizers');")
    cursor.execute("INSERT INTO Category (category_id, category_name) VALUES ('7484838330', 'Deserts');")
    cursor.execute("INSERT INTO Category (category_id, category_name) VALUES ('9347031003', 'Main Course');")
    cursor.execute("INSERT INTO Category (category_id, category_name) VALUES ('4457091146', 'Beverages');")
    
    # Insert initial data into Menu table
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('3710457831', 'Double smash burger', '9347031003', '12');")
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('2054678740', 'Omlet bar', '9347031003', '10');")
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('4428888732', 'Cheese pizza', '9347031003', '10');")
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('4631111267', 'Pepperoni pizza', '9347031003', '15');")
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('9144803265', 'Chicken tenders', '9347031003', '20');")
    cursor.execute("INSERT INTO Menu (item_id, item_name, category_id, price) VALUES ('8295903675', 'Grilled chicken alfredo', '9347031003', '13');")

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Initialize the database
setup_database()
