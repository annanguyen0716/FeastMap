document.querySelector("#drop-down").onchange = async function (e) {
    dish_name = this.value;
    var response = await fetch("/" + dish_name);
    var restaurant = await response.json();
    //console.log(restaurant.restaurant);
    //document.querySelector('#best_restaurant').innerHTML = `<div><b>${restaurant.restaurant}</b></div>` ;
    document.querySelector('#best_restaurant').innerHTML = `<h5 class="text-success"><a href="/restaurants/${restaurant.restaurant_id}">${restaurant.restaurant}</a></h5>`;
};

