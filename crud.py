"""CRUD operations."""

from model import db, User, Restaurant, Vote, RestaurantItem, MenuItem, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user


def get_users():
    """Return all users."""

    return User.query.all()


def get_user_by_id(user_id):
    """Return a user by primary key."""

    return User.query.get(user_id)


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_restaurant(name,zipcode,menu):
    """Create and return a new movie."""

    restaurant = Restaurant(
        name=name,
        zipcode=zipcode,

    )

    return restaurant

def create_restaurant_item(restaurant,item):

    restaurant_item = RestaurantItem(restaurant_id=restaurant, item=item)

    return restaurant_item

def create_menu_item(item):

    menu_item = MenuItem(item=item)

    return menu_item


def get_restaurants():
    """Return all movies."""

    return Restaurant.query.all()


def get_restaurant_by_id(restaurant_id):
    """Return a restaurant by restaurant id"""

    return Restaurant.query.get(restaurant_id)


def create_vote(user, restaurantitem):
    """Create and return a new rating."""

    vote = Vote(user_id=user, restaurant_item_id=restaurantitem)

    return vote


#def update_rating(rating_id, new_score):
#    """ Update a rating given rating_id and the updated score. """
#    rating = Rating.query.get(rating_id)
#    rating.score = new_score

if __name__ == "__main__":
    from server import app

    connect_to_db(app)
