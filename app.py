from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os


app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
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
