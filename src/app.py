from flask import Flask, redirect, render_template, request, url_for, session
from flask_mysqldb import MySQL
import yaml, hashlib

app = Flask(__name__, static_folder="static", static_url_path="/static/")
app.secret_key = b'_5.y2l"F4Q5z%P\xEc]/'

db = yaml.load(open('db.yaml'), Loader=yaml.BaseLoader)
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)

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
		# TODO calcolare saldo dal database
		return render_template('reserved.html', saldo=1460)


@app.route('/insert', methods=['POST'])
def insert():
	# TODO insert data into db then redirect to reserved
    return	redirect('/reserved')


if __name__ == "__main__":
    app.run(debug=True)