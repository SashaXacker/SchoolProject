from tkinter import *
from functools import partial
import sqlite3
from ttkthemes import ThemedTk
import tkinter.ttk as ttk
from tkcalendar import Calendar


sql = '''SELECT list.id, inventnum, typetext, cab, statustext, data FROM list
                JOIN typelist ON list.type = typelist.id
                JOIN statuslist ON list.status = statuslist.id'''

sqltype = '''SELECT list.id,inventnum, typetext, cab, statustext, data FROM list
                JOIN typelist ON list.type = typelist.id
                JOIN statuslist ON list.status = statuslist.id
                WHERE list.{obj} = {type}'''

typelist = '''SELECT typetext FROM typelist'''

statuslist = 'SELECT statustext FROM statuslist'


def size(w,h,qframe):
    qframe.resizable(width=False, height=False)
    ws = qframe.winfo_screenwidth()
    hs = qframe.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    qframe.geometry('%dx%d+%d+%d' % (w, h, x, y))


def comlist(coml,comsql):
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute(comsql)
        list = cur.fetchall()
        for x in list:
            coml.append(x[0])


def addFrame():
    add = Toplevel(root)
    w = 400
    h = 400
    size(w,h,add)
    add.grid()
    comtype = []
    comlist(comtype,typelist)
    comstatus = []
    comlist(comstatus,statuslist)
    num = ttk.Label(add,text='Номер:', font='Arial 16',anchor='e').grid(row=0,column=0,padx=5,sticky=E)
    addnum = ttk.Entry(add, font='Arial 16',width=18).grid(row=0,column=1,sticky=W)

    type = ttk.Label(add,text='Тип:', font='Arial 16',anchor='e').grid(row=1,column=0,padx=5,pady=3,sticky=E)
    addtype = ttk.Combobox(add,values=comtype,state='readonly',font='Arial 16',width=17).grid(row=1,column=1,pady=3,sticky=W)

    cab = ttk.Label(add,text='Кабинет:', font='Arial 16',anchor='e').grid(row=2,column=0,padx=5,sticky=E)
    addcab = ttk.Entry(add, font='Arial 16',width=18).grid(row=2,column=1,sticky=W)
    
    status = ttk.Label(add,text='Статус:', font='Arial 16',anchor='e').grid(row=3,column=0,padx=5,sticky=E,pady=3)
    addstatus = ttk.Combobox(add,values=comstatus,state='readonly',font='Arial 16',width=17).grid(row=3,column=1,pady=3,sticky=W)
    
    data = ttk.Label(add,text='Дата:', font='Arial 16',anchor='e').grid(row=4,column=0,padx=5,sticky='EN')
    adddata = Calendar(add,background='#41ABE9').grid(row=4,column=1)

    faddToTable = partial(addToTable,)
    btnadd = ttk.Button(add,text='Добавить',style = "Bold.TButton", command=faddToTable).grid(row=5, column=1,sticky='ES', pady=10)

def addToTable():


def clearFrame():
    for widget in main.winfo_children():
        widget.destroy()
    plabel  = ttk.Label(main,text='').grid(row=0,column=0)
    id      = ttk.Label(main, text='ID', font='Arial 16',background='#fff', width=3).grid(row=1, column=0, padx=3)
    num      = ttk.Label(main, text='Номер', font='Arial 16',background='#fff', width=12).grid(row=1, column=1, sticky=W)
    type    = ttk.Label(main,text='Тип',font='Arial 16',background='#fff',  width=10).grid(row=1, column=2, sticky=W)
    cab     = ttk.Label(main,text='Кабинет', font='Arial 16', background='#fff',width=5).grid(row=1, column=3, sticky=W, padx=2)
    status  = ttk.Label(main,text='Статус', font='Arial 16',  background='#fff',width=7).grid(row=1, column=4, sticky=W)
    data    = ttk.Label(main, text='Дата', font='Arial 16',background='#fff', width=9).grid(row=1, column=5, sticky=W, padx=2)

    btnall = ttk.Button(main,text='Вся база', width=11,style = "Bold.TButton", command=mainmenu).grid(row=1,column=6,sticky=E, padx=5)
    ftypebtn1 = partial(typebtn,'type', 1)
    btntype1 = ttk.Button(main,text='Компьютеры', width=11,style = "Bold.TButton", command=ftypebtn1).grid(row=2,column=6,sticky=E, padx=5)
    ftypebtn2 = partial(typebtn,'type',2)
    btntype2 = ttk.Button(main,text='Ноутбуки', width=11,style = "Bold.TButton", command=ftypebtn2).grid(row=3,column=6,sticky=E,padx=5)
    fstatus1 = partial(typebtn,'status',1)
    btnstatus1 = ttk.Button(main,text='Активно', width=11,style = "Bold.TButton", command=fstatus1).grid(row=4,column=6,sticky=E,padx=5)
    fstatus2 = partial(typebtn,'status',2)
    btnstatus1 = ttk.Button(main,text='Архив', width=11,style = "Bold.TButton", command=fstatus2).grid(row=4,column=6,sticky=E,padx=5)
    btnadd = ttk.Button(main,text='Добавить', width=9,style = "Bold.TButton",command=addFrame).grid(row=17,column=0,columnspan=2,sticky='WS',padx=15)




def view(i,*x):
    if i % 2 == 0:
        id     = ttk.Label(main,text=x[0],font='Arial 16',background='#b3b4bc',width=3).grid(row=i,column=0,padx=2,pady=5,sticky=W)
        num    = ttk.Label(main,text=x[1],font='Arial 16',background='#b3b4bc',width=12,anchor='e').grid(row=i,column=1,sticky=W,pady=5)
        type   = ttk.Label(main,text=x[2],font='Arial 16',background='#b3b4bc',width=10).grid(row=i,column=2,sticky=W,pady=5,padx=2)
        cab    = ttk.Label(main,text=x[3],font='Arial 16',background='#b3b4bc',width=5).grid(row=i,column=3,sticky=W,pady=5)
        status = ttk.Label(main,text=x[4],font='Arial 16',background='#b3b4bc',width=7).grid(row=i,column=4,sticky=W,pady=5,padx=2)
        data   = ttk.Label(main,text=x[5],font='Arial 16',background='#b3b4bc',width=9).grid(row=i,column=5,sticky=W,pady=5)
    else:
        id     = ttk.Label(main,text=x[0],font='Arial 16',background='#b3b4bc',width=3).grid(row=i,column=0,padx=2)
        num    = ttk.Label(main,text=x[1],font='Arial 16',background='#b3b4bc',width=12,anchor='e').grid(row=i,column=1,sticky=W)
        type   = ttk.Label(main,text=x[2],font='Arial 16',background='#b3b4bc',width=10).grid(row=i,column=2,sticky=W,padx=2)
        cab    = ttk.Label(main,text=x[3],font='Arial 16',background='#b3b4bc',width=5).grid(row=i,column=3,sticky=W)
        status = ttk.Label(main,text=x[4],font='Arial 16',background='#b3b4bc',width=7).grid(row=i,column=4,sticky=W,padx=2)           
        data   = ttk.Label(main,text=x[5],font='Arial 16',background='#b3b4bc',width=9).grid(row=i,column=5,sticky=W)


def typebtn(obj,type):
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute(sqltype.format(obj=obj,type=type))
        list = cur.fetchall()
        clearFrame()
        i=2
        for x in list:
            view(i,*x)          
            i+=1        



def nextbtn(already):
    nextstring = partial(nextstr, already)
    nextbtn = ttk.Button(main,text='next -->',style = "Bold.TButton",width=6,command=nextstring).grid(row=17,column=5,sticky=E)


def prevbtn(already):
    prevstring = partial(prevstr, already)
    prevbtn = ttk.Button(main,text='<-- prev',style = "Bold.TButton",width=6,command=prevstring).grid(row=17,column=4,sticky=W)


def nextstr(qstr):
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        qlen = len(cur.fetchall()) - qstr
        if qlen > 15:
            clearFrame()
            cur.execute(sql)
            for j in range(0,qstr):
                cur.fetchone()
            list = cur.fetchall()
            i=2
            for x in list:
                view(i,*x)
                i+=1
                qstr+=1
                if i == 17:break
            nextbtn(qstr)
            prevbtn(qstr)
        else:
            clearFrame()
            cur.execute(sql)
            for j in range(0,qstr):
                cur.fetchone()
            list = cur.fetchall()
            i=2
            for x in list:
                view(i,*x)
                i+=1
                qstr+=1
            prevbtn(qstr)

def prevstr(qstr):
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        qlen = len(cur.fetchall()) - qstr
################ НЕ ДОДЕЛАНО!!!##################
        if qlen > 15:
            cur.execute(sql)
            print(len(cur.fetchall()))
            # for j in range(0,qlen):
            #     print(cur.fetchone())

            # print(cur.fetchall())
            print(qstr)
################################################
        else:
            clearFrame()
            cur.execute(sql)
            i=2
            for j in range(0,15):
                x = cur.fetchone()
                view(i,*x)      
                i+=1
            a = i - 2
            nextbtn(a)
    


def mainmenu():
    clearFrame()
    with sqlite3.connect('server.db') as con:
        cur = con.cursor()
        cur.execute(sql)
        list = cur.fetchall()
        i = 2
        if len(list) > 15:
            cur.execute(sql)
            for j in range(0,15):
                x = cur.fetchone()
                view(i,*x)          
                i+=1
            a = i - 2
            nextbtn(a)

        else:
            for x in list:
                view(i,*x)          
                i+=1






root = ThemedTk()
root.title('DB')
root.set_theme("breeze")
w = 850
h = 600
size(w,h,root)
main = Frame(root)
main.grid()
boldStyle = ttk.Style ()
boldStyle.configure("Bold.TButton", font = ('Arial','14'))
mainmenu()
root.mainloop()