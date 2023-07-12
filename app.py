from flask import Flask, render_template, url_for, flash, redirect
from tests.forms import RegistrationForm
from flask_behind_proxy import FlaskBehindProxy
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
proxied = FlaskBehindProxy(app)
               
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


@app.route("/")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')
    
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
    app.run(debug=True, host="0.0.0.0", port = 5001)