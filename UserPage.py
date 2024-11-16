import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import messagebox

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

# Step 2: User Registration and Login - Tkinter UI
def register_user():
    username = entry_username.get()
    password = entry_password.get()
    email = entry_email.get()
    phone_number = entry_phone.get()
    if not username or not password or not email or not phone_number:
        messagebox.showerror("Error", "All fields are required!")
        return
    
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO Users (username, password, email, phone_number, user_role) VALUES (%s, %s, %s, %s, %s)",
                       (username, password, email, phone_number, 'user'))  # Assuming user role is 'user'
        conn.commit()
        messagebox.showinfo("Success", "Registration successful!")
        clear_fields()
    except Error as e:
        messagebox.showerror("Error", f"Error: {e}")
    finally:
        conn.close()

def login_user():
    username = entry_username1.get()
    password = entry_password1.get()
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Users WHERE username = %s AND password = %s", (username, password))
    user = cursor.fetchone()
    if user:
        open_user_dashboard(user[0])
    else:
        messagebox.showerror("Error", "Invalid credentials!")
    conn.close()

def open_user_dashboard(user_id):
    dashboard = tk.Toplevel()
    dashboard.title("User Dashboard")
    tk.Button(dashboard, text="View Menu", command=lambda: view_menu(user_id)).grid(row=0, column=0, pady=10)
    tk.Button(dashboard, text="Check Order Status", command=lambda: view_order_status(user_id)).grid(row=1, column=0, pady=10)

def view_menu(user_id):
    # Create a new window for the menu
    menu_window = tk.Toplevel()
    menu_window.title("Menu")
    
    # Variable to store the selected payment method
    payment_method = tk.StringVar()
    payment_method.set("none")  # Default value for payment method (none selected)
    
    # Function to enable order buttons when a payment method is selected
    def enable_order_buttons():
        if payment_method.get() != "none":
            for button in order_buttons:
                button.config(state=tk.NORMAL)  # Enable all order buttons
        else:
            for button in order_buttons:
                button.config(state=tk.DISABLED)  # Disable all order buttons

    # Radio buttons for selecting payment method
    tk.Label(menu_window, text="Select Payment Method:").grid(row=0, column=0, pady=10)
    
    tk.Radiobutton(menu_window, text="Cash", variable=payment_method, value="cash", command=enable_order_buttons).grid(row=1, column=0, pady=5)
    tk.Radiobutton(menu_window, text="Card", variable=payment_method, value="card", command=enable_order_buttons).grid(row=2, column=0, pady=5)
    
    # Fetch menu items from the database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM menu")
    menu_items = cursor.fetchall()

    # Create a list to store the order buttons so we can enable/disable them
    order_buttons = []

    # Display each menu item and create an order button for each
    row = 3
    for item in menu_items:
        tk.Label(menu_window, text=f"{item[1]} - {item[3]}$").grid(row=row, column=0, pady=5)
        # Create an "Order" button but disable it initially
        order_button = tk.Button(menu_window, text="Order", state=tk.DISABLED, 
                                 command=lambda item_id=item[0]: place_order(user_id, item_id,payment_method.get(), item[3]))
        order_button.grid(row=row, column=1, pady=5)
        
        # Add the button to the order_buttons list
        order_buttons.append(order_button)
        row += 1

    conn.close()

def place_order(user_id, item_id,payment_method,amount):
    print("payment_method.get()",user_id, item_id,payment_method)
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO orders (user_id, item_id) VALUES (%s, %s)", (user_id, item_id))
    cursor.execute("INSERT INTO Payments (amount_paid, payment_method,payment_status) VALUES (%s, %s, %s)", (amount, payment_method,'successful'))
    conn.commit()
    messagebox.showinfo("Success", "Order placed successfully!")
    conn.close()

# Step 4: Check Order Status for User
def view_order_status(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT orders.order_id, menu.item_name, orders.status 
                      FROM orders 
                      JOIN menu ON orders.item_id = menu.item_id 
                      WHERE orders.user_id = %s''', (user_id, ))
    orders = cursor.fetchall()
    status_window = tk.Toplevel()
    status_window.title("Order Status")
    row = 0
    for order in orders:
        tk.Label(status_window, text=f"Order ID: {order[0]}, Item: {order[1]}, Status: {order[2]}").grid(row=row, column=0, pady=5)
        row += 1
    conn.close()

# Step 3: Toggle between Register and Login forms
def show_register_form():
    login_frame.grid_forget()
    register_frame.grid(row=1, column=1, padx=10, pady=10)

def show_login_form():
    register_frame.grid_forget()
    login_frame.grid(row=1, column=1, padx=10, pady=10)

def clear_fields():
    entry_username.delete(0, tk.END)
    entry_password.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_phone.delete(0, tk.END)

# Main Application Window
app = tk.Tk()
app.title("Merrill Virtual Restaurant")
app.geometry("800x600") 
app.config(bg="maroon")  # Set the background color to maroon

# Configure grid to fill the entire window
app.grid_rowconfigure(0, weight=1)
app.grid_rowconfigure(1, weight=1)
app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)

# Register Form Frame
register_frame = tk.Frame(app, bg="maroon")  # Set background of the frame
register_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Username Label and Entry side by side
tk.Label(register_frame, text="Username", bg="maroon", fg="gold").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_username = tk.Entry(register_frame, bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_username.grid(row=0, column=1, padx=10, pady=5)

# Password Label and Entry side by side
tk.Label(register_frame, text="Password", bg="maroon", fg="gold").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_password = tk.Entry(register_frame, show="*", bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_password.grid(row=1, column=1, padx=10, pady=5)

# Email Label and Entry side by side
tk.Label(register_frame, text="Email", bg="maroon", fg="gold").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_email = tk.Entry(register_frame, bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_email.grid(row=2, column=1, padx=10, pady=5)

# Phone Number Label and Entry side by side
tk.Label(register_frame, text="Phone Number", bg="maroon", fg="gold").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_phone = tk.Entry(register_frame, bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_phone.grid(row=3, column=1, padx=10, pady=5)

# Register Button
tk.Button(register_frame, text="Register", command=register_user, bg="gold", fg="maroon", font=("Arial", 12), bd=2).grid(row=4, column=0, columnspan=2, pady=10)

# Back to Login Button
tk.Button(register_frame, text="Back to Login", command=show_login_form, bg="gold", fg="maroon", font=("Arial", 12), bd=2).grid(row=5, column=0, columnspan=2, pady=5)

# Login Form Frame
login_frame = tk.Frame(app, bg="maroon")  # Set background of the frame
login_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

# Title Label
title_label = tk.Label(login_frame, text="Merrill Virtual Restaurant", bg="maroon", fg="gold", font=("Arial", 20, "bold"))
title_label.grid(row=0, column=0, columnspan=2, pady=20)

# Username Label and Entry side by side
tk.Label(login_frame, text="Username", bg="maroon", fg="gold").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_username1 = tk.Entry(login_frame, bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_username1.grid(row=1, column=1, padx=10, pady=5)

# Password Label and Entry side by side
tk.Label(login_frame, text="Password", bg="maroon", fg="gold").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_password1 = tk.Entry(login_frame, show="*", bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_password1.grid(row=2, column=1, padx=10, pady=5)

# Login Button
tk.Button(login_frame, text="Login", command=login_user, bg="gold", fg="maroon", font=("Arial", 12), bd=2).grid(row=3, column=0, columnspan=2, pady=10)

# Register Button
tk.Button(login_frame, text="Don't have an account? Register", command=show_register_form, bg="gold", fg="maroon", font=("Arial", 12), bd=2).grid(row=4, column=0, columnspan=2, pady=5)

# Start with the login form
show_login_form()

# Run the application
app.mainloop()
