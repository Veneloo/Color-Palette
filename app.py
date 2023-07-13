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
app = Flask(__name__)
proxied = FlaskBehindProxy(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['SECRET_KEY'] = 'super secret key'
# app.config['SECRET_KEY'] = '53046ce2de3a349d31131737702b9825'
Session(app)


# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"
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
        if user is None:
            raise ValidationError('Username does not exit. Create an account')

@app.route("/")
@app.route("/welcome")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('welcome_page'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    session.clear()
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Welcome Back {form.username.data}!', 'success')
        return redirect(url_for('welcome_page'))
    return render_template('login.html', title='Log In', form=form)

@app.route("/logout")
def logout():
    db.session.clear()
    return redirect("/")

# Rest of the routes...
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
def history_page():


@app.route('/favorites', methods=['GET', 'POST'])
def favorites_page():
    if request.method == 'POST':
        color = request.form['color']
        one = request.form['one']
        two = request.form['two']
        three = request.form['three']
        four = request.form['four']
        five = request.form['five']
        
        if 'favorites' not in session:
            session['favorites'] = []
        
        session['favorites'].append({
            'color': color,
            'one': one,
            'two': two,
            'three': three,
            'four': four,
            'five': five
        })
        
        flash('Colors added to favorites!', 'success')
        return redirect(url_for('favorites_page'))
    
    return render_template('favorites.html', subtitle='Favorites', text='This is the Favorites page', favorites=session.get('favorites', []))


@app.route('/clear-favorites', methods=['POST'])
def clear_favorites():
    session.pop('favorites', None)
    flash('Favorites cleared!', 'success')
    return redirect(url_for('favorites_page'))





if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
