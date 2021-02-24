from ttkthemes import ThemedTk
import tkinter.ttk as ttk
from tkinter import *
from functools import partial
from tkinter import messagebox
import sqlite3
import tkinter.font as tkFont
from tkcalendar import Calendar
from datetime import datetime
from time import sleep
from table import *


#Регистрация
def reg(username, password):
    entlogin = username.get()
    entpassword = password.get()
    value = [entlogin, entpassword]
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        try:
            cur.execute('INSERT INTO users VALUES(?, ?)', value)
            con.commit()
            messagebox.showinfo('Успешно', 'Регистрация прошла успешно.\n Войдите в аккаунт.')
        except:
            messagebox.showinfo('Ошибка', 'Такой пользователь уже существует.')


#Авторизация: Проверка логина и пароля
def validateLogin(username, password):
    entlogin = username.get()
    entpassword = password.get()
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute('SELECT login FROM users')
        logins = cur.fetchall()
        x = -1
        for login in logins:
            x += 1
            curlogin = login[0]
            if curlogin == entlogin:
                cur.execute('SELECT password FROM users')
                passwords = cur.fetchall()
                if entpassword == passwords[x][0]:
                    mainFrame()
                    break
                else:
                    messagebox.showinfo("Ошибка", 'Неправильный логин или пароль.\nВведите коректные данные или зарегестрируйтесь')
                    break
        else:
            messagebox.showinfo("Ошибка", 'Неправильный логин или пароль.\nВведите коректные данные или зарегестрируйтесь')
    
    
def mainFrame():
    table()
    auth.destroy()
    


root = ThemedTk()
root.set_theme("breeze")
root.resizable(width=False, height=False)
w = 850
h = 650
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
root.geometry('%dx%d+%d+%d' % (w, h, x, y)) 


root.title('Authefication')

# Окно авторизации в систему
auth = ttk.Frame(root)

auth.grid()


usernameLabel = ttk.Label(auth, text="Username",font="Arial 14").grid(row=0, column=0)
username = StringVar()
usernameEntry = ttk.Entry(auth, textvariable=username, width=20, font="Arial 14").grid(row=0, column=1)  
passwordLabel = ttk.Label(auth,text="Password",font="Arial 14").grid(row=1, column=0)  
password = StringVar()
passwordEntry = ttk.Entry(auth, textvariable=password, show='*', width=20,font="Arial 14").grid(row=1, column=1)  
validateLogin = partial(validateLogin, username, password)
loginButton = ttk.Button(auth, text="Authefication",width=11, command=validateLogin,style = "Bold.TButton").grid(row=4, column=0, columnspan=2, sticky=W, padx=15)  
reg = partial(reg, username, password)
regButton = ttk.Button(auth, text="Registration",width=11,command=reg,style = "Bold.TButton").grid(row=4, column=1, columnspan=2, padx=70)  


root.mainloop()