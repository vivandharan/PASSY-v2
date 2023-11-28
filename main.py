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
    try:
        return cipher_suite.decrypt(encrypted_password).decode()
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return "Decryption Error"

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


# Create a function to delete a record
def delete():
    t = delete_id.get()
    if t:
        delete_query = "DELETE FROM manager WHERE id = %s"
        data = (t,)
        cursor.execute(delete_query, data)
        conn.commit()
        delete_id.delete(0, END)
        messagebox.showinfo("Alert", f"Record {t} Deleted")
    else:
        messagebox.showinfo("Alert", "Please enter record ID to delete!")

# Create a function to update a record
def update():
    t = update_id.get()
    if t:
        global edit
        edit = Tk()
        edit.title("Update Record")
        edit.geometry("500x400")
        edit.minsize(450, 300)
        edit.maxsize(450, 300)

        # Global variables
        global app_name_edit, url_edit, email_id_edit, password_edit

        # Create text boxes
        app_name_edit = Entry(edit, width=30)
        app_name_edit.grid(row=0, column=1, padx=20)
        url_edit = Entry(edit, width=30)
        url_edit.grid(row=1, column=1, padx=20)
        email_id_edit = Entry(edit, width=30)
        email_id_edit.grid(row=2, column=1, padx=20)
        password_edit = Entry(edit, width=30)
        password_edit.grid(row=3, column=1, padx=20)

        # Create text box labels
        app_name_label_edit = Label(edit, text="Application Name:")
        app_name_label_edit.grid(row=0, column=0)
        url_label_edit = Label(edit, text="URL:")
        url_label_edit.grid(row=1, column=0)
        email_id_label_edit = Label(edit, text="Email Id:")
        email_id_label_edit.grid(row=2, column=0)
        password_label_edit = Label(edit, text="Password:")
        password_label_edit.grid(row=3, column=0)

        # Create save button
        submit_btn_edit = Button(edit, text="Save Record", command=change)
        submit_btn_edit.grid(row=4, column=0, columnspan=2, pady=5, padx=15, ipadx=135)

        # Query the MySQL table
        select_query = "SELECT * FROM manager WHERE id = %s"
        data = (t,)
        cursor.execute(select_query, data)
        record = cursor.fetchone()

        app_name_edit.insert(0, record[1])
        url_edit.insert(0, record[2])
        email_id_edit.insert(0, record[3])
        password_edit.insert(0, record[4])

# Create a function to save updated records
def change():
    if app_name_edit.get() and url_edit.get() and email_id_edit.get() and password_edit.get():
        update_query = "UPDATE manager SET app_name = %s, url = %s, email_id = %s, password = %s WHERE id = %s"
        data = (app_name_edit.get(), url_edit.get(), email_id_edit.get(), password_edit.get(), update_id.get())
        cursor.execute(update_query, data)
        conn.commit()
        messagebox.showinfo("Info", "Record Updated in Database!")
        update_id.delete(0, END)
        edit.destroy()
    else:
        messagebox.showinfo("Alert", "Please fill all details!")

# Create a function to hide records
def hide():
    query_label['text'] = ""
    query_btn.configure(text="Show Records", command=query)

# Create text boxes
app_name = Entry(root, width=30)
app_name.grid(row=0, column=1, padx=20)
url = Entry(root, width=30)
url.grid(row=1, column=1, padx=20)
email_id = Entry(root, width=30)
email_id.grid(row=2, column=1, padx=20)
password = Entry(root, width=30)
password.grid(row=3, column=1, padx=20)
delete_id = Entry(root, width=20)
delete_id.grid(row=6, column=1, padx=20)
update_id = Entry(root, width=20)
update_id.grid(row=7, column=1, padx=20)

# Create text box labels
app_name_label = Label(root, text="Application Name:")
app_name_label.grid(row=0, column=0)
url_label = Label(root, text="URL:")
url_label.grid(row=1, column=0)
email_id_label = Label(root, text="Email Id:")
email_id_label.grid(row=2, column=0)
password_label = Label(root, text="Password:")
password_label.grid(row=3, column=0)

# Create submit button
submit_btn = Button(root, text="Add Record", command=submit)
submit_btn.grid(row=5, column=0, pady=5, padx=15, ipadx=35)

# Create a query button
query_btn = Button(root, text="Show Records", command=query)
query_btn.grid(row=5, column=1, pady=5, padx=5, ipadx=35)

# Create a delete button
delete_btn = Button(root, text="Delete Record", command=delete)
delete_btn.grid(row=6, column=0, ipadx=30)

# Create an update button
update_btn = Button(root, text="Update Record", command=update)
update_btn.grid(row=7, column=0, ipadx=30)

# Create a label to show responses
query_label = Label(frame, anchor="nw", justify="left")
query_label.place(relwidth=1, relheight=1)

def main():
    root.mainloop()

if __name__ == '__main__':
    root.mainloop()