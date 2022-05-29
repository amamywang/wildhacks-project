from flask import Flask
from flask import render_template
from flask import request
import json
import os
import requests

from pprint import pprint

# initializes flask app:
app = Flask(__name__)

##############
# Exercise 1 #
##############
@app.route('/')
def main_page():
    return render_template("home.html")

@app.route('/breakfast.html')
def breakfast():
    return render_template("breakfast.html")

@app.route('/lunch.html')
def lunch():
    return render_template("lunch.html")

@app.route('/dinner.html')
def dinner():
    return render_template("dinner.html")

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/finish.html')
def finish():
    return render_template("finish.html")


##############
# Exercise 4 #
##############
@app.route('/restaurant/')
@app.route('/restaurant')
def exercise4():
    args = request.args
    location = args.get('location')
    search_term = args.get('term')
    if not (location and search_term):
        return '"location" and "term" are required query parameters'


    url = 'https://www.apitutor.org/yelp/simple/v3/businesses/search?location={0}&term={1}'.format(location, search_term)
    response = requests.get(url)
    restaurants = response.json()
    pprint(restaurants[0]) # for debugging
    return render_template(
        'restaurant.html',
        user="helllo",
        search_term=search_term,
        location=location,
        restaurant=restaurants[0]
    )

if __name__ == '__main__':
    app.run()