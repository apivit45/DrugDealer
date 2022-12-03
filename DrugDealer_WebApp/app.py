from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
app.config['SECRET_KEY'] = "Never push this line to github public repo"

cred = yaml.load(open('cred.yaml'), Loader=yaml.Loader)
app.config['MYSQL_HOST'] = cred['mysql_host']
app.config['MYSQL_USER'] = cred['mysql_user']
app.config['MYSQL_PASSWORD'] = cred['mysql_password']
app.config['MYSQL_DB'] = cred['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route("/")
def index():
	return render_template("index.html")

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        loginForm = request.form
        username = loginForm['username']
        cur = mysql.connection.cursor()
        queryStatement = f"SELECT * FROM employee WHERE username = '{username}'"
        numRow = cur.execute(queryStatement)
        if numRow > 0:
            user =  cur.fetchone()
            if check_password_hash(user['password'], loginForm['password']):
                # Record session information
                session['login'] = True
                session['username'] = user['username']
                session['userroleid'] = str(user['role_id'])
                session['firstName'] = user['firstname']
                session['lastName'] = user['lastname']
                session['tel'] = user['employee_tel']
                session['email'] = user['email']
                print(session['username'] + " roleid: " + session['userroleid'] + " email: " + session['email'] + " phone number: " + session['tel'])
                flash('Welcome ' + session['firstName'], 'success')
                #flash("Log In successful",'success')
                return redirect('/')
            else:
                cur.close()
                flash("Password doesn't match", 'danger')
        else:
            cur.close()
            flash('User not found', 'danger')
            return render_template('login.html')
        cur.close()
        return redirect('/')
    return render_template('login.html')

@app.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        userDetails = request.form
        
         # Check the password and confirm password
        if userDetails['password'] != userDetails['confirm_password']:
            flash("Passwords do not match!", "danger")
            return render_template('register.html')
        p1 = userDetails['username']
        p2 = userDetails['password']
        p3 = userDetails['first_name']
        p4 = userDetails['last_name']
        p5 = userDetails['email']
        p6 = userDetails['tel']
        
        hashed_pw = generate_password_hash(p2)
        
        print(p1 + "," + p2 + "," + hashed_pw + "," + p3 + "," + p4 + "," + p5 + "," + p6)
        
        queryStatement = (
            f"INSERT INTO "
            f"employee(username, password, firstname, lastname, email, employee_tel, role_id) "
            f"VALUES('{p1}', '{hashed_pw}', '{p3}', '{p4}', '{p5}', '{p6}', 1)"
        )
        print(check_password_hash(hashed_pw, p2))
        print(queryStatement)
        cur = mysql.connection.cursor()
        cur.execute(queryStatement)
        mysql.connection.commit()
        cur.close()
        
        flash("Form Submitted Successfully.", "success")
        return redirect('/')    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out", 'info')
    return redirect('/')

if __name__ == '__main__':
	app.run(debug=True)