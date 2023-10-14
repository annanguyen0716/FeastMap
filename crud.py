"""CRUD operations."""

from model import db, User, Restaurant, Vote, RestaurantItem, Dish, connect_to_db


def create_user(email, password, username):
    """Create and return a new user."""

    user = User(email=email, password=password, username=username)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)

def get_item_by_id(item_id):
    """Return a user by primary key."""

    return RestaurantItem.query.get(item_id)

def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()

def get_user_by_username(username):
    """Return a user by email."""

    return User.query.filter(User.username == username).first()

def create_restaurant(name,zipcode,latitude,longtitude):
    """Create and return a new restaurant"""

    restaurant = Restaurant(
        name=name,
        zipcode=zipcode,
        latitude=latitude,
        longtitude=longtitude,
    )

    return restaurant

def create_restaurant_item(restaurant,item):

    restaurant_item = RestaurantItem(restaurant_id=restaurant, item=item)

    return restaurant_item

def create_menu_item(dish_name):

    menu_item = Dish(dish_name=dish_name)
    
    return menu_item

def get_items_by_restaurant(restaurant_id):
    """Return a list of items on the menu"""
    items = RestaurantItem.query.filter(RestaurantItem.restaurant_id == restaurant_id)

    return items

def get_restaurantitems_by_item(item):
    """Return a list of items on the menu"""
    restaurantitems = RestaurantItem.query.filter(RestaurantItem.item == item)

    return restaurantitems

def get_vote_by_id(vote_id):
    """Return a list of items on the menu"""
    vote = Vote.query.get(vote_id)

    return vote

def get_restaurants():
    """Return all movies."""

    return Restaurant.query.all()

def get_dishes():
    """Return all movies."""

    return Dish.query.order_by(Dish.dish_name)

def get_restaurant_name_by_id(restaurant_id):
    """Return a restaurant by restaurant id"""

    return Restaurant.query.get(restaurant_id).name

def get_restaurant_by_id(restaurant_id):
    """Return a restaurant by restaurant id"""

    return Restaurant.query.get(restaurant_id)


def create_vote(user_id, restaurantitem_id):
    """Create and return a new rating."""

    vote = Vote(user_id=user_id, restaurant_item_id=restaurantitem_id)

    return vote


#def update_rating(rating_id, new_score):
#    """ Update a rating given rating_id and the updated score. """
#    rating = Rating.query.get(rating_id)
#    rating.score = new_score

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
