from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
# from forms import LoginForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length, Email, EqualTo
from flask_behind_proxy import FlaskBehindProxy
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
app.config['SECRET_KEY'] = '53046ce2de3a349d31131737702b9825'


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
    return render_template('random.html', subtitle='Random Palette Generator', text='This is the Random Palette Generator')

@app.route("/personalized")
def personalized_page():
    return render_template('personalized.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator')

@app.route("/history")
def history_page():
    return render_template('history.html', subtitle='History', text='This is the History page')

@app.route("/favorites")
def favorites_page():
    return render_template('favorites.html', subtitle = 'Favorites', text = 'This is the Favorites page')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)