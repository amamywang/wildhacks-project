from flask import Flask
from flask import render_template
from flask import request
from flask import url_for
import apiscraper as api
import mongodb as mdb

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

### CHANGE
dining_hall = "Allison"

# returns a cursor object that must be iterated to obtain a dict
foods_all_meals = mdb.collection.find({'$and': [{'dining_hall': dining_hall}, {'date': mdb.date}]})

for food_items in foods_all_meals:
    foods_dict = food_items


def get_leftover(foods_at_meal):
    '''
    Function to obtain the names of foods where 
    dining_hall[meal_period][category_index][category_name][food_index]["leftover"]
    is "yes"

    foods_at_meals is the dict foods_dict[meal_period]
    '''
    leftover_foods = []

    # iterate through each category and the food items in each category
    for category in foods_at_meal:
        for food_dict in list(category.values())[0]:
            if food_dict["leftover"] == "yes":
                leftover_foods.append(food_dict["name"])

    return leftover_foods

dining_hall = ""

##############
# Exercise 1 #
##############
@app.route('/', methods=['GET', 'POST'])
@app.route('/home.html', methods=['GET', 'POST'])
def main_page():
    global dining_hall
    if request.method == 'POST':
        dining_hall = request.form.get('dining')
        time = request.form.get('meal')
        print(dining_hall, time)
        return render_template(time)

    return render_template("home.html")


@app.route('/breakfast.html', methods=['GET', 'POST'])
def breakfast():
    foods = foods_dict["Breakfast"]
    is_leftover = get_leftover(foods)
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                yes_to_no.append(food)
            else:
                no_to_yes.append(food)
            update_mongo(dining_hall, yes_to_no, no_to_yes)
        return render_template("finish.html")

    length = len(foods)
    firstfoods = foods[:round(length / 3)]
    secondfoods = foods[round(length / 3):round(2 * length / 3)]
    thirdfoods = foods[round(2 * length / 3):round(length / 3)]

    return render_template("breakfast.html",
                           firstfoods=firstfoods,
                           secondfoods=secondfoods,
                           thirdfoods=thirdfoods)


@app.route('/lunch.html', methods=['GET', 'POST'])
def lunch():
    foods = foods_dict["Lunch"]
    is_leftover = get_leftover(foods)
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                yes_to_no.append(food)
            else:
                no_to_yes.append(food)
            update_mongo(dining_hall, yes_to_no, no_to_yes)
        return render_template("finish.html")

    ### REPLACE ###
    # menu = api.populate_meal_period(data, "Lunch")
    # foods = menu["Lunch"][0]
    ### REPLACE ###
    length = len(foods)
    firstfoods = foods[:round(length / 3)]
    secondfoods = foods[round(length / 3):round(2 * length / 3)]
    thirdfoods = foods[round(2 * length / 3):round(length / 3)]

    return render_template("lunch.html",
                           firstfoods=firstfoods,
                           secondfoods=secondfoods,
                           thirdfoods=thirdfoods)


@app.route('/dinner.html', methods=['GET', 'POST'])
def dinner():
    foods = foods_dict["Dinner"]
    is_leftover = get_leftover(foods)
    if request.method == 'POST':
        yes_to_no = []
        no_to_yes = []
        for food in request.form.getlist('food'):
            if food in is_leftover:
                yes_to_no.append(food)
            else:
                no_to_yes.append(food)
            update_mongo(dining_hall, yes_to_no, no_to_yes)
        return render_template("finish.html")

    ### REPLACE ###
    # menu = api.populate_meal_period(data, "Dinner")
    # foods = menu["Dinner"][0]

    ### REPLACE ###

    length = len(foods)
    firstfoods = foods[:round(length / 3)]
    secondfoods = foods[round(length / 3):round(2 * length / 3)]
    thirdfoods = foods[round(2 * length / 3):round(length / 3)]

    return render_template("dinner.html",
                           firstfoods=firstfoods,
                           secondfoods=secondfoods,
                           thirdfoods=thirdfoods)


@app.route('/index.html')
def index():
    return render_template("index.html")


@app.route('/finish.html')
def finish():
    return render_template("finish.html")


@app.route('/s_breakfast.html')
def s_breakfast():
    return render_template("s_breakfast.html")


@app.route('/s_dinner.html')
def s_dinner():
    return render_template("s_dinner.html")


@app.route('/s_home.html')
def s_home():
    return render_template("s_home.html")


@app.route('/s_lunch.html')
def s_lunch():
    return render_template("s_lunch.html")

def update_mongo(dining_hall, yes_to_no, no_to_yes):

    # changing the entries for no_to_yes
    addresses_to_yes = find_addresses(no_to_yes)

    for address in addresses_to_yes:
        mdb.collection.update_one(
            { "dining_hall": dining_hall,"date": mdb.date}, # filter
            {"$set": { address[0]: "yes"}})
        
        print(address[0] + " updated to yes (" + address[1] + ")")
    
    # changing the entries for yes_to_no
    addresses_to_no = find_addresses(yes_to_no)

    for address in addresses_to_no:
        mdb.collection.update_one(
            { "dining_hall": dining_hall,"date": mdb.date}, # filter
            {"$set": { address[0]: "no"}})
        
        print(address[0] + " updated to no (" + address[1] + ")")

def find_addresses(food_item_list):
    category_index = 0
    food_index = 0
    food_meal = ""
    category_name = ""
    addresses = []
    item_addresses = []
    
    print(food_item_list)
    for changed_food in food_item_list:
        item_addresses = []
        for meal in ["Breakfast", "Lunch", "Dinner"]:
            category_index = 0
            print(meal + " menu")
            print(foods_dict[meal])
            print("\n")
            for category in foods_dict[meal]: # iterate through Comfort, Rooted, etc
                food_index = 0
                category_name = list(category.keys())[0]

                for food_item_dict in (list(category.values()))[0]:
                    if food_item_dict["name"] == changed_food:
                        
                        food_meal = meal
                        address = food_meal + "." + str(category_index) + "." + category_name + "." + str(food_index) + "." + "leftover"
                        item_addresses.append(address)
                    food_index += 1
                category_index += 1

        for address in item_addresses:
            addresses.append([address, changed_food])

    return addresses


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
    app.run(threaded=True)