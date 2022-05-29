import urllib.request
import json 
import ssl

#todo: make directory load with $HOME

locations = {
    "Allison": "5b33ae291178e909d807593d",
    "Sargent": "5b33ae291178e909d807593e"
}

# times = {} # Breakfast, Lunch, Dinner
#categories = {} # Rooted, Comfort, etc

# items["Breakfast"]: {category: items}

# items = {
#     "Breakfast": [], # contains a list of dictionaries {category_name: [items]}
#     "Lunch": [],
#     "Dinner": []
# }

### starting menu loads all the possible food items
### starting_menu: { meal_period: [{category_1: foods}, {category_2: foods}]
#                       }
starting_menu = {}


ssl._create_default_https_context = ssl._create_unverified_context
with urllib.request.urlopen(f"https://api.dineoncampus.com/v1/location/{locations['Allison']}/periods?platform=0&date=2022-5-28") as url:
    # data contains the information for one meal period
    data = json.loads(url.read().decode()) #dictionary 

## POPULATING STARTING MENU
### starting_menu: { meal_period: [{category_1: foods}, {category_2: foods}]
#                       }

## add the meal period to starting_menu
# mydict["newkey"] = "newValue"
meal_period = data["menu"]["periods"]["name"]
starting_menu[meal_period] = []

# obtain the categories for each meal period (ex: Comfort 1, Comfort 2, ...)
categories = []
for category_info in data["menu"]["periods"]["categories"]:
    categories.append(category_info["name"])

# add the food items for each category
food_items = []

# append the list of {category: foods} to meal_period in starting_menu



# data["menu"] keys: dict_keys(['id', 'date', 'name', 'from_date', 'to_date', 'periods'])
# data["menu"]["periods"] keys: dict_keys(['id', 'name', 'sort_order', 'categories'])
    # periods 
# data["menu"]["periods"]["categories"] is a list of dictionaries, representing the diff categories during one period (Comfort I, Comfort 2)
    # each dictionary has the keys: dict_keys(['id', 'name', 'sort_order', 'items'])
        # ["items"] contains is a list of dictionaries
            # each dictionary has the keys: dict_keys(['id', 'name', 'mrn', 'rev', 'mrn_full', 'desc', 'webtrition_id', 'sort_order', 'portion', 'qty', 'ingredients', 'nutrients', 'filters', 'custom_allergens', 'calories'])
                # name = food name!!


#print(data["menu"]["periods"].keys())
# print(data["menu"]["periods"]["categories"][0])
print(data["menu"]["periods"]["categories"][0].keys())
# print(data["menu"]["periods"]["name"])
#print(data["menu"]["periods"]["categories"][0]["items"][0]["name"])
#print(type(data["menu"]["periods"]["categories"][0]["items"][0]["name"]))
#print(type(data["menu"]["periods"]))


# # All periods are listed under the menu
# for period in data["periods"]:
#     times[period["name"]] = period["id"]

# for category in data["menu"]["periods"]["categories"]:
#     # Each period is either Breakast/Lunch/Dinner
#     timePeriod = data["menu"]["periods"]["name"]

#     # Get each category name (Rooted, Comfort, etc.)
#     categories[category["name"]] = category["id"]

#     # Get all items and put them in the item dictionary
#     for item in category["items"]:
#         items[timePeriod] = item["name"]




