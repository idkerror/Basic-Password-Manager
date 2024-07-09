import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
import os
import json

PASSWORD_FILE = 'passwords.json'

def load_passwords():
    if not os.path.exists(PASSWORD_FILE):
        return {}
    try:
        with open(PASSWORD_FILE, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading passwords: {e}")
        return {}

def save_passwords(passwords):
    try:
        with open(PASSWORD_FILE, 'w') as file:
            json.dump(passwords, file)
    except Exception as e:
        print(f"Error saving passwords: {e}")

def add_password(service, username, password):
    passwords = load_passwords()
    if service not in passwords:
        passwords[service] = []
    passwords[service].append({"username": username, "password": password})
    save_passwords(passwords)
    print("Password added!")

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

def get_password(service):
    passwords = load_passwords()
    return passwords.get(service, [])

def delete_password(service, username):
    passwords = load_passwords()
    if service in passwords:
        passwords[service] = [acc for acc in passwords[service] if acc["username"] != username]
        if not passwords[service]:
            del passwords[service]
        save_passwords(passwords)
        print("Password deleted!")

def get_password_ui(service):
    accounts = get_password(service)
    if accounts:
        for widget in details_frame.winfo_children():
            widget.destroy()
        tk.Label(details_frame, text=f"Details for {service}", font=('Helvetica', 14, 'bold')).pack(pady=10)
        for acc in accounts:
            acc_frame = tk.Frame(details_frame, bg="white", padx=10, pady=5, relief=tk.RIDGE, bd=2)
            acc_frame.pack(fill='x', pady=5)

            tk.Label(acc_frame, text=f"Username: {acc['username']}", font=('Helvetica', 10)).pack(side='left', padx=5)
            copy_username_btn = tk.Button(acc_frame, text="Copy", bg="#4CAF50", fg="white", command=lambda u=acc['username']: copy_to_clipboard(u))
            copy_username_btn.pack(side='left', padx=5)

            tk.Label(acc_frame, text=f"Password: {acc['password']}", font=('Helvetica', 10)).pack(side='left', padx=5)
            copy_password_btn = tk.Button(acc_frame, text="Copy", bg="#2196F3", fg="white", command=lambda p=acc['password']: copy_to_clipboard(p))
            copy_password_btn.pack(side='left', padx=5)
    else:
        messagebox.showinfo("Error", "No passwords found for this service.")

def delete_password_ui():
    service = simpledialog.askstring("Input", "Service:")
    username = simpledialog.askstring("Input", "Username:")
    if service and username:
        delete_password(service, username)
        messagebox.showinfo("Success", "Password deleted!")
        refresh_service_list()

def refresh_service_list():
    services = load_passwords()
    for widget in service_frame.winfo_children():
        widget.destroy()
    for service in services:
        service_button = tk.Button(service_frame, text=service, bg="#FF5722", fg="white", activebackground="#FFA726",
                                  activeforeground="white", relief=tk.RAISED, bd=2,
                                  command=lambda s=service: show_service_details(s))
        service_button.pack(fill='x', pady=2)

def show_service_details(service):
    get_password_ui(service)

def copy_to_clipboard(text):
    root.clipboard_clear()
    root.clipboard_append(text)
    root.update()  # Keeps the clipboard content after the window is closed
    messagebox.showinfo("Success", f"Copied to clipboard: {text}")

# Initialize Tkinter root window
root = tk.Tk()
root.title("Password Manager")
root.geometry("800x600")

# Header frame
header_frame = tk.Frame(root, bg="#263238")
header_frame.pack(fill="x")

tk.Label(header_frame, text="Password Manager", fg="white", bg="#263238", font=('Helvetica', 18, 'bold')).pack(pady=10)

# Main frame for services and details
main_frame = tk.Frame(root)
main_frame.pack(pady=10, padx=10, fill="both", expand=True)

# Frame for the list of services
service_frame = tk.LabelFrame(main_frame, text="Saved Services", width=200, bg="#B0BEC5", fg="black", font=('Helvetica', 12, 'bold'))
service_frame.pack(side="left", fill="y", padx=10, pady=10)

# Frame for showing details of selected service
details_frame = tk.LabelFrame(main_frame, text="Service Details", width=400, bg="#B0BEC5", fg="black", font=('Helvetica', 12, 'bold'))
details_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

# Refresh the service list initially
refresh_service_list()

# Buttons for add, delete, and exit
button_frame = tk.Frame(root)
button_frame.pack(side="bottom", fill="x", pady=10)

add_button = tk.Button(button_frame, text="Add Password", command=add_password_ui)
add_button.pack(side="left", padx=10)

delete_button = tk.Button(button_frame, text="Delete Password", command=delete_password_ui)
delete_button.pack(side="left", padx=10)

exit_button = tk.Button(button_frame, text="Exit", command=root.quit)
exit_button.pack(side="right", padx=10)

# Start the Tkinter event loop
root.mainloop()
