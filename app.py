from flask import Flask, render_template, url_for, request
import random, requests

app = Flask(__name__)

@app.route("/")
@app.route("/welcome")
def welcome_page():
    return render_template('welcome.html', subtitle='Welcome Page', text='This is the welcome page')

@app.route("/random", methods=['GET', 'POST'])
def random_page():
    if request.method == 'POST':
        # Generate random RGB values
        rand_color = random.choices(range(256), k=3)
        rgb_vals = str(rand_color[0]) + ',' + str(rand_color[1]) + ',' + str(rand_color[2])

        # Make API request to generate color palette
        url = 'https://www.thecolorapi.com/scheme?rgb=' + rgb_vals
        response = requests.get(url).json()

        # Extract color values from the API response
        colors = []
        for i in range(5):
            color = response['colors'][i]['hex']['value']
            colors.append(color)

        return render_template('random.html', subtitle='Random Palette Generator', text='This is the Random Palette Generator', colors=colors)

    return render_template('random.html', subtitle='Random Palette Generator', text='This is the Random Palette Generator', colors=None)

@app.route("/personalized")
def personalized_page():
    return render_template('personalized.html', subtitle='Personalized Palette Generator', text='This is the Personalized Palette Generator')

@app.route("/history")
def history_page():
    return render_template('history.html', subtitle='History', text='This is the History page')

@app.route("/favorites")
def favorites_page():
    return render_template('favorites.html', subtitle='Favorites', text='This is the Favorites page')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5001)
