from flask import Flask, flash, render_template, request, url_for, redirect
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from recent_files import Recent_Files 
from daily_changes import Daily_Changes
from disc_space import Storage

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.sqlite"
app.config["SECRET_KEY"] = "grafisk_design"
db = SQLAlchemy()

#directory_location = ("D:/GrafiskDesign")
#filechange_db_location = ("C:/Users/Administrator/Desktop/Dashboard/database/daily_filechanges.sqlite")

directory_location = ("C:/Users/Lau/Music")
filechange_db_location = ("C:/Users/Lau/Documents/GitHub/FirstYearProject/Dashboard/database/daily_filechanges.sqlite")

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)

class Users(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(250), unique=True, nullable=False)
	password = db.Column(db.String(250), nullable=False)

db.init_app(app)
with app.app_context():
	db.create_all()

@login_manager.user_loader
def loader_user(user_id):
	return Users.query.get(user_id)

@app.route("/")
def home():
	return redirect(url_for("login"))

@app.route("/index")
@login_required
def index():
    recent_file_list = Recent_Files(directory_location, 100)
    files_returned = recent_file_list.list_recent_files()
	
    graph = Daily_Changes(filechange_db_location, directory_location, 7)
    graph.log_changes()
    graph = graph.daily_changes_graph()

    return render_template('index.html', files = files_returned, graph = graph)

@app.route("/storage")
@login_required
def storage():
	log_storage = Daily_Changes(filechange_db_location, directory_location, 7)
	log_storage.log_changes()

	storage_data = Storage(filechange_db_location, directory_location)

	pi_chart = storage_data.storage_graph()
	days_to_full = storage_data.days_to_full()

	return render_template('storage.html', pi_chart = pi_chart, days_to_full = days_to_full)

@app.route('/register', methods=["GET", "POST"])
@login_required
def register():
	if request.method == "POST":
		hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
		user = Users(username=request.form.get("username"), password=hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("index"))
	return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = Users.query.filter_by(
			username=request.form.get("username")).first()
		if user is None:
			flash("user does not exist")
			return render_template("login.html")
		if bcrypt.check_password_hash(user.password, request.form.get("password")):
			login_user(user)
			return redirect(url_for("index"))
		else:
			flash('Incorrect username or password')
	return render_template("login.html")

@app.route("/authentication")
def authentication():
	return render_template("authentication.html")

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("authentication"))

@app.errorhandler(401)
def page_not_found(e):
    return redirect(url_for("authentication"))

if __name__ == '__main__':
    app.run(debug=True)