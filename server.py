"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, db
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route("/")
def homepage():
    """View homepage."""
    dishes = crud.get_dishes()

    return render_template("homepage.html", dishes=dishes)

@app.route("/dishes")
def all_dishes():
    """View all restaurant"""

    dishes = crud.get_dishes()

    return render_template("all_dishes.html", dishes=dishes)

@app.route("/dishes/<dish_name>")
def show_restaurants(dish_name):
    """Show restaurants that serve a dish."""

    restaurantitems = crud.get_restaurantitems_by_item(dish_name)
    restaurants = []
    for restaurantitem in restaurantitems:
        number_of_votes = len(restaurantitem.votes)
        restaurant = crud.get_restaurant_by_id(restaurantitem.restaurant_id)
        restaurants.append((number_of_votes,restaurant))
    restaurants.sort(key=lambda a: a[0], reverse = True)
        #restaurants.append(crud.get_restaurant_by_id(restaurantitem.restaurant_id))
    return render_template("restaurants_that_serve_dish.html", restaurants=restaurants, dish_name=dish_name.capitalize())

@app.route("/restaurants")
def all_restaurants():
    """View all restaurant"""

    restaurants = crud.get_restaurants()

    return render_template("all_restaurants.html", restaurants=restaurants)


@app.route("/restaurants/<restaurant_id>")
def show_restaurant(restaurant_id):
    """Show details on a particular restaurant"""

    restaurant = crud.get_restaurant_by_id(restaurant_id)
    items_to_vote = crud.get_items_by_restaurant(restaurant_id)
    logged_in_email = session.get("user_email")

    if logged_in_email is None:
        flash("You must log in to vote for a restaurant.")
        
    return render_template("restaurant_details.html", restaurant=restaurant, items_to_vote=items_to_vote)


@app.route("/users")
def all_users():
    """View all users."""

    users = crud.get_users()

    return render_template("all_users.html", users=users)


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    email = request.form.get("email")
    password = request.form.get("password")
    username = request.form.get("username")

    user = crud.get_user_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")

    else:
        user = crud.create_user(email, password, username)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = crud.get_user_by_id(user_id)
    votes_details = []
    for vote in user.votes:
        restaurant_item = crud.get_item_by_id(vote.restaurant_item_id)
        votes_details.append((crud.get_restaurant_name_by_id(restaurant_item.restaurant_id),restaurant_item.item))
    
    votes_details.sort(key=lambda a: a[0])

    return render_template("user_details.html", user=user, votes_details=votes_details)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")

#@app.route("/update_rating", methods=["POST"])
#def update_rating():
#    rating_id = request.json["rating_id"]
#    updated_score = request.json["updated_score"]
#    crud.update_rating(rating_id, updated_score)
#    db.session.commit()

#    return "Success"


@app.route("/restaurants/<restaurant_id>/votes", methods=["POST"])
def create_vote(restaurant_id):
    """Create a new vote for the restaurant"""

    logged_in_email = session.get("user_email")
    items_to_vote = crud.get_items_by_restaurant(restaurant_id)
    voted_item = request.form.get("vote")

    if logged_in_email is None:
        flash("You must log in to vote for a restaurant.")
    elif not voted_item:
        flash("Error: you didn't select a menu item for your vote")
    else:
        user = crud.get_user_by_email(logged_in_email)
 
        #restaurantitem = crud.get_restaurant_by_id(restaurant_id)


        vote = crud.create_vote(user.id, int(voted_item.split(" - ")[0]))
   
  
        db.session.add(vote)
        db.session.commit()

        flash(f"You voted for {voted_item} at {crud.get_restaurant_by_id(restaurant_id).name}.")

    return redirect(f"/restaurants/{restaurant_id}")

@app.route("/<dish_name>")
def recommended_restaurant(dish_name):
    
    restaurantitems = crud.get_restaurantitems_by_item(dish_name)
    highest = 0
    best_restaurant = 0
    for restaurantitem in restaurantitems:
        number_of_votes = len(restaurantitem.votes)
        if number_of_votes > highest:
            highest = number_of_votes
            best_restaurant = restaurantitem.restaurant_id
    
    res = crud.get_restaurant_by_id(best_restaurant)

    if highest == 0:
        return jsonify({'restaurant': "Oops. No restaurant has been voted for this dish", 'restaurant_id': -1})

    
    return jsonify({'restaurant': res.name, 'restaurant_id': res.id})

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
