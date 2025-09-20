from os import environ
from random import randint, choice, shuffle
from tkinter import messagebox, Tk, PhotoImage, Canvas, Label, Entry, Button, END
import pyperclip
import rsa
import json
from dotenv import load_dotenv

load_dotenv()

PATH = environ.get('PATH')
EMAIL = environ.get('EMAIL')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project

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
            with open(f"{PATH}/passwords.json", mode="r") as password_file:
                # Reading old data
                data = json.load(password_file)
        except FileNotFoundError:
            with open(f"{PATH}/passwords.json", mode="w") as password_file:
                json.dump(new_data, password_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)
            with open(f"{PATH}/passwords.json", mode="w") as password_file:
                # Saving updated data
                json.dump(data, password_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- SEARCH PASSWORD ------------------------------- #
def search():
    """To search password from data file"""
    website = website_entry.get()
    try:
        with open(f"{PATH}/passwords.json", mode="r") as password_file:
            data = json.load(password_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops!", message="File not found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email},\nPassword: {password}")
            pyperclip.copy(password)
        else:
            messagebox.showerror(title="Oops!", message="No saved passwords exist")



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

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
