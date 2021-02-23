from tkinter import *
from tkinter import messagebox
from functools import partial
import sqlite3
from ttkthemes import ThemedTk
import tkinter.ttk as ttk
from tkcalendar import Calendar
from datetime import datetime
from time import sleep

sql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataEdit FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id'''

sqltype = '''SELECT inventNum, typetext, cabinet.number, statustext, dataEdit FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id
				WHERE list.{obj} = {type}'''

typelist = '''SELECT typetext FROM typelist'''
statuslist = 'SELECT statustext FROM statuslist'
cablist = '''SELECT cabinet.number FROM list
			JOIN cabinet ON list.cab = cabinet.id'''

insertsql = 'INSERT INTO list( inventNum, type, cab, status, dataRegistration, dataEdit )'


def date():
	time = datetime.now()
	str(time)
	day = time.day
	month = time.month
	if len(str(month)) == 1:month = '0' + str(month)
	year = time.year
	now = str(day)+ '.' + str(month) + '.' + str(year)
	return now

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
	comcab = []
	comlist(comcab,cablist)
	numberadd = StringVar()
	num = ttk.Label(add,text='Номер:', font='Arial 16',anchor='e').grid(row=0,column=0,padx=5,sticky=E)
	addnum = ttk.Entry(add, font='Arial 16',textvariable=numberadd,width=18).grid(row=0,column=1,sticky=W)

	typeadd = StringVar()
	type = ttk.Label(add,text='Тип:', font='Arial 16',anchor='e').grid(row=1,column=0,padx=5,pady=3,sticky=E)
	addtype = ttk.Combobox(add,values=comtype,state='readonly',textvariable=typeadd,font='Arial 16',width=17).grid(row=1,column=1,pady=3,sticky=W)
	
	cabadd = StringVar()
	cab = ttk.Label(add,text='Кабинет:', font='Arial 16',anchor='e').grid(row=2,column=0,padx=5,sticky=E)
	addcab = ttk.Combobox(add, values=comcab,state='readonly',textvariable=cabadd,font='Arial 16',width=17).grid(row=2,column=1,sticky=W)
	
	statusadd = StringVar()
	status = ttk.Label(add,text='Статус:', font='Arial 16',anchor='e').grid(row=3,column=0,padx=5,sticky=E,pady=3)
	addstatus = ttk.Combobox(add,values=comstatus,state='readonly',textvariable=statusadd,font='Arial 16',width=17).grid(row=3,column=1,pady=3,sticky=W)
	
	dateregadd = StringVar()
	datereg = ttk.Label(add,text='Дата на учете:', font='Arial 16',anchor='e').grid(row=4,column=0,padx=5,sticky='EN')
	adddatereg = Calendar(add,background='#41ABE9',textvariable = dateregadd).grid(row=4,column=1)

	faddstr = partial(addstr,numberadd,typeadd,cabadd,statusadd,dateregadd,add) 
	btnadd = ttk.Button(add,text='Добавить',style = "Bold.TButton",command=faddstr).grid(row=5, column=1,sticky='ES', pady=10)


def select(sqlobj,sqlist,obj):
	curr = ''
	with sqlite3.connect('server.db') as con:
		cur = con.cursor()
		qsql = 'SELECT id,{obj} FROM {list}'.format(obj=sqlobj,list=sqlist)
		cur.execute(qsql)
		lendth = len(cur.fetchall())
		cur.execute(qsql)
		for i in range(0,lendth):
			x = cur.fetchone()
			if x[1] == obj:
				curr = x[0]
				break
	return curr


def addstr(numberadd,typeadd,cabadd,statusadd,dateregadd,add):
	number = numberadd.get()

	type = typeadd.get()
	cab = int(cabadd.get()) 
	status = statusadd.get()
	
	datereg = dateregadd.get()
	datechng = date()

	type = select('typetext','typelist',type)
	cab = select('number', 'cabinet', cab)
	status = select('statustext', 'statuslist', status)
	
	

	templist = [number,type,cab,status,datereg,datechng]
	for x in templist:
		if x == '':
			messagebox.showinfo('Ошибка','Введите все данные')
			break
	with sqlite3.connect('server.db') as con:
		cur = con.cursor()
		try:
			cur.execute('''INSERT INTO list (inventNum, type, cab, status, dataEdit, dataRegistration)
						VALUES(?, ?, ?, ?, ?, ?)''',templist)
			con.commit()
			messagebox.showinfo('Успешно', 'Элемент добавлен')
		except:
			messagebox.showinfo('Ошибка', 'Введите верные данные')
	add.destroy()
	sleep(1)
	mainmenu()
	

def deleteFrame():
	delete = Toplevel(root)
	w = 400
	h = 400
	size(w,h,delete)
	delete.grid()
	numberdelete=StringVar()
	num = ttk.Label(delete,text='Номер:', font='Arial 16',anchor='e').grid(row=0,column=0,padx=5,sticky=E)
	addnum = ttk.Entry(delete, font='Arial 16',textvariable=numberdelete,width=18).grid(row=0,column=1,sticky=W)
	fdeletestr = partial(deletestr, numberdelete, delete)
	btndelete = ttk.Button(delete,text='Удалить',style = "Bold.TButton",command=fdeletestr).grid(row=1, column=1,sticky='ES', pady=10)


def deletestr(number, delete):
	number = number.get()
	with sqlite3.connect('server.db') as con:
		cur = con.cursor()
		try:
			cur.execute(f'DELETE FROM list WHERE inventNum = {number}')
			messagebox.showinfo('Успешно', 'Элемент удален')
		except:
			messagebox.showinfo('Ошибка', 'Введите верный номер')
	delete.destroy()
	sleep(1)
	mainmenu()

def selectFrame():
	select = Toplevel(root)
	w = 800
	h = 400
	size(w,h,select)
	select.grid()
	comtype = []
	comlist(comtype,typelist)
	comstatus = []
	comlist(comstatus,statuslist)
	comcab = []
	comlist(comcab,cablist)

	lbldate = ttk.Label(select,text='Дата',font='Arial 16').grid(row=0,column=0,columnspan=2,pady=(20,0))
	fselectstartdate = StringVar()
	selectstartdate= Calendar(select,background='#41ABE9',textvariable = fselectstartdate).grid(row=1,column=0,padx=10,pady=5)
	fselectfinishdate = StringVar()
	selectfinishdate = Calendar(select,background='#41ABE9',textvariable = fselectfinishdate).grid(row=1,column=1,pady=5)

	
	
	type = ttk.Label(select,text='Тип', font='Arial 16').grid(row=0,column=2,columnspan=6,pady=(25,0))
	listtype = Listbox(select,font='Arial 16',height=6)

	for type in comtype:
		listtype.insert(END, type)
	
	listtype.grid(column=2,row=1, columnspan=5, rowspan=1,padx=(25,0),pady=(5,0))
	scrolltype = ttk.Scrollbar(select)
	listtype.config(yscrollcommand=scrolltype.set)
	scrolltype.config(command=listtype.yview)
	scrolltype.grid(column=7, row=1, rowspan=2,  sticky=S+N+W,pady=(5,0))

	cab = ttk.Label(select,text='Кабинет', font='Arial 16').grid(row=3,column=0,columnspan=1,pady=(5,0))
	listcab = Listbox(select,font='Arial 16',height=4,width=8)

	for cab in comcab:
		listcab.insert(END, cab)
	
	listcab.grid(column=0,row=4, rowspan=1,padx=(80,0),pady=(15,0),sticky=W)
	scrollcab = ttk.Scrollbar(select)
	listcab.config(yscrollcommand=scrollcab.set)
	scrollcab.config(command=listcab.yview)
	scrollcab.grid(column=0, row=4, rowspan=2,  sticky=S+N,pady=(15,0),padx=(85,0))

	status = ttk.Label(select,text='Кабинет', font='Arial 16').grid(row=3,column=1,columnspan=1,pady=(5,0))
	liststatus = Listbox(select,font='Arial 16',height=4,width=9)

	for status in comstatus:
		liststatus.insert(END, status)
	
	liststatus.grid(column=1,row=4, rowspan=1,padx=(70,0),pady=(15,0),sticky=W)
	scrollstatus = ttk.Scrollbar(select)
	liststatus.config(yscrollcommand=scrollstatus.set)
	scrollstatus.config(command=liststatus.yview)
	scrollstatus.grid(column=1, row=4, rowspan=2,  sticky=S+N,pady=(15,0),padx=(110,0))

	btn = ttk.Button(select,text='Сделать запрос',style = "Bold.TButton").grid(column=6,row=4,sticky=S+E)


def clearFrame():
	for widget in main.winfo_children():
		widget.destroy()
	plabel  = ttk.Label(main,text='').grid(row=0,column=0)
	num      = ttk.Label(main, text='Номер', font='Arial 16',background='#fff', width=12).grid(row=1, column=0, sticky=W,padx=2)
	type    = ttk.Label(main,text='Тип',font='Arial 16',background='#fff',  width=10).grid(row=1, column=1, sticky=W)
	cab     = ttk.Label(main,text='Кабинет', font='Arial 16', background='#fff',width=7).grid(row=1, column=2, sticky=W, padx=2)
	status  = ttk.Label(main,text='Статус', font='Arial 16',  background='#fff',width=7).grid(row=1, column=3, sticky=W)
	data    = ttk.Label(main, text='Дата изменения', font='Arial 16',background='#fff', width=14).grid(row=1, column=4, sticky=W, padx=2)

	# btnall = ttk.Button(main,text='Вся база', width=11,style = "Bold.TButton", command=mainmenu).grid(row=1,column=6,sticky=E, padx=5)
	# ftypebtn1 = partial(typebtn,'type', 1)
	# btntype1 = ttk.Button(main,text='Компьютеры', width=11,style = "Bold.TButton", command=ftypebtn1).grid(row=2,column=6,sticky=E, padx=5)
	# ftypebtn2 = partial(typebtn,'type',2)
	# btntype2 = ttk.Button(main,text='Ноутбуки', width=11,style = "Bold.TButton", command=ftypebtn2).grid(row=3,column=6,sticky=E,padx=5)
	# fstatus1 = partial(typebtn,'status',1)
	# btnstatus1 = ttk.Button(main,text='Активно', width=11,style = "Bold.TButton", command=fstatus1).grid(row=4,column=6,sticky=E,padx=5)
	# fstatus2 = partial(typebtn,'status',2)
	# btnstatus1 = ttk.Button(main,text='Архив', width=11,style = "Bold.TButton", command=fstatus2).grid(row=4,column=6,sticky=E,padx=5)
	btnadd = ttk.Button(main,text='Добавить', width=9,style = "Bold.TButton",command=addFrame).grid(row=17,column=0,sticky=E,padx=2,pady=5)
	btndelete = ttk.Button(main,text='Удалить', width=9,style = "Bold.TButton",command=deleteFrame).grid(row=17,column=1,sticky=W,pady=5,padx=4)
	btnselect = ttk.Button(main,text='Выбор', width=9, style = "Bold.TButton", command=selectFrame).grid(row=17,column=2,columnspan=2,sticky=W,pady=5)




def view(i,*x):
	if i % 2 == 0:
		num    = ttk.Label(main,text=x[0],font='Arial 16',background='#b3b4bc',width=12,anchor='w').grid(row=i,column=0,sticky=W,pady=5,padx=2)
		type   = ttk.Label(main,text=x[1],font='Arial 16',background='#b3b4bc',width=10).grid(row=i,column=1,sticky=W,pady=5)
		cab    = ttk.Label(main,text=x[2],font='Arial 16',background='#b3b4bc',width=7,anchor='w').grid(row=i,column=2,sticky=W,pady=5,padx=2)
		status = ttk.Label(main,text=x[3],font='Arial 16',background='#b3b4bc',width=7).grid(row=i,column=3,sticky=W,pady=5)
		data   = ttk.Label(main,text=x[4],font='Arial 16',background='#b3b4bc',width=14).grid(row=i,column=4,sticky=W,pady=5,padx=2)
	else:
		num    = ttk.Label(main,text=x[0],font='Arial 16',background='#b3b4bc',width=12,anchor='w').grid(row=i,column=0,sticky=W,padx=2)
		type   = ttk.Label(main,text=x[1],font='Arial 16',background='#b3b4bc',width=10).grid(row=i,column=1,sticky=W)
		cab    = ttk.Label(main,text=x[2],font='Arial 16',background='#b3b4bc',width=7,anchor='w').grid(row=i,column=2,sticky=W,padx=2)
		status = ttk.Label(main,text=x[3],font='Arial 16',background='#b3b4bc',width=7).grid(row=i,column=3,sticky=W)           
		data   = ttk.Label(main,text=x[4],font='Arial 16',background='#b3b4bc',width=14).grid(row=i,column=4,sticky=W,padx=2)


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
	nextbtn = ttk.Button(main,text='next -->',style = "Bold.TButton",width=7,command=nextstring).grid(row=17,column=4,sticky=E)


def prevbtn(already):
	prevstring = partial(prevstr, already)
	prevbtnn = ttk.Button(main,text='<-- prev',style = "Bold.TButton",width=7,command=prevstring).grid(row=17,column=3,sticky=W)


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
		qlen = qstr - 15
		if qstr < len(cur.fetchall()):
			clearFrame()
			cur.execute(sql)
			i=2
			for j in range(0,qlen-15):
				x = cur.fetchone()
			for x in range(qlen,qstr):
				x = cur.fetchone()
				view(i,*x)
				i+=1
				qstr-=1
		
			nextbtn(qstr)
			if qstr != 15: prevbtn(qstr)
			

		else:
			clearFrame()
			cur.execute(sql)
			i=2
			for j in range(0,qlen):
				x = cur.fetchone()

			list = cur.fetchall()
			for x in list:
				view(i,*x)      
				i+=1
			qstr = qstr - (qstr % 15)
			nextbtn(qstr)
			prevbtn(qstr)
	


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