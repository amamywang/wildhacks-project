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
