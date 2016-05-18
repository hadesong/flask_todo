#coding:utf-8
from todo import app  
from flask import render_template , redirect , session , g , request  , flash 
import sqlite3 , time

@app.route('/')
def redir():
	return redirect('/login')


@app.route('/index' , methods=['POST' , 'GET'])
def index():
	#if ('username' and 'password'  in session ) and session['username']
	if request.method == 'POST':
		text = request.form.get('todo')
		ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		#链接
		conn = sqlite3.connect('todo.db') 
		#创建表
		sql_create = '''
create table if not exists todolist
(id integer primary key autoincrement , todo text(50) , time integer  , state integer )
		'''
		conn.execute(sql_create)
		#插入数据
		sql_inser = '''
insert into todolist(todo , time , state)  values(? , ? , ?);
		'''
		if len(text) != 0:
			conn.execute(sql_inser , (text , ti , "1"))
			conn.commit()
			#return sql_inser
			return render_template('index.html'  , list = show())
		else:
			flash("Write something....")
			return render_template('index.html'  , list = show())

	return render_template('index.html'  , list = show())

#展示列表
def show():
	cur = None
	con = sqlite3.connect('todo.db')
		#创建表
	sql_create = '''
create table if not exists todolist
(id integer primary key autoincrement , todo text(50) , time integer  , state integer )
		'''
	con.execute(sql_create)
	sql_select = '''select * from todolist order by id desc '''
	cur = con.execute(sql_select)
	string = []
	for x in cur:
		string.append(x)
	return string

@app.route('/done/<id>' , methods=['POST' , 'GET'])
def done(id):
	id = int(id)
	conn = sqlite3.connect('todo.db')
	cur = conn.execute("select * from todolist where id=?" , (id,))
	context = []
	for x in cur:
		context.append(x)
	return render_template('index.html' , list = id)




@app.route('/modify/<id>' , methods=['POST' , 'GET'])
def modify(id):

	id = int(id)
	conn = sqlite3.connect('todo.db')
	cur = conn.execute("select * from todolist where id=?" ,  (id,))
	context = []
	for x in cur:
		context.append(x)
	if request.method == 'POST':
		newtodo = request.form.get('todo')
		ti = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
		sql_updata = '''
 update todolist set todo  = ? , time= ? where id = ? 
		'''
		conn.execute(sql_updata , (newtodo , ti,id ))
		conn.commit()
		return redirect("/")
	return render_template('modify.html' , list = cur , context=context)


@app.route('/delet/<id>' , methods=['POST' , 'GET'])
def delet(id):
	#id =str(id)
	if request.method == 'POST':
		conn = sqlite3.connect('todo.db')
		sql_delet = '''delete from todolist where id=?;'''
		conn.execute(sql_delet , (id,))
		conn.commit()
		return redirect('/index')
	return render_template('delet.html')



@app.route('/login' , methods=['POST' ,  'GET'])
def login():
	log_msg =""
	if request.method == 'POST':
		user = request.form.get('username')
		pawd = request.form.get('password')
		if user != 'hadesong':
			log_msg = 'UserName Error!!'
		elif pawd != '123456':
			log_msg = 'PassWord Error!!'
		else:
			session['username']=user
			session['password']=pawd
			return redirect('/index')
	return render_template('login.html' , log_msg = log_msg)