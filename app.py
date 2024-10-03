from flask import Flask, render_template, redirect, request, flash, url_for, session
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
import os

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.secret_key = 'dm95YWdld29yZGNvd2JveXJlbGF0aW9uc2hpcHJvY2t5ZGVzY3JpYmVjbG91ZHRyZWU='
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(200), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #string format result
    def __repr__(self) -> str:
        return f"User {self.id}"

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    major = db.Column(db.String(200), nullable=False)
    scholarship = db.Column(db.String(100), nullable=False)  # Corrected here
    amount = db.Column(db.Integer, nullable=False, default=0)
    details = db.Column(db.String(100), nullable=True)

    def __repr__(self) -> str:
        return f"Student {self.id}"

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        hashed_password = generate_password_hash(password)

        new_user = Users(username=username, password_hash=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()

        # flash('Registration successful! You can now log in.', 'success')
        session['success_message'] = "Registration successful!"
        return redirect(url_for('index'))
    return render_template("register.html", form=form)

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Login')


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            session['success_message'] = "Login successful!"
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    session['success_message'] = "You have been logged out successfully."
    return redirect(url_for('index'))


#default route
@app.route("/")
def index():
    return render_template("index.html")


#runner and debugger
if __name__ in "__main__":
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 5001))
    app.run(host='0.0.0.0',port=port, debug=True)
