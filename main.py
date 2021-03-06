from pyperclip import copy
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox
import json

DEFAULT_USER = 'jamescolbertv@gmail.com'


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for char in range(randint(8, 10))]
    password_list += [choice(symbols) for char in range(randint(2, 4))]
    password_list += [choice(numbers) for char in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)

    password_input.config(show="")
    password_input.delete(0, END)
    password_input.insert(0, password)
    copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    global DEFAULT_USER
    website = website_input.get()
    username = username_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "username": username,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            with open("data.json", "w") as f:
                json.dump(new_data, f, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as f:
                json.dump(data, f, indent=4)
        finally:
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')
        if username != DEFAULT_USER:
            username_input.delete(0, 'end')
            username_input.insert(0, DEFAULT_USER)
        password_input.config(show="*")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_input.get()
    try:
        with open("data.json", "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        messagebox.showerror(title="ERROR", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title="Entry found!", message=f"Password found!\n{data[website]['username']}\n{data[website]['password']}")
        else:
            messagebox.showinfo(title="Not found", message="No details for the website exist.")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_input = Entry(width=21)
website_input.focus()
website_input.grid(column=1, row=1)

search_button = Button(width=13, text="Search", command=find_password)
search_button.grid(column=2, row=1)

username_label = Label(text="Username:")
username_label.grid(column=0, row=2)

username_input = Entry(width=35)
username_input.grid(column=1, row=2, columnspan=2)
username_input.insert(0, DEFAULT_USER)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_input = Entry(width=21, show="*")
password_input.grid(column=1, row=3)

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

add_button = Button(text="Add", width=36, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()
