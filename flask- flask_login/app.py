from flask import Flask, flash, render_template, url_for, redirect, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_bcrypt import Bcrypt
from disc_space import storage_graph
import base64
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite"
app.config["SECRET_KEY"] = "grafisk_design"

db = SQLAlchemy()

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt=Bcrypt(app)

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


@app.route('/register', methods=["GET", "POST"])
def register():
	if request.method == "POST":
		hashed_password = bcrypt.generate_password_hash(request.form.get("password")).decode('utf-8')
		user = Users(username=request.form.get("username"), password=hashed_password)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("frontpage"))
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
			return redirect(url_for("frontpage"))
		else:
			flash('Incorrect username or password')
	return render_template("login.html")


@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for("home"))

@app.route("/frontpage")
def frontpage():
	return render_template("base.html")

@app.route("/storage")
def storage():
	buf = storage_graph()
	img_str = base64.b64encode(buf.getvalue()).decode('utf-8')
	return render_template("storage.html", storage_graph_base64=img_str)
	



@app.route("/")
def home():
	return render_template("authentication.html")


if __name__ == "__main__":
	app.run(debug=True)


