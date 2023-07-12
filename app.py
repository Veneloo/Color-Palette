from flask import Flask, render_template, url_for, request
import requests
import pprint
import random

app = Flask(__name__)                    

@app.route("/")
@app.route("/welcome")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')
    
@app.route("/random")
def random_page():
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