'''
Checking if the new color API works

'''
import requests
import pprint
import random

rand_color = random.choices(range(256), k=3)
rgb_vals = str(rand_color[0]) + ',' + str(rand_color[1]) + ',' + str(rand_color[2])
url = 'https://www.thecolorapi.com/scheme?rgb=' + rgb_vals

response = requests.get(url).json()

# Print urls of 5 random monochromatic colors
for i in range(5):
    pprint.pprint(response['colors'][i]['image']['bare'])