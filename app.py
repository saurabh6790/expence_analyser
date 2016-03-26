from flask import Flask, render_template, url_for, request, redirect
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'password'
app.config['MYSQL_DATABASE_DB'] = 'expence_analyzer'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route("/")
def home():
	return render_template("welcome.html")
	
@app.route("/login", methods=["GET", "POST"])
def login():
	error = None
	if request.method == "POST":
		username = request.form['username']
		password = request.form['password']
		cursor = mysql.connect().cursor()
		print """select `username` from Auth where `username`='{0}'
			and `pwd`=password('{1}')""".format(username, password)
		cursor.execute("""select `username` from Auth where `username`='{0}'
			and `pwd`=password('{1}')""".format(username, password))
		data = cursor.fetchone()
		if data is None:
			error = "Username or Password is wrong"
		else:
			return render_template("welcome.html")
	
	return render_template("login.html", error=error)
	
	
if __name__ == "__main__":
	app.run(debug=True)