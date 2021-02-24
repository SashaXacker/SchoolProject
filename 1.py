import sqlite3
				# WHERE dataRegistration >= {start}
				# WHERE dataRegistration <= {finish}
sql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id
WHERE'''
datesql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id
                WHERE dataRegistration >= {start} and dataRegistration <= {finish}
                '''
qsql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id'''
newsql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id'''
selectsql = '''SELECT inventNum, typetext, cabinet.number, statustext, dataRegistration FROM list
				JOIN typelist ON list.type = typelist.id
				JOIN statuslist ON list.status = statuslist.id
				JOIN cabinet ON list.cab = cabinet.id
				WHERE list.cab = {cab} and list.status = {status} and list.type = {type}'''

cab=[1]
status=[1]
type = [3]
if cab == [] and status == [] and type == []:
    newsql = qsql
else:
    newsql = qsql + '\nWHERE'
    print(newsql)
    print(sql)
    if cab != []:
        if newsql == sql:
            newsql+= f' list.cab = {cab[0]}'
        else:
            newsql+= f' and list.cab = {cab[0]}'
    if status != []:
        if newsql == sql:
            newsql+= f' list.status = {status[0]}'
        else:
            newsql+= f' and list.status = {status[0]}'
    if type != []:
        if newsql == sql:
            newsql+= f' list.type = {type[0]}'
        else:
            newsql+= f' and list.type = {type[0]}'

with sqlite3.connect('server.db') as con:
    cur = con.cursor()
    datesql = datesql.format(start='')
    print(newsql)
    cur.execute(newsql)
    print(cur.fetchall())



