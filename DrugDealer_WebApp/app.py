import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
import mysql.connector

mydb = mysql.connector.connect(
	host='localhost',
	username='root',
	password='',
	port=3306
)

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

if __name__ == '__main__':
	app.run(debug=True)