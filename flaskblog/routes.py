from flask import render_template, url_for, flash, redirect,request
from flaskblog import app,bcrypt,db
from flaskblog.forms import RegistrationForm, LoginForm,UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user,current_user,logout_user,login_required

posts = [
    {
        'author': 'Corey',
        "title": "Post 1",
        'content': 'First content',
        'date_posted': 'April 20,2020'
    },
    {
        'author': 'Pavan',
        "title": "Post 2",
        'content': 'Second content',
        'date_posted': 'April 22,2020'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/about")
def about():
    return render_template("about.html", title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data,email = form.email.data,password = hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created ", 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Register", form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Unsuccessful Login .Proper shit please", 'danger')

    return render_template('login.html', title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static',filename="profile_pics/" + current_user.image_file)
    return render_template('account.html', title="Account",image_file=image_file,form=form )
