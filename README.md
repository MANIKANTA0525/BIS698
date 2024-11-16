
# Merrill Virtual Restaurant Management System

This project is a **Python-based GUI application** designed for the **Merrill Virtual Restaurant**, enabling both administrators and users to interact with the system efficiently. Built using **Tkinter** for the graphical user interface and **MySQL** for database management, the application provides separate interfaces for **Admin** and **User functionalities**.

## Features

### **Admin Interface**
- **Secure Admin Login**:
  - Predefined admin credentials for secure access.
  - Simple and intuitive login page.
  
- **Order Management**:
  - View a list of all pending orders, including:
    - `Order ID`
    - `Customer Name`
    - `Menu Item`
    - `Order Status`
  - Mark orders as "Ready for Pickup" with a single click.

- **User-Friendly Design**:
  - Color scheme: `Maroon` and `Gold` for a professional and polished look.
  - Responsive layouts for efficient navigation.

---

### **User Interface**
- **User Registration and Login**:
  - New users can register with details such as:
    - Username
    - Password
    - Email
    - Phone Number
  - Existing users can log in with their credentials.

- **Menu and Order Placement**:
  - Browse the restaurant's menu fetched dynamically from the database.
  - Select items to order after choosing a payment method (`Cash` or `Card`).
  - Real-time interaction with the database to place orders and manage payments.

- **Order Tracking**:
  - Check the status of current and previous orders:
    - Pending
    - Ready for Pickup
  - Seamless order status updates for better customer experience.

---

## Technology Stack

- **Python**: Core programming language for the application logic.
- **Tkinter**: For creating the graphical user interfaces.
- **MySQL**: Backend database to manage users, menu items, orders, and payment details.

---

## How to Run

1. Ensure you have Python and MySQL installed on your system.
2. Clone this repository to your local machine.
3. Set up the `restaurant` database using the provided SQL script (if available).
4. Update the MySQL connection details (`host`, `user`, `password`, and `database`) in the code as per your environment.
5. Run the script:
   ```bash
   python filename.py
   ```
6. Use the following credentials to explore the system:
   - **Admin Credentials**:
     - Username: `admin`
     - Password: `admin`
   - **User Credentials**:
     - Register as a new user or log in with an existing user account.

---

## Future Enhancements

- **Admin Page**:
  - Add order history and analytics dashboard.
  - Enable dynamic admin account creation and management.

- **User Page**:
  - Integrate notifications for order updates.
  - Allow users to cancel or modify orders.

- **General**:
  - Improve responsiveness for better user experience.

---
