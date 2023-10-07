"""Models for movie ratings app."""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    #zipcode = db.Column(db.Integer)

    votes = db.relationship("Vote", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.id} email={self.email}>"

class Restaurant(db.Model):
    """A restaurant"""

    __tablename__ = "restaurants"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String)
    zipcode = db.Column(db.Integer)
    city = db.Column(db.String)

    #restaurants = db.relationship("Zipcode", back_populates="restaurants")
    restaurantitems = db.relationship("RestaurantItem", back_populates="restaurant")

    def __repr__(self):
        return f"<Restaurant restaurant_id={self.id} restaurant_name={self.name}>"

class Vote(db.Model):
    """A vote for a restaurant"""

    __tablename__ = "votes"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_item_id = db.Column(db.Integer, db.ForeignKey("restaurantitems.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    restaurant_item = db.relationship("RestaurantItem", back_populates="votes")
    user = db.relationship("User", back_populates="votes")

    def __repr__(self):
        return f"<Vote vote_id={self.id} restaurant_item_id={self.restaurant_item_id}>"

class RestaurantItem(db.Model):
    """A vote for a restaurant"""

    __tablename__ = "restaurantitems"

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))
    item = db.Column(db.String, db.ForeignKey("dishes.dish_name"))

    votes = db.relationship("Vote", back_populates="restaurant_item")
    restaurant = db.relationship("Restaurant", back_populates="restaurantitems")
    dish = db.relationship("Dish", back_populates="restaurantitems")

    def __repr__(self):
        return f"{self.id} - {self.item.capitalize()}"

class Dish(db.Model):
    
    __tablename__ = "dishes"

    #id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    dish_name = db.Column(db.String, primary_key=True)
    #cuisine - nice to have but not added for now

    restaurantitems = db.relationship("RestaurantItem", back_populates="dish")


#class Zipcode(db.Model):
#    __tablename__ = "zipcodes"
#    zipcode = db.Column(db.Integer, primary_key=True)
#    city = db.Column(db.String)
#    county = db.Column(db.String)


def connect_to_db(flask_app, db_uri="postgresql:///ratings", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
