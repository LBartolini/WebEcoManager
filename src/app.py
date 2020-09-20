from flask import Flask, redirect, render_template, request, url_for, session
#from flask_mysqldb import MySQL # commented 'cause on mac i have no mysql server 
#import yaml
import sqlite3
import hashlib

app = Flask(__name__, static_folder="static", static_url_path="/static/")
app.secret_key = b'_5.y2l"F4Q5z%P\xEc]/'

'''
db = yaml.load(open('db.yaml'), Loader=yaml.BaseLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
'''

def calcola_saldo():
	con = sqlite3.connect('wem.db')
	transactions = [float(x[0]) for x in con.execute('select value from webecomanager')]
	saldo = sum(transactions)

	return saldo

def get_transactions():
	con = sqlite3.connect('wem.db')
	transactions = [x for x in con.execute('select value, descrizione from webecomanager')]

	return transactions


@app.route('/', methods=['GET'])
def entry():
    return redirect('/home')

@app.route('/home', methods=['GET'])
def home():
	if 'username' in session:
		session.pop('username', None)
	return render_template('home.html', saldo=-1)

@app.route('/reserved', methods=['GET', 'POST'])
def reserved():
	logged_in = False
	if request.method == 'GET':
		if 'username' in session:
			# already logged in
			logged_in = True
		else:
			return redirect('/home')
	else:
		# login authentication
		session['username'] = request.form['username']
		logged_in = True
    
	if logged_in:
		return render_template('reserved.html', saldo=calcola_saldo(), transazioni=get_transactions())
	else:
		redirect('/home')


@app.route('/insert', methods=['POST'])
def insert():
	form = [x for x in request.form.values()]
	try:	
		form[0] = abs(float(form[0]))
	except:
		redirect('/reserved')

	if len(form) != 3:
		#spesa
		form[0] *= -1
	
	if calcola_saldo() + form[0] >= 0:
		con = sqlite3.connect('wem.db')
		with con:
			con.execute('insert into webecomanager (value, descrizione) values (?, ?)', form[:2])

	return	redirect('/reserved')


if __name__ == "__main__":
    app.run(debug=True)