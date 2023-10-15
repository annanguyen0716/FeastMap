let map;
async function initMap() {
    const { Map } = await google.maps.importLibrary("maps");
    const map = new Map(document.getElementById("map"), {
        zoom: 12,
        center: { lat: 37.3284494, lng: -121.8611376 },
    });
    const image = {
        url: "/static/img/food icon.png",
        scaledSize: new google.maps.Size(50, 50),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(0, 0)
    };
    const response = await fetch("/restaurant_positions");
    const positions = await response.json();
    positions.restaurants.forEach(restaurant => {
        const infowindow = new google.maps.InfoWindow({
            content: `<b> ${restaurant.name}<br> Address: ${restaurant.address}<br> Hours: ${restaurant.hours}</b>`,
        });
        const marker = new google.maps.Marker({
            position: restaurant.position,
            map,
            icon: image,
        });
        marker.addListener("click", () => {
            infowindow.open({
                anchor: marker,
                map,
            });
        });
    });
}
initMap();
