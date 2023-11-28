
from tkinter import *
from tkinter import messagebox
import mysql.connector
from cryptography.fernet import Fernet

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

# Function to encrypt password
def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

# Function to decrypt password
def decrypt_password(encrypted_password):
    try:
        return cipher_suite.decrypt(encrypted_password).decode()
    except Exception as e:
        print(f"Error decrypting password: {e}")
        return "..."

# Function to submit a new record
def submit():
    if app_name.get() and url.get() and email_id.get() and password.get():
        encrypted_password = encrypt_password(password.get())
        insert_query = "INSERT INTO manager (app_name, url, email_id, password) VALUES (%s, %s, %s, %s)"
        data = (app_name.get(), url.get(), email_id.get(), encrypted_password)
        cursor.execute(insert_query, data)
        conn.commit()
        messagebox.showinfo("Info", "Record Added in Database!")
        clear_entries()
        query()
    else:
        messagebox.showinfo("Alert", "Please fill all details!")

# Function to display records
def query():
    query_btn.configure(text="Hide Records", command=hide)
    cursor.execute("SELECT * FROM manager")
    records = cursor.fetchall()
    display_records(records)

# Function to delete a record
def delete():
    record_id = delete_id.get()
    if record_id:
        delete_query = "DELETE FROM manager WHERE id = %s"
        data = (record_id,)
        cursor.execute(delete_query, data)
        conn.commit()
        delete_id.delete(0, END)
        messagebox.showinfo("Alert", f"Record {record_id} Deleted")
        query()
    else:
        messagebox.showinfo("Alert", "Please enter record ID to delete!")

def update():
    record_id = update_id.get()
    if record_id:
        global edit
        edit = Tk()
        edit.title("Update Record")
        edit.geometry("400x300")
        edit.minsize(400, 300)
        edit.maxsize(400, 300)

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

# Function to save updated records
def change(record_id):
    if app_name_edit.get() and url_edit.get() and email_id_edit.get() and password_edit.get():
        update_query = "UPDATE manager SET app_name = %s, url = %s, email_id = %s, password = %s WHERE id = %s"
        data = (app_name_edit.get(), url_edit.get(), email_id_edit.get(), password_edit.get(), record_id)
        cursor.execute(update_query, data)
        conn.commit()
        messagebox.showinfo("Info", "Record Updated in Database!")
        edit.destroy()
        query()
    else:
        messagebox.showinfo("Alert", "Please fill all details!")

# Function to hide records
def hide():
    query_label['text'] = ""
    query_btn.configure(text="Show Records", command=query)

# Function to clear entry fields
def clear_entries():
    app_name.delete(0, END)
    url.delete(0, END)
    email_id.delete(0, END)
    password.delete(0, END)

# Function to display records in the label
def display_records(records):
    p_records = ""
    for record in records:
        decrypted_password = decrypt_password(record[4])
        p_records += f"{record[0]} {record[1]} {record[2]} {record[3]} {decrypted_password}\n"
    query_label['text'] = p_records

# Create the main window
root = Tk()
root.title("Password Manager")
root.geometry("600x400")
root.resizable(False, False)

# Create a frame for the main content
main_frame = Frame(root, bg="#80c1ff", bd=5)
main_frame.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.8, anchor="center")

# Create text boxes
app_name = Entry(main_frame, width=30)
app_name.grid(row=0, column=1, padx=20)
url = Entry(main_frame, width=30)
url.grid(row=1, column=1, padx=20)
email_id = Entry(main_frame, width=30)
email_id.grid(row=2, column=1, padx=20)
password = Entry(main_frame, width=30)
password.grid(row=3, column=1, padx=20)
delete_id = Entry(main_frame, width=20)
delete_id.grid(row=6, column=0, padx=10, pady=5)
update_id = Entry(main_frame, width=20)
update_id.grid(row=7, column=0, padx=10, pady=5)

# Create text box labels
app_name_label = Label(main_frame, text="Application Name:")
app_name_label.grid(row=0, column=0)
url_label = Label(main_frame, text="URL:")
url_label.grid(row=1, column=0)
email_id_label = Label(main_frame, text="Email Id:")
email_id_label.grid(row=2, column=0)
password_label = Label(main_frame, text="Password:")
password_label.grid(row=3, column=0)

# Create action buttons
submit_btn = Button(main_frame, text="Add Record", command=submit)
submit_btn.grid(row=4, column=0, pady=5, padx=15, ipadx=35)

query_btn = Button(main_frame, text="Show Records", command=lambda: query())
query_btn.grid(row=4, column=1, pady=5, padx=5, ipadx=35)

delete_btn = Button(main_frame, text="Delete Record", command=delete)
delete_btn.grid(row=6, column=1, pady=5, padx=5, ipadx=30)

update_btn = Button(main_frame, text="Update Record", command=update)
update_btn.grid(row=7, column=1, pady=5, padx=5, ipadx=30)

# Create a label to show responses
query_label = Label(main_frame, anchor="nw", justify="left")
query_label.grid(row=8, column=0, columnspan=2, pady=10)

# Start the main loop
root.mainloop()



def generate_key():
    """Generates a key and save it into a file
    """
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)