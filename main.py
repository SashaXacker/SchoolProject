from tkinter import *
from tkinter import messagebox
from functools import partial
from ttkthemes import ThemedTk
import tkinter.ttk as ttk
import mariadb
from table import main
import re


# Регистрация
def reg(user, passwd):
    this_login = user.get()
    this_password = passwd.get()
    try:
        con = mariadb.connect(
            user="create",
            password="fakepassword",
            host="178.154.197.251",
            port=3306,
            database="db")
        cur = con.cursor()
        cur.execute(f"CREATE USER '{this_login}'@'%' IDENTIFIED BY '{this_password}'")
        cur.execute(f"GRANT SELECT ON db.* TO '{this_login}'@'%'")
        con.commit()
        messagebox.showinfo('Успешно', 'Вы успешно зарегистрировались')

    except mariadb.Error:
        messagebox.showwarning("Ошибка", 'Введите корректные данные для создания аккаунта.')


# Авторизация: Проверка логина и пароля
def validate_login(user, passwd):
    this_login = user.get()
    this_password = passwd.get()
    try:
        con = mariadb.connect(
            user=this_login,
            password=this_password,
            host="178.154.197.251",
            port=3306,
            database="db")
        con.close()
        con = mariadb.connect(
            user="create",
            password="fakepassword",
            host="178.154.197.251",
            port=3306,
            database="db")
        cur = con.cursor()
        cur.execute(f"SHOW GRANTS FOR '{this_login}'@'%'")
        tmp = cur.fetchall()
        if bool(re.search(r'ALL PRIVILEGES', tmp[1][0])) or bool(re.search(r'ALL PRIVILEGES', tmp[0][0])):
            main_frame(1, this_login, this_password)
        else:
            main_frame(0, this_login, this_password)

    except mariadb.Error:
        messagebox.showwarning("Ошибка", 'Неправильный логин или пароль.\n'
                                         'Введите корректные данные или зарегистрируйтесь')


def main_frame(right, login, passwd):
    root.destroy()
    main(right, login, passwd)


root = ThemedTk()
root.set_theme("breeze")
root.resizable(width=False, height=False)
w = 360
h = 120
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws / 2) - (w / 2)
y = (hs / 2) - (h / 2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y))
root.title('Authentication')
boldStyle = ttk.Style()
boldStyle.configure("Bold.TButton", font=('Arial', '14'))
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
loginButton = ttk.Button(auth, text="Authentication", width=14, command=validateLogin, style="Bold.TButton")
loginButton.grid(row=4, column=0, columnspan=2, sticky=W, padx=(0, 180))
reg = partial(reg, username, password)
regButton = ttk.Button(auth, text="Registration", width=14, command=reg, style="Bold.TButton")
regButton.grid(row=4, column=1, columnspan=2, padx=(60, 0))
root.mainloop()
