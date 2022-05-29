import pymongo, certifi
import apiscraper
import datetime

# create client object
client = pymongo.MongoClient("mongodb+srv://awang:wildhacks@cluster00.rtsknmc.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())

db = client["munchies"] # database
collection = db["food-items"] # collection name

# all the documents in the ["munchies""food-items"] db
all_dh_data = collection.find({})

date = datetime.datetime.now().strftime("%Y-%m-%d")

# extracting the dining hall and date combinations already stored in mongodb
id_count = 0
populated_dh_data = []
for dh in all_dh_data:
    populated_dh_data.append([dh['dining_hall'], date])
    id_count += 1

# initially putting starting_menus for all dining halls into MongoDB
dining_halls = apiscraper.locations

for dh in dining_halls.keys():
    if [dh, date] not in populated_dh_data:
        starting_menu = apiscraper.generate_starting_menu(dh)
        starting_menu["_id"] = id_count+1
        id_count += 1
        collection.insert_one(starting_menu)
        print(dh + " data were uploaded to MDB")
    else:
        print(dh + " data were already uploaded to MDB" )

dining_hall = "Allison"
foods_all_meals = collection.find({'$and':[{'dining_hall': dining_hall}, {'date': date}]})

for food_items in foods_all_meals:
    foods = food_items

#print(foods["Breakfast"])

# breakfast foods
leftover_foods = []
breakfast = foods["Breakfast"]
for category in breakfast:
    for food_dict in list(category.values())[0]:
            if food_dict["leftover"] == "yes":
                leftover_foods.append(food_dict["name"])

print(leftover_foods)
'''
allison = collection.find_one({})
category_index = 0
food_index = 0
food_item = 'Scrambled Eggs'
found = False
category_name = ""

for meal in ["Breakfast", "Lunch", "Dinner"]:
    category_index = 0
    for category in allison[meal]: # iterate through Comfort, Rooted, etc
        category_name = list(category.keys())[0]
        food_index = 0
        for food_dict in list(category.values())[0]:
            if food_dict["name"] == food_item:
                print(food_item + " found!")
                print("food_index is " + str(food_index))    
                print("category_index is " + str(category_index))
                found = True
            if not found:
                food_index += 1
                print("food" + str(food_index))
        if found:
            break
        category_index += 1
        print("cat" + str(category_index))

# print(allison["Breakfast"][category_index][category_name][food_index]["name"])

print("Breakfast." + str(category_index) + "." + category_name + "." + str(food_index) + "." + "name")
address = "Breakfast." + str(category_index) + "." + category_name + "." + str(food_index) + "." + "leftover"

collection.update_one(
    { "dining_hall": "Allison","date":date}, # filter
    {"$set": { address: "yes"}
}
)
print(address + " updated")

'''
