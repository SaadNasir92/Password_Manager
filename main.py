import tkinter as tk
from tkinter import messagebox as mb
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
               'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_list += [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_list += [random.choice(numbers) for _ in range(random.randint(2, 4))]

    random.shuffle(password_list)
    password = ''.join(password_list)
    pyperclip.copy(password)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pass():
    web = website_entry.get().title()
    username = user_or_email_entry.get()
    pword = password_entry.get()
    password_data = {
        web: {
            'Username/Email': username,
            'Password': pword
        }
    }
    if len(web) == 0 or len(pword) == 0 or len(username) == 0:
        mb.showerror(title='Oops', message='Please do not leave any fields empty.')
    else:
        is_ok = mb.askokcancel(title=web, message=f'These are the details entered: \n\nEmail: {username}\n'
                                                  f'Password: {pword}\n\nConfirm and Save?')
        if is_ok:

            try:
                with open('passwords.json', mode='r') as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open('passwords.json', mode='w') as data_file:
                    json.dump(password_data, data_file, indent=4)
            else:
                data.update(password_data)
                with open('passwords.json', mode='w') as data_file:
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, 'end')
                password_entry.delete(0, 'end')


# ---------------------------- Get Saved Data ------------------------------- #
def search():
    website = website_entry.get().title()
    try:
        with open('passwords.json', mode='r') as data_file:
            data = json.load(data_file)
        user = data[website]['Username/Email']
        pword = data[website]['Password']
    except FileNotFoundError:
        mb.showerror(title='Error', message='No datafile found.')
    except KeyError:
        mb.showerror(title='Error', message='No details for the website exist.')
    else:
        mb.showinfo(title=website, message=f'Username: {user}\nPassword: {pword}')
        pyperclip.copy(pword)


# ---------------------------- UI SETUP ------------------------------- #
# Window
win = tk.Tk()
win.config(pady=50, padx=50)
win.title('Password Manager')

# Canvas
canvas = tk.Canvas(width=200, height=200)
image = tk.PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=image)
canvas.grid(column=1, row=0)

# Labels
website_label = tk.Label(text='Website:')
website_label.grid(column=0, row=1)

user_or_email_label = tk.Label(text='Email/Username:')
user_or_email_label.grid(column=0, row=2)

password_label = tk.Label(text='Password:')
password_label.grid(column=0, row=3)

# Entry boxes
website_entry = tk.Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()

user_or_email_entry = tk.Entry(width=33)
user_or_email_entry.grid(column=1, row=2)
user_or_email_entry.insert(0, 'saadnasir80@gmail.com')

password_entry = tk.Entry(width=33)
password_entry.grid(column=1, row=3)

# Buttons
search_button = tk.Button(text='Search', command=search, width=15)
search_button.grid(column=2, row=1)

generate_password_button = tk.Button(text='Generate Password', command=generate_pass, width=15)
generate_password_button.grid(column=2, row=3)

add_button = tk.Button(text='Add', width=28, command=save_pass)
add_button.grid(column=1, row=4, columnspan=1)



win.mainloop()
