# PASSY V2 - Password Manager

PASSY V2 is a simple password manager application built using Python and Tkinter for the graphical user interface. It securely stores and manages your passwords in a MySQL database, with password encryption for added security.

## Features

- **Add Record:** Add new records containing the application name, URL, email ID, and password.
- **Show Records:** Display a list of all saved records with their decrypted passwords.
- **Delete Record:** Delete a record based on the application name.
- **Update Record:** Modify and save changes to an existing record.

## Getting Started

### Prerequisites

1. **Python:** Make sure you have Python installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).

2. **MySQL Database:** Set up a MySQL database with the following details:
   - Host: localhost
   - User: root
   - Password: *******
   - Database: PASSY

3. **Dependencies:** Install the required Python packages using the following command:

   ```bash
   pip install cryptography MySQL-connector-python
   ```

### Setup

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/your-password-manager.git
   cd your-password-manager
   ```

2. **Generate Encryption Key:**

   ```bash
   python your_password_manager.py
   ```

   This command generates an encryption key and saves it in a file named `secret. key`.

3. **Run the Application:**

   ```bash
   python your_password_manager.py
   ```

   This will launch the PASSY V2 password manager.

## Usage

1. **Adding a New Record:**
   - Enter the application name, URL, email ID, and password in the respective text boxes.
   - Click the "Add Record" button.

2. **Showing Records:**
   - Click the "Show Records" button to display a list of all saved records.

3. **Deleting a Record:**
   - Enter the application name you want to delete in the "Delete Record" text box.
   - Click the "Delete Record" button.

4. **Updating a Record:**
   - Enter the application name you want to update in the "Update Record" text box.
   - Click the "Update Record" button.
   - In the new window, make the necessary changes and click the "Save Record" button.

## Security Considerations

- The passwords are stored in an encrypted form using the Fernet symmetric encryption scheme from the `cryptography` library.
- Make sure to keep the `secret.key` file secure as it is used for encryption and decryption.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
