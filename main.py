from tkinter import *
from tkinter import messagebox
from functools import partial
import sqlite3
from ttkthemes import ThemedTk
import tkinter.ttk as ttk
from table import main


# Регистрация
def reg(user, passwd):
    this_login = user.get()
    this_password = passwd.get()
    value = [this_login, this_password]
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO users VALUES(?, ?)', value)
            con.commit()
            messagebox.showinfo('Успешно', 'Регистрация прошла успешно.\n Войдите в аккаунт.')
        except:
            messagebox.showinfo('Ошибка', 'Такой пользователь уже существует.')


# Авторизация: Проверка логина и пароля
def validate_login(user, passwd):
    this_login = user.get()
    this_password = passwd.get()
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute('SELECT login FROM users')
        logins = cur.fetchall()
        el = -1
        for login in logins:
            el += 1
            current_login = login[0]
            if current_login == this_login:
                cur.execute('SELECT password FROM users')
                passwords = cur.fetchall()
                if this_password == passwords[el][0]:
                    main_frame()
                    break
                else:
                    messagebox.showinfo("Ошибка", 'Неправильный логин или пароль.\n'
                                                  'Введите корректные данные или зарегистрируйтесь')
                    break
        else:
            messagebox.showinfo("Ошибка", 'Неправильный логин или пароль.\n'
                                          'Введите корректные данные или зарегистрируйтесь')


def main_frame():
    root.destroy()
    main()


root = ThemedTk()
root.set_theme("breeze")
root.resizable(width=False, height=False)
w = 850
h = 650
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))

root.title('Authentication')

# Окно авторизации в систему
auth = ttk.Frame(root)

auth.grid()

usernameLabel = ttk.Label(auth, text="Username", font="Arial 14")
usernameLabel.grid(row=0, column=0)
username = StringVar()
usernameEntry = ttk.Entry(auth, textvariable=username, width=20, font="Arial 14")
usernameEntry.grid(row=0, column=1)
passwordLabel = ttk.Label(auth, text="Password", font="Arial 14")
passwordLabel.grid(row=1, column=0)
password = StringVar()
passwordEntry = ttk.Entry(auth, textvariable=password, show='*', width=20, font="Arial 14")
passwordEntry.grid(row=1, column=1)
validateLogin = partial(validate_login, username, password)
loginButton = ttk.Button(auth, text="Authentication", width=11, command=validateLogin, style="Bold.TButton")
loginButton.grid(row=4, column=0, columnspan=2, sticky=W, padx=15)
reg = partial(reg, username, password)
regButton = ttk.Button(auth, text="Registration", width=11, command=reg, style="Bold.TButton")
regButton.grid(row=4, column=1, columnspan=2, padx=70)

root.mainloop()
