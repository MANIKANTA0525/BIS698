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

def admin_login():
    username = entry_username.get()
    password = entry_password.get()
    if username == "admin" and password == "admin":  # Example credentials for admin login
        open_admin_dashboard()
    else:
        messagebox.showerror("Error", "Invalid admin credentials!")

def open_admin_dashboard():
    admin_dashboard = tk.Toplevel()
    admin_dashboard.title("Admin Dashboard")
    tk.Button(admin_dashboard, text="View All Orders", command=view_orders_admin, bg="gold", fg="maroon", font=("Arial", 12), bd=2).pack(pady=5)

def view_orders_admin():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''SELECT orders.order_id, users.username, menu.item_name, orders.status 
                      FROM orders 
                      JOIN users ON orders.user_id = users.user_id 
                      JOIN menu ON orders.item_id = menu.item_id
                      WHERE orders.status = 'Pending';
                   ''')
    orders = cursor.fetchall()
    admin_window = tk.Toplevel()
    admin_window.title("Admin - View Orders")
    for order in orders:
        order_info = f"Order ID: {order[0]}, User: {order[1]}, Item: {order[2]}, Status: {order[3]}"
        tk.Label(admin_window, text=order_info, bg="maroon", fg="gold", font=("Arial", 12)).pack()
        tk.Button(admin_window, text="Mark as Ready", command=lambda order_id=order[0]: update_order_status(order_id), bg="gold", fg="maroon", font=("Arial", 12), bd=2).pack(pady=2)
    conn.close()

def update_order_status(order_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = 'Ready for Pickup' WHERE order_id = %s", (order_id,))
    conn.commit()
    messagebox.showinfo("Success", f"Order {order_id} marked as ready!")
    conn.close()

# Main Application Window
app = tk.Tk()
app.title("Merrill Virtual Restaurant")
app.geometry("300x400")
app.config(bg="maroon")  # Set the background color to maroon
app.eval('tk::PlaceWindow . center')  # Center the window on screen

# Login Form Frame
login_frame = tk.Frame(app, bg="maroon")  # Set background of the frame
login_frame.pack(pady=20)

# Username Label and Entry side by side
tk.Label(login_frame, text="Username", bg="maroon", fg="gold", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(login_frame, bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_username.pack(pady=5)

# Password Label and Entry side by side
tk.Label(login_frame, text="Password", bg="maroon", fg="gold", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(login_frame, show="*", bg="gold", fg="maroon", bd=2, font=("Arial", 12))
entry_password.pack(pady=5)

# Admin Login Button
tk.Button(login_frame, text="Admin Login", command=admin_login, bg="gold", fg="maroon", font=("Arial", 12), bd=2).pack(pady=20)

app.mainloop()
