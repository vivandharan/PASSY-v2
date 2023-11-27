# PASSY-v2
import sys
from tkinter import *
from cryptography.fernet import Fernet
import mysql.connector
from tkinter import messagebox

# Create a MySQL connection
conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="Qwerty772",
    database="PASSY"
)
cursor = conn.cursor()

# Generate a key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)

root = Tk()
root.title("Password Manager")
root.geometry("500x400")
root.minsize(600, 400)
root.maxsize(600, 400)

frame = Frame(root, bg="#80c1ff", bd=5)
frame.place(relx=0.50, rely=0.50, relwidth=0.98, relheight=0.45, anchor="n")

# Create a MySQL table
cursor.execute("""CREATE TABLE IF NOT EXISTS manager (
                       id INT AUTO_INCREMENT PRIMARY KEY,
                       app_name VARCHAR(255),
                       url VARCHAR(255),
                       email_id VARCHAR(255),
                       password VARBINARY(255)
                        )
""")

# Commit changes
conn.commit()

# Encryption function
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

# Decryption function
def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

# Create submit function for the database
def submit():
    # Insert into the MySQL table
    if app_name.get() and url.get() and email_id.get() and password.get():
        encrypted_password = encrypt_password(password.get())
        insert_query = "INSERT INTO manager (app_name, url, email_id, password) VALUES (%s, %s, %s, %s)"
        data = (app_name.get(), url.get(), email_id.get(), encrypted_password)
        cursor.execute(insert_query, data)
        conn.commit()
        # Message box
        messagebox.showinfo("Info", "Record Added in Database!")

        # After data entry, clear the text boxes
        app_name.delete(0, END)
        url.delete(0, END)
        email_id.delete(0, END)
        password.delete(0, END)
    else:
        messagebox.showinfo("Alert", "Please fill all details!")

# Create a query function
def query():
    query_btn.configure(text="Hide Records", command=hide)
    # Query the MySQL table
    cursor.execute("SELECT * FROM manager")
    records = cursor.fetchall()
    p_records = ""
    for record in records:
        decrypted_password = decrypt_password(record[4])
        p_records += f"{record[0]} {record[1]} {record[2]} {record[3]} {decrypted_password}\n"
    query_label['text'] = p_records

# Rest of your code remains unchanged...
