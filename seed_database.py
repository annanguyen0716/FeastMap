"""Script to seed database."""

import os
import json
from random import choice, randint
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
restaurantitems_in_db = set()
menuitems_in_db = set()

for restaurant in restaurant_data:
    name, zipcode, city = (
        restaurant["name"],
        restaurant["zipcode"],
        restaurant["city"],
    )

    db_restaurant = crud.create_restaurant(name, zipcode, city)
    restaurants_in_db.append(db_restaurant)

    menu_list = restaurant["menu"].split(", ")

    for item in menu_list:
        menu_item = crud.create_menu_item(item)
        menuitems_in_db.add(menu_item)
        restaurant_item = crud.create_restaurant_item(db_restaurant.id, item)
        restaurantitems_in_db.add(restaurant_item)


model.db.session.add_all(restaurants_in_db)
model.db.session.commit()

model.db.session.add_all(restaurantitems_in_db)
model.db.session.commit()

model.db.session.add_all(menuitems_in_db)
model.db.session.commit()
# 
# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"  # Voila! A unique email!
    password = "test"

    user = crud.create_user(email, password)
    model.db.session.add(user)

    for _ in range(30):
        random_restaurant_item = choice(restaurantitems_in_db)
        vote = crud.create_vote(user.id,random_restaurant_item.id)
        model.db.session.add(vote)

model.db.session.commit()