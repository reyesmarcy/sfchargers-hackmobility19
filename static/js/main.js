


class HereMap {

    constructor(appId, appCode, mapElement) {
        this.platform = new H.service.Platform({
            "app_id": appId,
            "app_code": appCode
        });
        let defaultLayers = this.platform.createDefaultLayers();
        this.map = new H.Map(
            mapElement,
            defaultLayers.normal.map,
            {
                zoom: 10,
                center: { lat: 37.7397, lng: -121.4252 }
            }
        );
        let behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(this.map));
        this.geocoder = this.platform.getGeocodingService();
        this.router = this.platform.getRoutingService();
    }
    dropMarker(latitude, longitude) {
        var marker = new H.map.Marker({ lat: latitude, lng: longitude });
        this.map.addObject(marker);
    }
    drawLinesBetweenMarkers(start, finish) {
        let lineString = new H.geo.LineString();
        lineString.pushPoint(start);
        lineString.pushPoint(finish);
        this.map.addObject(new H.map.Polyline(
            lineString, { style: { strokeColor: "green", lineWidth: 5 }}
        ));
        // this.map.setViewBounds()
    }
    geocode(query) {
        return new Promise((resolve, reject) => {
            this.geocoder.geocode({ searchText: query }, result => {
                if(result.Response.View.length > 0) {
                    if(result.Response.View[0].Result.length > 0) {
                        resolve(result.Response.View[0].Result[0].Location.DisplayPosition);
                    } else {
                        reject({ message: "no results found" });
                    }
                } else {
                    reject({ message: "no results found" });
                }
            }, error => {
                reject(error);
            });
        });
    }
    drawRoute(start, finish) {
        let params = {
            "mode": "fastest;car",
            "waypoint0": "geo!" + start.Latitude + "," + start.Longitude,
            "waypoint1": "geo!" + finish.Latitude + "," + finish.Longitude,
            "representation": "display"
        }
        this.router.calculateRoute(params, data => {
            if(data.response) {
                data = data.response.route[0];
                let lineString = new H.geo.LineString();
                data.shape.forEach(point => {
                    let parts = point.split(",");
                    lineString.pushLatLngAlt(parts[0], parts[1]);
                });
                let routeLine = new H.map.Polyline(lineString, {
                    style: { strokeColor: "blue", lineWidth: 5 }
                });
                this.map.addObjects([routeLine]);
            }
        }, error => {
            console.error(error);
        });
    }

}

function getUserAddress(evt){
    // evt.preventDefault()
    const start = document.getElementById("start").value;
    const end = document.getElementById("end").value;
    // console.log(address)
    return [start,end]
 };