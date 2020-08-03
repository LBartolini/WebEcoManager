from flask import Flask, redirect, render_template, request, url_for
from flask_mysqldb import MySQL
import yaml, hashlib

app = Flask(__name__, static_folder="static", static_url_path="/static/")

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
    return render_template('home.html')

@app.route('/reserved', methods=['POST'])
def reserved():
    return render_template('reserved.html')


if __name__ == "__main__":
    app.run(debug=True)