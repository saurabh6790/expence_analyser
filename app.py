from flask import Flask, render_template,  request, redirect, url_for
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'expence_analyzer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

	
@app.route("/", methods=["GET", "POST"])
def login():
	error = ''
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connect().cursor()
		print """select `username` from Auth where `username`='{0}'
			and `pwd`=password('{1}')""".format(username, password)
		cursor.execute("""select `username` from Auth where `username`='{0}'
			and `pwd`=password('{1}')""".format(username, password))
		data = cursor.fetchone()
		print data
		if data is None:
			error = "Username or Password is wrong"
		else:
			return render_template("welcome.html")
	
	return render_template("login.html", error=error)

@app.route("/signup.html", methods=["GET", "POST"])
def signup():
	if request.method == "POST":
		cursor = mysql.connect().cursor()
		cursor.execute("""insert into `User` values('{0}', '{1}', '{2}', '{3}') 
			""".format(request.form['username'], request.form['first_name'], request.form['last_name'], request.form['mobile_no']))
		cursor.execute("""insert into Auth values('{0}', password('{1}')) 
			""".format(request.form['username'], request.form['password']))
		cursor.execute("commit")
		return login()
	return render_template("signup.html")
	
if __name__ == "__main__":
	app.run(debug=True)