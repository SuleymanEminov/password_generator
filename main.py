from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generator():
    password_entry.delete(0, 'end')
    # Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # for char in range(nr_letters):
    #     password_list.append(random.choice(letters))

    password_letters = [choice(letters) for _ in range(randint(8, 10))]

    # for char in range(nr_symbols):
    #     password_list += random.choice(symbols)

    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]

    # for char in range(nr_numbers):
    #     password_list += random.choice(numbers)

    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_numbers + password_symbols

    shuffle(password_list)

    password = ''.join(password_list)  # converts elements in password_list to a String

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def add():
    website = website_entry.get().upper()
    password = password_entry.get()
    email = email_entry.get()

    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == '' or email == '' or password == '':
        messagebox.showerror("Error", "Please fill in blank spaces")
    else:

        try:
            with open('passwords.json', 'r') as file:
                if file.read(2) != '':
                    file.seek(0)
                    # reading old data
                    data = json.load(file)
                    # check if website has a password in the json file
                    if website in data:

                        change = messagebox.askyesno("Warning",
                                                     "You already have a password for this website. Are you sure"
                                                     " you want to change it?")

                        if change:
                            data = new_data
                        else:
                            website_entry.delete(0, 'end')
                            password_entry.delete(0, 'end')
                    else:
                        # updating old data with new data
                        data.update(new_data)

            with open('passwords.json', 'w') as file:
                # saving updated data
                json.dump(data, file, indent=4)

        except FileNotFoundError:  # need this code for the first entry
            with open('passwords.json', 'w') as file:
                json.dump(new_data, file, indent=4)

        website_entry.delete(0, 'end')
        password_entry.delete(0, 'end')


# ---------------------------- SEARCH METHOD ------------------------------- #
def search():
    website = website_entry.get().upper()
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)

            if website.upper() in data:
                email = data[website]['email']
                password = data[website]['password']
                print(email, password)
                pyperclip.copy(password)
                messagebox.showinfo(website.title(), f"Email: {email}\n"
                                                     f"Password: {password}\n"
                                                     f"Your password was copied to your clipboard:)")

            else:
                messagebox.showerror("Not found", "Website info was not found in your database.")
    except FileNotFoundError:
        messagebox.showerror("Error", "Password database is not found.\nPlease add a new password.")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Generator")
window.config(pady=50, padx=50)

# logo
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=logo)

# labels
website_label = Label(text="Website:")
email_label = Label(text="Email/Username:")
password_label = Label(text="Password:")

# entries
website_entry = Entry(width=35)
website_entry.focus()
email_entry = Entry(width=35)
email_entry.insert(0, "suleyman.eminov22@gmail.com")
password_entry = Entry(width=21)

# buttons
gen_button = Button(text="Generate Password", command=generator)
add_button = Button(text="Add", width=36, command=add)
search_button = Button(text="Search", width=15, command=search)
# grid
canvas.grid(column=1, row=0)
website_label.grid(column=0, row=1)
website_entry.grid(column=1, row=1)
email_label.grid(column=0, row=2)
email_entry.grid(column=1, row=2, columnspan=2, sticky="nsew")
password_label.grid(column=0, row=3)
password_entry.grid(column=1, row=3, sticky="nsew")
gen_button.grid(column=2, row=3)
add_button.grid(column=1, row=4, columnspan=2, sticky="nsew")
search_button.grid(column=2, row=1, sticky='nsew')

window.mainloop()
