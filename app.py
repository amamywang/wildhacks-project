from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import backend.apiscraper as api

# initializes flask app:
app = Flask(__name__)

# Fetch initializing data
data = api.fetchAPI()

for period in data["periods"]:
    if period["name"] == "Breakfast":
        pass
    else:
        api.periods[period["name"]] = period["id"]

menu = api.populate_meal_period(data, "Breakfast")

##############
# Exercise 1 #
##############
@app.route('/')
@app.route('/home.html')
def main_page():
    return render_template("home.html")

@app.route('/breakfast.html', methods = ['GET', 'POST'])
def breakfast():
    is_leftover = []
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                pass
                # update_mongo(food)

    ### REPLACE ###
    foods = menu["Breakfast"]
    ### REPLACE ###

    return render_template("breakfast.html",
                           foods=foods)

@app.route('/lunch.html', methods = ['GET', 'POST'])
def lunch():
    is_leftover = []
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                pass
                # update_mongo(food)

    ### REPLACE ###
    menu = api.populate_meal_period(data, "Lunch")
    foods = menu["Lunch"][0]
    ### REPLACE ###

    return render_template("lunch.html",
                           foods=foods)

@app.route('/dinner.html', methods = ['GET', 'POST'])
def dinner():
    is_leftover = []
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                pass
                # update_mongo(food)

    ### REPLACE ###
    menu = api.populate_meal_period(data, "Dinner")
    foods = menu["Dinner"][0]
    ### REPLACE ###

    return render_template("dinner.html",
                           foods=foods)

@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/finish.html')
def finish():
    return render_template("finish.html")

def update_mongo():
    # call to mongo
    pass


# ##############
# # Exercise 4 #
# ##############
# @app.route('/restaurant/')
# @app.route('/restaurant')
# def exercise4():
#     args = request.args
#     location = args.get('location')
#     search_term = args.get('term')
#     if not (location and search_term):
#         return '"location" and "term" are required query parameters'
#
#
#     url = 'https://www.apitutor.org/yelp/simple/v3/businesses/search?location={0}&term={1}'.format(location, search_term)
#     response = requests.get(url)
#     restaurants = response.json()
#     pprint(restaurants[0]) # for debugging
#     return render_template(
#         'restaurant.html',
#         user="helllo",
#         search_term=search_term,
#         location=location,
#         restaurant=restaurants[0]
#     )

if __name__ == '__main__':
    app.run()