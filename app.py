from flask import Flask, render_template, url_for, request
import requests
import random
import re

import random, requests

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


@app.route("/personalized", methods=['GET', 'POST'])
def personalized_page():
        if request.method == 'POST':
         # Get color input from form
            color_input = request.form['color_input']

         # Remove any whitespace and convert to lowercase
            color_input = color_input.replace(" ", "").lower()

#         # Check if the color input is in RGB format
        if re.match(r'^\d{1,3},\d{1,3},\d{1,3}$', color_input):
#             # Extract the RGB values from the input string
            rgb_values = color_input.split(',')

#             # Convert RGB values to integers
            r, g, b = map(int, rgb_values)

#             # Make API request to generate color palette based on the RGB values
            url = f'https://www.thecolorapi.com/scheme?rgb={r},{g},{b}'
            response = requests.get(url).json()

#             # Check if the API response contains 'colors' key
            if 'colors' in response:
                # Extract color values from the API response
                colors = []
                for i in range(5):
                    color = response['colors'][i]['hex']['value']
                    colors.append(color)

        return render_template('personalized.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator', colors=colors)
@app.route("/history")
def history_page():
    return render_template('history.html', subtitle='History', text='This is the History page')

@app.route("/favorites")
def favorites_page():
    return render_template('favorites.html', subtitle='Favorites', text='This is the Favorites page')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
