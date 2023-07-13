import os
import requests
import random
import re
from flask import Flask, render_template, url_for, flash, redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_behind_proxy import FlaskBehindProxy
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required

app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'super secret key'
Session(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

# Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables
with app.app_context():
    db.create_all()

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
        
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')
        
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('Username does not exist. Create an account')

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    color = db.Column(db.String(7), nullable=False)
    one = db.Column(db.String(50), nullable=False)
    two = db.Column(db.String(50), nullable=False)
    three = db.Column(db.String(50), nullable=False)
    four = db.Column(db.String(50), nullable=False)
    five = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Favorite('{self.color}', '{self.one}', '{self.two}', '{self.three}', '{self.four}', '{self.five}')"


@app.route("/")
@app.route("/welcome")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('welcome_page'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        login_user(user)
        return redirect(url_for('welcome_page'))

    return render_template('register.html', title='Register', form=form)

from flask_login import login_user

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('welcome_page'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash(f'Welcome Back {form.username.data}!', 'success')
            return redirect(url_for('welcome_page'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html', title='Log In', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect("/")


@app.route("/random")
def random_page():
    if request.method == 'POST':
    #     # Generate random RGB values
         rand_color = random.choices(range(256), k=3)
         rgb_vals = str(rand_color[0]) + ',' + str(rand_color[1]) + ',' + str(rand_color[2])

    #     # Make API request to generate color palette
         url = 'https://www.thecolorapi.com/scheme?rgb=' + rgb_vals
         response = requests.get(url).json()
  # Extract color values from the API response
         colors = []
         for i in range(5):
             color = response['colors'][i]['hex']['value']
             colors.append(color)
    return render_template('random.html', subtitle='Random Palette Generator', text='This is the Random Palette Generator')


@app.route('/result', methods=['POST'])
def process():
    color = request.form['colorPicker']
    mode = request.form["mode-choice"]
    colorurl = f"https://www.thecolorapi.com/id?format=svg&named=false&hex={color[1:]}"
    url = f"https://www.thecolorapi.com/scheme?hex={color[1:]}&mode={mode}"

    response = requests.get(url).json()

# Print urls of 5 random monochromatic colors
    result = []
    for i in range(5):
        result.append(response['colors'][i]['image']['bare'])
    one = result[0]
    two = result [1]
    three = result[2]
    four = result [3]
    five = result[4]
  
    
    return render_template('result.html', result=result, 
                           colorurl = colorurl, one = one, 
                           two = two, three = three, four = four, five = five)


@app.route("/personalized", methods=['GET', 'POST'])
def personalized_page():
    if request.method == 'POST':
        # Get color input from form
        color_input = request.form['color_input']

        # Check if the color input starts with "#"
        if color_input.startswith("#"):
            # Make API request to generate color palette based on user input
            url = 'https://www.thecolorapi.com/scheme?hex=' + color_input[1:]  # Exclude the "#" symbol
            response = requests.get(url).json()

            # Check if the API response contains 'colors' key
            if 'colors' in response:
                # Extract color values from the API response
                colors = []
                for i in range(5):
                    color = response['colors'][i]['hex']['value']
                    colors.append(color)

                return render_template('personalized.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator', colors=colors)

    return render_template('personalized.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator', colors=None)

@app.route('/history', methods=['GET', 'POST'])



@app.route('/favorites', methods=['GET', 'POST'])
@login_required
def favorites_page():
    if request.method == 'POST':
        color = request.form['color']
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']
        four = request.form['four']
        five = request.form['five']

        favorite = Favorite(color=color, one=one, two=two, three=three, four=four, five=five, user_id=current_user.id)
        db.session.add(favorite)
        db.session.commit()

        flash('Colors added to favorites!', 'success')
        return redirect(url_for('favorites_page'))

    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    return render_template('favorites.html', subtitle='Favorites', text='This is the Favorites page', favorites=favorites)



@app.route('/clear-favorites', methods=['POST'])
def clear_favorites():
    session.pop('favorites', None)
    flash('Favorites cleared!', 'success')
    return redirect(url_for('favorites_page'))





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
