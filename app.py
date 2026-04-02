from flask import Flask, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import json


app = Flask(__name__)
app.secret_key = "secret"
login_manager = LoginManager()
login_manager.init_app(app)


def save_json(users):
	with open('users.json', 'w') as f:
		json.dump(users, f, indent=4)

def load_json():
	with open('users.json') as f:
		return json.load(f)


users = load_json()


class User(UserMixin):
	def __init__(self, username):
		self.id = username
		self.password = users[username]['password']
		self.balance = users[username]['balance']


@login_manager.user_loader
def load_users(username):
	if username in users:
		return User(username)
	return None


@app.route('/')
@app.route('/home')
def home():
	return 'here should be some stuff...'

@app.route('/lottery/<lottery_id>')
def lottery(lottery_id):
	return f'{lottery_id}'

@app.route('/register', methods=['GET', 'POST'])
def register():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		if username in users:
			flash("Username already exists")
			return redirect(url_for('register'))

		users[username] = {"password": password, "balance": 0}
		save_json(users)
		return "successfully registred"
	return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		if username in users:
			if users[username]['password'] == password:
				user = User(username)
				login_user(user)
				return "Success!!!"
		flash("ERROR")
	return render_template('login.html')


@app.route('/profile')
@login_required
def profile():
	return f"youre logged in as {current_user.id}, your balance is {current_user.balance}"


if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=80)
