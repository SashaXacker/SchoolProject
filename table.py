from tkinter import *
from tkinter import messagebox
from functools import partial
from ttkthemes import ThemedTk
import tkinter.ttk as ttk
from tkcalendar import Calendar
from datetime import datetime
from time import sleep
import pandas as pd
import os
import mariadb


def main(right, login, passwd):

    sql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataEdit FROM list
                    JOIN typelist ON list.type = typelist.id
                    JOIN statuslist ON list.status = statuslist.id
                    JOIN cabinet ON list.cab = cabinet.id'''

    sqlType = '''SELECT inventNum, typetext, cabinet.number, statustext, dataEdit FROM list
                    JOIN typelist ON list.type = typelist.id
                    JOIN statuslist ON list.status = statuslist.id
                    JOIN cabinet ON list.cab = cabinet.id
                    WHERE list.{obj} = {type}'''

    typeList = '''SELECT typetext FROM typelist'''
    statusList = 'SELECT statustext FROM statuslist'
    cabList = '''SELECT cabinet.number FROM cabinet
                 ORDER BY id'''

    insertSql = 'INSERT INTO list( inventNum, type, cab, status, dataRegistration, dataEdit )'

    # НЕ ТРОГАТЬ
    whereSql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
                     JOIN typelist ON list.type = typelist.id
                     JOIN statuslist ON list.status = statuslist.id
                     JOIN cabinet ON list.cab = cabinet.id
WHERE'''
    standardSql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
                     JOIN typelist ON list.type = typelist.id
                     JOIN statuslist ON list.status = statuslist.id
                     JOIN cabinet ON list.cab = cabinet.id'''
    selectSql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
                   JOIN typelist ON list.type = typelist.id
                   JOIN statuslist ON list.status = statuslist.id
                   JOIN cabinet ON list.cab = cabinet.id
                   WHERE list.cab = {cab} and list.status = {status} and list.type = {type}'''

    def reverse_date(current_date):
        f_date = current_date.split('.')
        f_date = f_date[::-1]
        f_date = '-'.join(f_date)
        return f_date

    def date(format_of):
        time = datetime.now()
        str(time)
        date_list = [str(time.day), str(time.month), str(time.year), str(time.hour), str(time.minute), str(time.second)]
        for el in date_list:
            if len(el) == 1:
                date_list[date_list.index(el)] = '0' + el
        if format_of == 'ymd':
            now = f'{date_list[2]}-{date_list[1]}-{date_list[0]}'
        elif format_of == 'dmy_hms':
            now = f'{date_list[0]}-{date_list[1]}-{date_list[2]}_{date_list[3]}-{date_list[4]}-{date_list[5]}'
        else:
            now = 0
        return now

    def size(width, height, current_frame):
        current_frame.resizable(width=False, height=False)
        ws = current_frame.winfo_screenwidth()
        hs = current_frame.winfo_screenheight()
        x = (ws / 2) - (width / 2)
        y = (hs / 2) - (height / 2)
        current_frame.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def com_list(new_com_list, com_sql):
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        cur.execute(com_sql)
        sql_list = cur.fetchall()
        for x in sql_list:
            new_com_list.append(x[0])

        cur.close()
        con.close()

    def add_frame():
        add = Toplevel(root)
        width = 400
        height = 400
        size(width, height, add)
        add.grid()
        com_type = []
        com_list(com_type, typeList)
        com_status = []
        com_list(com_status, statusList)
        com_cab = []
        com_list(com_cab, cabList)
        number_add = StringVar()
        num = ttk.Label(add, text='Номер:', font='Arial 16', anchor='e')
        num.grid(row=0, column=0, padx=5, sticky=E)
        add_num = ttk.Entry(add, font='Arial 16', textvariable=number_add, width=18)
        add_num.grid(row=0, column=1, sticky=W)

        type_add = StringVar()
        lbl_type = ttk.Label(add, text='Тип:', font='Arial 16', anchor='e')
        lbl_type.grid(row=1, column=0, padx=5, pady=3, sticky=E)
        add_type = ttk.Combobox(add, values=com_type, state='readonly', textvariable=type_add, font='Arial 16', width=17)
        add_type.grid(row=1, column=1, pady=3, sticky=W)

        cab_add = StringVar()
        cab = ttk.Label(add, text='Кабинет:', font='Arial 16', anchor='e')
        cab.grid(row=2, column=0, padx=5, sticky=E)
        add_cab = ttk.Combobox(add, values=com_cab, state='readonly', textvariable=cab_add, font='Arial 16', width=17)
        add_cab.grid(row=2, column=1, sticky=W)

        status_add = StringVar()
        status = ttk.Label(add, text='Статус:', font='Arial 16', anchor='e')
        status.grid(row=3, column=0, padx=5, sticky=E, pady=3)
        add_status = ttk.Combobox(add, values=com_status, state='readonly', textvariable=status_add, font='Arial 16',
                                  width=17)
        add_status.grid(row=3, column=1, pady=3, sticky=W)

        date_reg_add = StringVar()
        date_reg = ttk.Label(add, text='Дата на учете:', font='Arial 16', anchor='e')
        date_reg.grid(row=4, column=0, padx=5, sticky='EN')
        add_date_reg = Calendar(add, background='#41ABE9', textvariable=date_reg_add, date_pattern='y-mm-dd')
        add_date_reg.grid(row=4, column=1)

        f_add_str = partial(add_str, number_add, type_add, cab_add, status_add, date_reg_add, add)
        btn_add = ttk.Button(add, text='Добавить', style="Bold.TButton", command=f_add_str)
        btn_add.grid(row=5, column=1, sticky='ES', pady=10)

    def select(sql_object, sql_list, obj):
        curr = ''
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        current_sql = 'SELECT id,{obj} FROM {list}'.format(obj=sql_object, list=sql_list)
        cur.execute(current_sql)
        length = len(cur.fetchall())
        cur.execute(current_sql)
        for i in range(0, length):
            x = cur.fetchone()
            if x[1] == obj:
                curr = x[0]
                break
        cur.close()
        con.close()

        return curr

    def add_str(number_add, type_add, cab_add, status_add, date_reg_add, add):
        number = number_add.get()

        this_type = type_add.get()
        cab = int(cab_add.get())
        status = status_add.get()
        date_reg = reverse_date(date_reg_add.get())
        date_change = date('ymd')
        this_type = select('typetext', 'typelist', this_type)
        cab = select('number', 'cabinet', cab)
        status = select('statustext', 'statuslist', status)

        temp_list = [number, this_type, cab, status, date_change, date_reg]
        for x in temp_list:
            if x == '':
                messagebox.showinfo('Ошибка', 'Введите все данные')
                break
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        try:
            cur.execute('''INSERT INTO list (inventNum, type, cab, status, dataEdit, dataRegistration)
                        VALUES(?, ?, ?, ?, ?, ?)''', temp_list)
            con.commit()
            messagebox.showinfo('Успешно', 'Элемент добавлен')
        except:
            messagebox.showinfo('Ошибка', 'Введите верные данные')

        cur.close()
        con.close()

        add.destroy()
        sleep(1)
        main_menu()

    def delete_frame():
        delete = Toplevel(root)
        width = 350
        height = 100
        size(width, height, delete)
        delete.grid()
        number_delete = StringVar()
        num = ttk.Label(delete, text='Номер:', font='Arial 16', anchor='e')
        num.grid(row=0, column=0, padx=5, sticky=E)
        add_num = ttk.Entry(delete, font='Arial 16', textvariable=number_delete, width=18)
        add_num.grid(row=0, column=1, sticky=W)
        f_delete_str = partial(delete_str, number_delete, delete)
        btn_delete = ttk.Button(delete, text='Удалить', style="Bold.TButton", command=f_delete_str)
        btn_delete.grid(row=1, column=1, sticky='ES', pady=10)

    def delete_str(number, delete):
        number = int(number.get())

        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()

        try:
            cur.execute(f'DELETE FROM list WHERE inventnum = {number}')
            con.commit()
            messagebox.showinfo('Успешно', 'Элемент удален')
        except:
            messagebox.showinfo('Ошибка', 'Введите верный номер')

        cur.close()
        con.close()

        delete.destroy()
        sleep(1)
        main_menu()

    def select_frame():
        frame = Toplevel(root)
        width = 800
        height = 400
        size(width, height, frame)
        frame.grid()
        com_type = []
        com_list(com_type, typeList)
        com_status = []
        com_list(com_status, statusList)
        com_cab = []
        com_list(com_cab, cabList)

        lbl_date = ttk.Label(frame, text='Дата', font='Arial 16')
        lbl_date.grid(row=0, column=0, columnspan=2, pady=(20, 0))
        f_select_start_date = StringVar()
        select_start_date = Calendar(frame, background='#41ABE9', textvariable=f_select_start_date,
                                     date_pattern='y-mm-dd')
        select_start_date.grid(row=1, column=0, padx=10, pady=5)
        f_select_finish_date = StringVar()
        select_finish_date = Calendar(frame, background='#41ABE9', textvariable=f_select_finish_date,
                                      date_pattern='y-mm-dd')
        select_finish_date.grid(row=1, column=1, pady=5)

        lbl_type = ttk.Label(frame, text='Тип', font='Arial 16')
        lbl_type.grid(row=0, column=2, columnspan=6, pady=(25, 0))
        list_type = Listbox(frame, font='Arial 16', height=6, selectmode=EXTENDED, exportselection=False)

        for lbl_type in com_type:
            list_type.insert(END, lbl_type)

        list_type.grid(column=2, row=1, columnspan=5, rowspan=1, padx=(25, 0), pady=(5, 0))
        scroll_type = ttk.Scrollbar(frame)
        list_type.config(yscrollcommand=scroll_type.set)
        scroll_type.config(command=list_type.yview)
        scroll_type.grid(column=7, row=1, rowspan=2, sticky=S + N + W, pady=(5, 0))

        cab = ttk.Label(frame, text='Кабинет', font='Arial 16')
        cab.grid(row=3, column=0, columnspan=1, pady=(5, 0))
        list_cab = Listbox(frame, font='Arial 16', height=4, width=8, selectmode=EXTENDED, exportselection=False)

        for cab in com_cab:
            list_cab.insert(END, cab)

        list_cab.grid(column=0, row=4, rowspan=1, padx=(80, 0), pady=(15, 0), sticky=W)
        scroll_cab = ttk.Scrollbar(frame)
        list_cab.config(yscrollcommand=scroll_cab.set)
        scroll_cab.config(command=list_cab.yview)
        scroll_cab.grid(column=0, row=4, rowspan=2, sticky=S + N, pady=(15, 0), padx=(85, 0))

        status = ttk.Label(frame, text='Статус', font='Arial 16')
        status.grid(row=3, column=1, columnspan=1, pady=(5, 0))
        list_status = Listbox(frame, font='Arial 16', height=4, width=9, selectmode=EXTENDED, exportselection=False)

        for status in com_status:
            list_status.insert(END, status)

        list_status.grid(column=1, row=4, rowspan=1, padx=(70, 0), pady=(15, 0), sticky=W)
        scroll_status = ttk.Scrollbar(frame)
        list_status.config(yscrollcommand=scroll_status.set)
        scroll_status.config(command=list_status.yview)
        scroll_status.grid(column=1, row=4, rowspan=2, sticky=S + N, pady=(15, 0), padx=(110, 0))
        f_btn = partial(btn_sql_select, list_status, list_cab, list_type, f_select_start_date, f_select_finish_date, frame)
        btn = ttk.Button(frame, text='Сделать запрос', style="Bold.TButton", command=f_btn)
        btn.grid(column=6, row=4, sticky=S + E)

    def save_to_excel():
        def current_el(current_id):
            result = list()
            try:
                con = mariadb.connect(
                    user=login,
                    password=passwd,
                    host="178.154.197.251",
                    port=3306,
                    database="db")
            except mariadb.Error as e:
                messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')
            cur = con.cursor()
            cur.execute(sql)
            length = len(cur.fetchall())
            cur.execute(sql)
            while length > 0:
                result.append(cur.fetchone()[current_id])
                length -= 1

            cur.close()
            con.close()
            return result

        names = current_el(0)
        types = current_el(1)
        cabinets = current_el(2)
        statuses = current_el(3)
        dates = current_el(4)

        df = pd.DataFrame({
            "Номер": names,
            "Тип": types,
            "Кабинет": cabinets,
            "Статус": statuses,
            "Дата изменения": dates
        })

        this_time = date('dmy_hms')

        if not os.path.isdir("excel"):
            os.mkdir("excel")
        df.to_excel(f'./excel/{this_time}.xlsx', index=False)
        messagebox.showinfo('Успешно', 'Файл успешно записан')

    def btn_sql_select(status, cab, current_type, start_date, finish_date, frame):
        status = list(status.curselection())
        cab = list(cab.curselection())
        current_type = list(current_type.curselection())
        start = reverse_date(start_date.get())
        finish = reverse_date(finish_date.get())

        def format_this(element):
            for e in element:
                element[element.index(e)] = element[element.index(e)] + 1
            element = ','.join(str(e) for e in element)
            return element

        current_type = format_this(current_type)
        status = format_this(status)
        cab = format_this(cab)

        if cab == '' and status == '' and current_type == '' and start == '' and finish == '':
            select_sql = standardSql
        else:
            select_sql = standardSql + '\nWHERE'
            if cab != '':
                if select_sql == whereSql:
                    select_sql += f' list.cab IN ({cab})'
                else:
                    select_sql += f' and list.cab IN ({cab})'
            if status != '':
                if select_sql == whereSql:
                    select_sql += f' list.status IN ({status})'
                else:
                    select_sql += f' and list.status IN ({status})'
            if current_type != '':
                if select_sql == whereSql:
                    select_sql += f' list.type IN ({current_type})'
                else:
                    select_sql += f' and list.type IN ({current_type})'
            if start != '':
                if select_sql == whereSql:
                    select_sql += f' dataRegistration >= date("{start}")'
                else:
                    select_sql += f' and dataRegistration >= date("{start}")'
            if start != '' and finish != '':
                select_sql += f' and dataRegistration <= date("{finish}")'
            if finish != '' and start == '':
                if select_sql == whereSql:
                    select_sql += f' dataRegistration <= date("{finish}")'
                else:
                    select_sql += f' and dataRegistration <= date("{finish}")'

        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        cur.execute(select_sql)
        messagebox.showinfo('Удачно', 'Найдено ' + str(len(cur.fetchall())) + ' элементов')
        frame.destroy()
        select_btn(select_sql)
        cur.close()
        con.close()

    def clear_frame():
        for widget in main.winfo_children():
            widget.destroy()
        for widget in bottomMenu.winfo_children():
            widget.destroy()
        blank_label = ttk.Label(main, text='')
        blank_label.grid(row=0, column=0, sticky=W)

        call_sort_by_id = partial(call_sort_by, "inventNum")
        num = ttk.Button(main, text='Номер', style="my.TButton", width=14, command=call_sort_by_id)
        num.grid(row=1, column=0, sticky=W, padx=2)

        call_sort_by_type = partial(call_sort_by, "typetext")
        lbl_type = ttk.Button(main, text='Тип', style="my.TButton", width=11, command=call_sort_by_type)
        lbl_type.grid(row=1, column=1, sticky=W)

        call_sort_by_cab = partial(call_sort_by, "cabinet.number")
        cab = ttk.Button(main, text='Кабинет', style="my.TButton", width=7, command=call_sort_by_cab)
        cab.grid(row=1, column=2, sticky=W, padx=2)

        call_sort_by_status = partial(call_sort_by, "statustext")
        status = ttk.Button(main, text='Статус', style="my.TButton", width=7, command=call_sort_by_status)
        status.grid(row=1, column=3, sticky=W)

        call_sort_by_data = partial(call_sort_by, "dataEdit")
        data = ttk.Button(main, text='Дата изменения', style="my.TButton", width=16, command=call_sort_by_data)
        data.grid(row=1, column=4, sticky=W, padx=2)

        right_menu = Frame(root)
        right_menu.grid(row=0, column=5, padx=5, sticky=N, pady=(15, 0))
        btn_all = ttk.Button(right_menu, text='Вся база', width=11, style="Bold.TButton", command=main_menu)
        btn_all.grid(row=0, column=0, sticky=W + N)
        f_type_btn_1 = partial(type_btn, 'type', 1)
        btn_type_1 = ttk.Button(right_menu, text='Компьютеры', width=11, style="Bold.TButton", command=f_type_btn_1)
        btn_type_1.grid(row=1, column=0, sticky=W + N, pady=(5, 0))
        f_type_btn_2 = partial(type_btn, 'type', 2)
        btn_type_2 = ttk.Button(right_menu, text='Ноутбуки', width=11, style="Bold.TButton", command=f_type_btn_2)
        btn_type_2.grid(row=2, column=0, sticky=W + N, pady=(5, 0))
        f_status_1 = partial(type_btn, 'status', 1)
        btn_status_1 = ttk.Button(right_menu, text='Активно', width=11, style="Bold.TButton", command=f_status_1)
        btn_status_1.grid(row=3, column=0, sticky=W + N, pady=(5, 0))
        f_status_2 = partial(type_btn, 'status', 2)
        btn_status_2 = ttk.Button(right_menu, text='Архив', width=11, style="Bold.TButton", command=f_status_2)
        btn_status_2.grid(row=4, column=0, sticky=W + N, pady=(5, 0))

        btn_excel = ttk.Button(right_menu, text='Вывод в excel', width=13, style="Bold.TButton", command=save_to_excel)
        btn_excel.grid(row=5, column=0, sticky=W, pady=(140, 0))
        btn_add = ttk.Button(right_menu, text='Добавить', width=13, style="Bold.TButton", command=add_frame)
        btn_add.grid(row=6, column=0, sticky=W, pady=(5, 0))
        if not right:
            btn_add['state'] = 'disabled'

        btn_delete = ttk.Button(right_menu, text='Удалить', width=13, style="Bold.TButton", command=delete_frame)
        btn_delete.grid(row=7, column=0, sticky=W, pady=(5, 0))
        if not right:
            btn_delete['state'] = 'disabled'

        btn_select = ttk.Button(right_menu, text='Выбор', width=13, style="Bold.TButton", command=select_frame)
        btn_select.grid(row=8, column=0, sticky=W, pady=(5, 0))

    def view(i, *x):
        num = ttk.Label(main, text=x[0], font='Arial 16', background='#b3b4bc', width=12, anchor='w')
        num.grid(row=i, column=0, sticky=W, pady=(5, 0), padx=2)
        lbl_type = ttk.Label(main, text=x[1], font='Arial 16', background='#b3b4bc', width=10)
        lbl_type.grid(row=i, column=1, sticky=W, pady=(5, 0))
        cab = ttk.Label(main, text=x[2], font='Arial 16', background='#b3b4bc', width=7, anchor='w')
        cab.grid(row=i, column=2, sticky=W, pady=(5, 0), padx=2)
        status = ttk.Label(main, text=x[3], font='Arial 16', background='#b3b4bc', width=7)
        status.grid(row=i, column=3, sticky=W, pady=(5, 0))
        data = ttk.Label(main, text=x[4], font='Arial 16', background='#b3b4bc', width=14)
        data.grid(row=i, column=4, sticky=W, pady=(5, 0), padx=(2, 0))

    def type_btn(obj, current_type):
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')
        cur = con.cursor()
        sql_type = sqlType.format(obj=obj, type=current_type)
        cur.execute(sql_type)
        sql_list = cur.fetchall()
        clear_frame()
        i = 2
        if len(sql_list) > 15:
            cur.execute(sql_type)
            for j in range(0, 15):
                x = cur.fetchone()
                view(i, *x)
                i += 1
            a = i - 2
            call_next_btn(a, sql_type)

        else:
            for x in sql_list:
                view(i, *x)
                i += 1
        cur.close()
        con.close()

    def select_btn(current_select_sql):
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        cur.execute(current_select_sql)
        sql_list = cur.fetchall()
        clear_frame()
        i = 2
        if len(sql_list) > 15:
            cur.execute(current_select_sql)
            for j in range(0, 15):
                x = cur.fetchone()
                view(i, *x)
                i += 1
            a = i - 2
            call_next_btn(a, current_select_sql)

        else:
            for x in sql_list:
                view(i, *x)
                i += 1
        cur.close()
        con.close()

    def call_sort_by(by):
        current_sql = sql + f'\n\t\t\t\tORDER BY {by}'
        select_btn(current_sql)

    def call_next_btn(already, current_sql):
        next_string = partial(next_str, already, current_sql)
        next_btn = ttk.Button(bottomMenu, text='next -->', style="Bold.TButton", width=7, command=next_string)
        next_btn.grid(row=0, column=2, sticky=E, pady=5, padx=5)

    def call_previous_btn(already, current_sql):
        previous_string = partial(previous_str, already, current_sql)
        previous_btn = ttk.Button(bottomMenu, text='<-- prev', style="Bold.TButton", width=7, command=previous_string)
        previous_btn.grid(row=0, column=1, sticky=W, pady=5)

    def next_str(current_str, current_sql):
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        cur.execute(current_sql)
        current_len = len(cur.fetchall()) - current_str
        if current_len > 15:
            clear_frame()
            cur.execute(current_sql)
            for j in range(0, current_str):
                cur.fetchone()
            sql_list = cur.fetchall()
            i = 2
            for x in sql_list:
                view(i, *x)
                i += 1
                current_str += 1
                if i == 17:
                    break
            call_next_btn(current_str, current_sql)
            call_previous_btn(current_str, current_sql)
        else:
            clear_frame()
            cur.execute(current_sql)
            for j in range(0, current_str):
                cur.fetchone()
            sql_list = cur.fetchall()
            i = 2
            for x in sql_list:
                view(i, *x)
                i += 1
                current_str += 1
            call_previous_btn(current_str, current_sql)
        cur.close()
        con.close()

    def previous_str(current_str, current_sql):
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')
        cur = con.cursor()
        cur.execute(current_sql)
        current_len = current_str - 15

        if current_str < len(cur.fetchall()):
            clear_frame()
            cur.execute(current_sql)
            i = 2
            for j in range(0, current_len - 15):
                _ = cur.fetchone()
            for x in range(current_len, current_str):
                x = cur.fetchone()
                view(i, *x)
                i += 1
                current_str -= 1

            call_next_btn(current_str, current_sql)
            if current_str != 15:
                call_previous_btn(current_str, current_sql)

        else:
            clear_frame()
            cur.execute(current_sql)
            i = 2
            for j in range(0, current_len):
                _ = cur.fetchone()

            sql_list = cur.fetchall()
            for x in sql_list:
                view(i, *x)
                i += 1
            current_str = current_str - (current_str % 15)
            call_next_btn(current_str, current_sql)
            call_previous_btn(current_str, current_sql)
        cur.close()
        con.close()

    def main_menu():
        clear_frame()
        try:
            con = mariadb.connect(
                user=login,
                password=passwd,
                host="178.154.197.251",
                port=3306,
                database="db")
        except mariadb.Error as e:
            messagebox.showwarning('Ошибка', f'Возникла ошибка при подключении к базе данных:\n {e}')

        cur = con.cursor()
        cur.execute(sql)
        sql_list = cur.fetchall()
        i = 2
        if len(sql_list) > 15:
            cur.execute(sql)
            for j in range(0, 15):
                x = cur.fetchone()
                view(i, *x)
                i += 1
            a = i - 2
            call_next_btn(a, sql)
        else:
            for x in sql_list:
                view(i, *x)
                i += 1
        cur.close()
        con.close()

    root = ThemedTk()
    root.title('DB')
    root.set_theme("breeze")
    w = 850
    h = 600
    size(w, h, root)
    main = Frame(root)
    main.grid(sticky=N)
    bottomMenu = Frame(root)
    bottomMenu.grid(row=17, sticky=E)
    boldStyle = ttk.Style()
    boldStyle.configure("Bold.TButton", font=('Arial', '14'))
    sortedButton = ttk.Style()
    sortedButton.configure("my.TButton", font=('Arial', '13'))
    main_menu()

    root.mainloop()

