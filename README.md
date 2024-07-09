
# Password Manager

The password manager application is designed to store (locally) and manage passwords for various online services or accounts. It provides a graphical user interface (GUI) using the tkinter library in Python, allowing users to interact with their stored passwords.


## Documentation

Imports and Constants



```bash
import tkinter as tk
from tkinter import simpledialog, messagebox
import os
import json

```
- **tkinter:** GUI toolkit for Python.

- **simpledialog, messagebox:** Modules from tkinter for dialog boxes and message boxes.

- **os, json:** Standard Python libraries for file operations and JSON handling.

- **PASSWORD_FILE:** Constant storing the filename where passwords will be saved (passwords.json).

**Functions**

'load_passwords()'
```
def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    try:
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading passwords: {e}")
        return {}
```
- **Purpose:** Loads passwords from the JSON file.
- **Behavior:** 
    - Checks if the PASSWORD_FILE exists.
    - If exists, reads and returns the JSON content.
    - Catches and prints any exceptions that occur during file reading.

'save_passwords(passwords)'
```
def save_passwords(passwords):
    try:
        with open(PASSWORD_FILE, 'w') as file:
            json.dump(passwords, file, indent=4)
    except Exception as e:
        print(f"Error saving passwords: {e}")

```
- **Purpose:** Saves passwords to the JSON file.
- **Parameters:** passwords (dictionary) - Passwords to be saved.
- **Behavior:**
    - Writes passwords dictionary to the PASSWORD_FILE in JSON format.
    - Uses indent=4 for pretty-printing JSON for better readability.
    - Catches and prints any exceptions that occur during file writing.
'add_password(service, username, password)'
```
def add_password(service, username, password):
    passwords = load_passwords()
    if service not in passwords:
        passwords[service] = []
    passwords[service].append({"username": username, "password": password})
    save_passwords(passwords)
    print("Password added!")
```
- **Purpose:** Adds a new password entry.
- **Parameters:** service (str), username (str), password (str) - Details of the password to be added.
- **Behavior:**
    - Loads existing passwords.
    - Adds the new password entry to the passwords dictionary.
    - Saves the updated passwords back to the JSON file.
    - Prints a message confirming the addition.
'add_password_ui()'
```
def add_password_ui():
    dialog = tk.Toplevel(root)
    dialog.title("Add Password")

    service_var = tk.StringVar()
    username_var = tk.StringVar()
    password_var = tk.StringVar()

    def add_and_close():
        service = service_var.get()
        username = username_var.get()
        password = password_var.get()

        if service.strip() and username.strip() and password.strip():
            add_password(service, username, password)
            messagebox.showinfo("Success", "Password added!")
            refresh_service_list()
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Please enter Service, Username, and Password.")

    tk.Label(dialog, text="Service:").grid(row=0, column=0, sticky='w', padx=10, pady=5)
    tk.Entry(dialog, textvariable=service_var).grid(row=0, column=1, padx=10, pady=5)

    tk.Label(dialog, text="Username:").grid(row=1, column=0, sticky='w', padx=10, pady=5)
    tk.Entry(dialog, textvariable=username_var).grid(row=1, column=1, padx=10, pady=5)

    tk.Label(dialog, text="Password:").grid(row=2, column=0, sticky='w', padx=10, pady=5)
    tk.Entry(dialog, textvariable=password_var, show='*').grid(row=2, column=1, padx=10, pady=5)

    tk.Button(dialog, text="Add", command=add_and_close).grid(row=3, column=0, padx=10, pady=10)
    tk.Button(dialog, text="Cancel", command=dialog.destroy).grid(row=3, column=1, padx=10, pady=10)

    dialog.focus_force()
```
- **Purpose:** Provides a UI for adding passwords.
- **Behavior:**
    - Opens a Toplevel dialog window.
    - Accepts inputs for Service, Username, and Password.
    - Validates the inputs and adds the password using add_password() if valid.
    - Displays success or error messages using messagebox.
'get_password(service)'
```
def get_password(service):
    passwords = load_passwords()
    return passwords.get(service, [])
```
- **Purpose:** Retrieves passwords for a given service.
- **Parameters:** service (str) - The service for which passwords are requested.
- **Behavior:**
    - Loads passwords from the JSON file.
    - Returns a list of dictionaries containing usernames and passwords for the specified service. If the service doesn't exist, returns an empty list.
'delete_password(service, username)'
```
def delete_password(service, username):
    passwords = load_passwords()
    if service in passwords:
        passwords[service] = [acc for acc in passwords[service] if acc["username"] != username]
        if not passwords[service]:
            del passwords[service]
        save_passwords(passwords)
        print("Password deleted!")
```
- **Purpose:** Deletes a password entry for a given service and username.
- **Parameters:** service (str), username (str) - Details of the password to be deleted.
- **Behavior:**
    - Loads passwords from the JSON file.
    - Removes the specified username/password pair from the service's list.
    - If no more passwords are left for the service, removes the service entry altogether.
    - Saves the updated passwords back to the JSON file.
    - Prints a message confirming the deletion.
'refresh_service_list()'
```
def refresh_service_list():
    services = load_passwords()
    for widget in service_frame.winfo_children():
        widget.destroy()
    for service in services:
        service_button = tk.Button(service_frame, text=service, command=lambda s=service: show_service_details(s))
        service_button.pack(fill='x', pady=2)
```
- **Purpose:** Refreshes the list of services displayed in the GUI.
- **Behavior:**
    - Clears all existing buttons in the service_frame.
    - Retrieves the current list of services from the JSON file.
    - Creates a button for each service, which when clicked, shows the details of that service using show_service_details().
'show_service_details(service)'
```
def show_service_details(service):
    accounts = get_password(service)
    if accounts:
        for widget in details_frame.winfo_children():
            widget.destroy()
        tk.Label(details_frame, text=f"Details for {service}", font=('Helvetica', 14, 'bold')).pack(pady=10)
        for acc in accounts:
            acc_frame = tk.Frame(details_frame)
            acc_frame.pack(fill='x', pady=2)

            tk.Label(acc_frame, text=f"Username: {acc['username']}").pack(side='left', padx=5)
            tk.Button(acc_frame, text="Copy Username", command=lambda u=acc['username']: copy_to_clipboard(u)).pack(side='left', padx=5)

            tk.Label(acc_frame, text=f"Password: {acc['password']}").pack(side='left', padx=5)
            tk.Button(acc_frame, text="Copy Password", command=lambda p=acc['password']: copy_to_clipboard(p)).pack(side='left', padx=5)
    else:
        messagebox.showinfo("Error", "No passwords found for this service.")
```
- **Purpose:** Displays the details (username/password) for a selected service.
- **Parameters:** service (str) - The service for which details are requested.
- **Behavior:**
    - Clears all existing widgets (labels, buttons) in the details_frame.
    - Retrieves the list of accounts (username/password pairs) for the specified service using get_password().
    - Displays each username and password pair with corresponding "Copy" buttons for clipboard functionality.
    - If no passwords are found for the service, displays an error message using messagebox.
'copy_to_clipboard(text)'
```
def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Keeps the clipboard content after the window is closed
    messagebox.showinfo("Success", f"Copied to clipboard: {text}")
```
- Purpose:** Copies a given text to the clipboard.
- Parameters:** text (str) - The text to be copied.
- Behavior:**
    - Clears the clipboard contents.
    - Appends the specified text to the clipboard.
    - Updates the root window to maintain clipboard content even after the application window is closed.
    - Displays a success message with the copied text using messagebox.

## User Interface (UI) Setup
```
root = tk.Tk()
root.title("Password Manager")

# Header frame
header_frame = tk.Frame(root, bg="lightblue")
header_frame.pack(pady=10, padx=10, fill="x")

# Main frame for services and details
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Frame for the list of services
service_frame = tk.LabelFrame(main_frame, text="Saved Services", width=200)
service_frame.pack(side="left", fill="y", padx=10, pady=10)

# Frame for showing details of selected service
details_frame = tk.LabelFrame(main_frame, text="Service Details", width=400)
details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Buttons for Add Password, Delete Password, and Exit
tk.Button(header_frame, text="Add Password", command=add_password_ui).pack(side='left', padx=10, pady=5)
tk.Button(header_frame, text="Delete Password", command=delete_password_ui).pack(side='left', padx=10, pady=5)
tk.Button(header_frame, text="Exit", command=root.quit).pack(side='left', padx=10, pady=5)

# Initialize the application
refresh_service_list()

root.mainloop()
```
**Explanation of UI Setup**
- **Root Window (tk.Tk()):** Initializes the main application window with the title "Password Manager".
- **Header Frame:** Contains buttons for "Add Password", "Delete Password", and "Exit". It's packed at the top ('x' axis) of the root window.
- **Main Frame (main_frame):**
    - Contains two sub-frames: service_frame (for displaying services) and details_frame (for displaying service details).
    - Packed to expand in both directions ('both'), filling the available space.
- **Buttons:**
    - **"Add Password":** Calls add_password_ui() to open a dialog for adding passwords.
    - **"Delete Password":** Calls delete_password_ui() to open a dialog for deleting passwords.
    - **"Exit":** Closes the application.
- **Initialization:** Calls refresh_service_list() to populate the service_frame with buttons for each saved service from the JSON file.

## Conclusion

This password manager application provides a basic yet functional GUI for managing passwords. It allows users to add, view, and delete passwords for different services, with options to copy usernames and passwords to the clipboard. The application handles file I/O operations using JSON for storing passwords securely. Further enhancements can be made for validation, encryption, and more sophisticated GUI improvements based on specific needs and preferences.
