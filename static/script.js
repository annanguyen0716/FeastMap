document.querySelector("#drop-down").onchange = async function (e) {
    dish_name = this.value;
    var response = await fetch("/" + dish_name);
    var restaurant = await response.json();
    console.log(restaurant.restaurant);
    document.querySelector('#best_restaurant').innerHTML = `<div><b>${restaurant.restaurant}</b></div>` ;
};