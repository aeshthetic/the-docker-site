from flask import Flask
from flask import request, render_template, flash, redirect, url_for
from werkzeug.urls import url_parse
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, current_user, login_user, logout_user
from itsdangerous import URLSafeTimedSerializer
from mail import send_mail
from config import BaseConfig


app = Flask(__name__)
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
login = LoginManager(app)
login.login_view = "login"


# pylint: disable=wrong-import-position
from models import Member


def generate_confirmation_link(user_email):
    confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return url_for("confirm",
                   token=confirm_serializer.dumps(user_email, salt="email-confirmation-salt"),
                   external=True)


def send_confirmation_email(user_email):
    send_mail(user_email,
              "Confirm your Docker account",
              f"Thanks for signing up to become a member of the Docker! "
              f"Follow this link to confirm your account: {generate_confirmation_link(user_email)}")


@app.route('/', methods=['GET'])
def index():
    member_count = Member.query.filter_by(confirmed=True).count()
    return render_template('index.html', member_count=member_count)


@app.route('/join', methods=['GET', 'POST'])
def join():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        country = request.form['country']
        password = request.form['password']
        member = Member(first_name, last_name, email, password, country)
        db.session.add(member)
        db.session.commit()
        send_confirmation_email(member.email)
        flash("nice meme", "success")
        return redirect("/")
    return render_template('join.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect("/")

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        member = Member.query.filter_by(email=email).first()
        if member is None or not member.check_password(password) or not member.confirmed:
            flash("Account not found or confirmed, or password is incorrect")
            return redirect("/login")
        login_user(member)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = "/"
        return redirect(next_page)
    return render_template("login.html")


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/login")


@app.route('/confirm/<token>')
def confirm(token):
    try:
        confirm_serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        email = confirm_serializer.loads(token, salt='email-confirmation-salt', max_age=3600)
    except:
        return render_template("confirmed.html", success=False)
    member = Member.query.filter_by(email=email).first()

    if member.confirmed:
        flash("Account already confirmed, please log in", "info")
    else:
        member.confirmed = True
        db.session.add(member)
        db.session.commit()
        return render_template("confirmed.html", success=True)
    return render_template("confirmed.html", success=True)


@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')


if __name__ == '__main__':
    app.run()
