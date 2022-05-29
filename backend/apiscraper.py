import urllib.request
import json 
import ssl
import re
from datetime import datetime


#todo: make directory load with $HOME

locations = {
    "Allison": "5b33ae291178e909d807593d",
    "Sargent": "5b33ae291178e909d807593e"
}

periods = {
    "Breakfast": ""
}

def fetchAPI(dining_hall: str="Allison", period: str="Breakfast", date=datetime.now().strftime("%Y-%m-%d")) -> dict:
    """
    Fetches data from dineoncampus API given a dining hall and a period (Breakfast, Lunch, Dinner)
    and returns a dictionary of the data.
    """
    
    if period == "Breakfast":
        url_period = periods["Breakfast"]
    elif period == "Lunch":
        url_period = periods["Lunch"]
    elif period == "Dinner":
        url_period = periods["Dinner"]
    else:
        raise ValueError("Incorrect Period Given")
    
    # Prevents Certificate Errors
    ssl._create_default_https_context = ssl._create_unverified_context
    with urllib.request.urlopen(f"https://api.dineoncampus.com/v1/location/{locations[dining_hall]}/periods{url_period}?platform=0&date={date}") as url:
        # data contains the information for one meal period
        data = json.loads(url.read().decode())

    return data

## POPULATING STARTING MENU

starting_menu = {}

def populate_meal_period(data: dict, meal_period: str):
    """
    Populates starting_menu in the format of:
    
    starting_menu: { 
        meal_period: [
            {category_1: foods},
            {category_2: foods}, ...
        ] 
    }
    
    for the meal_period parameter.
    
    Appends the {meal_period: [
                    {category_1: food_1, ...}
                    {category_2: food_2, ...}
                    ]
                }

    ]}
    ### extracts the {category: food_items} for each category of the meal_period
    ### appends dictionaries to starting_menu 
    """
        
    starting_menu[meal_period] = []

    # extract the {category_name: [food1, food2, ...]} for each meal period (ex: Comfort 1, Comfort 2, ...), 
    # append to starting_menu
    food_items = []
    seen_categories = []

    for category_info in data["menu"]["periods"]["categories"]:
        category = category_info["name"]
        food_items = []
        for food in category_info["items"]:
            food_items.append(food["name"])

        # Combine similar categories (ex: Comfort 1 and Comfort 2) together
        if re.search(r' \d$', category):
            category = category[:-2]
        
        # Add category if not in menu, otherwise combine them.
        if category not in seen_categories:
            starting_menu[meal_period].append({category: food_items})
            seen_categories.append(category)
        else:
            starting_menu[meal_period][seen_categories.index(category)][category] += food_items

    return starting_menu

### starting menu loads all the possible food items
### starting_menu: { meal_period: [{category_1: foods}, {category_2: foods}] }

if __name__ == '__main__':
    data = fetchAPI("Allison", "Breakfast")

    for period in data["periods"]:
        if period["name"] == "Breakfast":
            pass
        else:
            periods[period["name"]] = period["id"]

    starting_menu = populate_meal_period(data, "Breakfast")
    
    print("Breakfast: ", starting_menu["Breakfast"], "\n")

    data = fetchAPI("Allison", "Lunch")
    starting_menu = populate_meal_period(data, "Lunch")
    print("Lunch: ", starting_menu["Lunch"], "\n")

    data = fetchAPI("Allison", "Dinner")
    starting_menu = populate_meal_period(data, "Dinner")
    print("Dinner: ", starting_menu["Dinner"])

#with urllib.request.urlopen(f"https://api.dineoncampus.com/v1/location/{locations['Allison']}/periods{periods['Breakfast']}platform=0&date=2022-5-28") as url:


# print(second)


# append the list of {category: foods} to meal_period in starting_menu



# data["menu"] keys: dict_keys(['id', 'date', 'name', 'from_date', 'to_date', 'periods'])
# data["menu"]["periods"] keys: dict_keys(['id', 'name', 'sort_order', 'categories'])
    # periods 
# data["menu"]["periods"]["categories"] is a list of dictionaries, representing the diff categories during one period (Comfort I, Comfort 2)
    # each dictionary has the keys: dict_keys(['id', 'name', 'sort_order', 'items'])
        # ["items"] contains is a list of dictionaries
            # each dictionary has the keys: dict_keys(['id', 'name', 'mrn', 'rev', 'mrn_full', 'desc', 'webtrition_id', 'sort_order', 'portion', 'qty', 'ingredients', 'nutrients', 'filters', 'custom_allergens', 'calories'])
                # name = food name!!






