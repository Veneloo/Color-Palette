from flask import Flask
from flask import render_template

app = Flask(__name__)                    

@app.route("/")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')
    
@app.route("/random")
def random_page():
    return render_template('random_page.html', subtitle='Random Palette Generator', text='This is the Random Palette Generator')

@app.route("/personalized")
def personalized_page():
    return render_template('personalized_page.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator')

@app.route("/history")
def history_page():
    return render_template('history_page.html', subtitle='History', text='This is the History page')

@app.route("/favorites")
def favorites_page():
    return render_template('favorites_page.html', subtitle = 'Favorites', text = 'This is the Favorites page')

  
if __name__ == '__main__':               
    app.run(debug=True, host="0.0.0.0")