from os import environ, path, makedirs
from random import randint, choice, shuffle
from tkinter import simpledialog, messagebox, Tk, PhotoImage, Canvas, Label, Entry, Button, END
import pyperclip
import json
from dotenv import load_dotenv

from crypto_utils import derive_key, new_salt, encrypt, decrypt

load_dotenv()


HOME = environ.get('USERPROFILE') or environ.get('HOME')
APP_DIR = path.join(HOME or '.', '.password_manager')
makedirs(APP_DIR, exist_ok=True)
DATA_FILE = path.join(APP_DIR, 'passwords.json')
SALT_FILE = path.join(APP_DIR, 'salt.bin')

EMAIL = environ.get('EMAIL') or ''

MASTER_PASSWORD = None

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate():
    """To generate a random password"""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    password_list = password_symbols + password_numbers + password_letters

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    """To add the entries to the data file"""
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Error!", message="Fields are empty")
    else:
        try:
            with open(DATA_FILE, mode="r") as password_file:

                data = json.load(password_file)
        except FileNotFoundError:
            data = {}

        if not path.exists(SALT_FILE):
            salt = new_salt()
            with open(SALT_FILE, 'wb') as sf:
                sf.write(salt)
        else:
            with open(SALT_FILE, 'rb') as sf:
                salt = sf.read()

        if MASTER_PASSWORD is None:
            messagebox.showerror(title="Error", message="Master password not set. Restart and provide it.")
            return

        key = derive_key(MASTER_PASSWORD, salt)

        enc_password = encrypt(password.encode('utf-8'), key).decode('utf-8')
        new_data[website]['password'] = enc_password

        data.update(new_data)
        with open(DATA_FILE, mode="w") as password_file:
            json.dump(data, password_file, indent=4)

        website_entry.delete(0, END)
        password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    """To search password from data file"""
    website = website_entry.get()
    try:
        with open(DATA_FILE, mode="r") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops!", message="No saved passwords file found")
        return

    if website in data:
        stored = data[website]
        email = stored.get("email", "")
        enc_password = stored.get("password", "")

        if not path.exists(SALT_FILE):
            messagebox.showerror(title="Oops!", message="Encryption salt missing")
            return
        with open(SALT_FILE, 'rb') as sf:
            salt = sf.read()

        if MASTER_PASSWORD is None:
            messagebox.showerror(title="Error", message="Master password not set. Restart and provide it.")
            return

        key = derive_key(MASTER_PASSWORD, salt)
        try:
            password = decrypt(enc_password.encode('utf-8'), key).decode('utf-8')
        except Exception:
            messagebox.showerror(title="Error", message="Failed to decrypt password. Wrong master password?")
            return

        messagebox.showinfo(title=website, message=f"Email: {email},\nPassword: {password}")
        pyperclip.copy(password)
    else:
        messagebox.showerror(title="Oops!", message="No saved passwords exist")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

MASTER_PASSWORD = simpledialog.askstring("Master Password", "Enter master password (will be used to encrypt/decrypt data):", show='*')

if not MASTER_PASSWORD:
    messagebox.showerror(title="Error", message="Master password not set. Restart and provide it.")
    exit()

logo = PhotoImage(file="logo.png")

canvas = Canvas(width=200, height=200)
canvas.create_image(100, 100, image=logo)
canvas.grid(row=0, column=1)

# Labels
website_label = Label(text="Website:")
website_label.grid(row=1, column=0)
password_label = Label(text="Password:")
password_label.grid(row=3, column=0)
email_label = Label(text="Email/Username:")
email_label.grid(row=2, column=0)

# Entries
website_entry = Entry(width=17)
website_entry.focus()
website_entry.grid(row=1, column=1)
email_entry = Entry(width=35)
email_entry.insert(0, EMAIL)
email_entry.grid(row=2, column=1, columnspan=2)
password_entry = Entry(width=17)
password_entry.grid(row=3, column=1)

# Buttons
add_button = Button(text="Add", width=36, command=add)
add_button.grid(row=4, column=1, columnspan=2)
password_button = Button(text="Generate Password", command=generate)
password_button.grid(row=3, column=2)
search_button = Button(text="Search", fg="Yellow", bg="Blue", width=15, command=search)
search_button.grid(row=1, column=2)

window.mainloop()
