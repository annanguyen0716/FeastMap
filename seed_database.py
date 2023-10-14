"""Script to seed database."""

import os
import json
from random import sample, randint, choice
from datetime import datetime

import crud
import model
import server

os.system("dropdb ratings")
os.system("createdb ratings")

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open("data/restaurants.json") as f:
    restaurant_data = json.loads(f.read())

# Create movies, store them in list so we can use them
# to create fake ratings
restaurants_in_db = []
restaurantitems_in_db = []
dishes_in_db_check = set()
dishes_in_db = []


for restaurant in restaurant_data:
    name, zipcode, city = (
        restaurant["name"],
        restaurant["zipcode"],
        restaurant["city"],
    )

    db_restaurant = crud.create_restaurant(name, zipcode)
    model.db.session.add(db_restaurant)
    model.db.session.commit()

    menu_list = restaurant["menu"].split(", ")

    for item in menu_list:
        if item not in dishes_in_db_check:
            dishes_in_db_check.add(item)
            dish = crud.create_menu_item(item)
            dishes_in_db.append(dish)
        restaurant_item = crud.create_restaurant_item(db_restaurant.id, item)
        restaurantitems_in_db.append(restaurant_item)
    



model.db.session.add_all(dishes_in_db)
model.db.session.add_all(restaurantitems_in_db)
model.db.session.commit()

#model.db.session.add_all(menuitems_in_db)
#model.db.session.commit()
# 
# Create 50 users; each user will make 10 ratings
for n in range(50):
    email = f"user{n+1}@test.com"  # Voila! A unique email!
    password = "test"
    adjective = choice(["Hangry","Happy"])
    username = f"{adjective}Eater{n+1}"

    user = crud.create_user(email, password, username)
    model.db.session.add(user)

    model.db.session.commit()


    random_restaurant_item = sample(restaurantitems_in_db, 15)

    for item in random_restaurant_item:
        vote = crud.create_vote(user.id, item.id)
        model.db.session.add(vote)
        model.db.session.commit()


model.db.session.commit()