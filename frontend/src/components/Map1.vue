<template>
  <main>
    <div class="text-container">
      <h4>Map</h4>
    </div>
        <div id="map" ref="map"></div>

  </main>
</template>

<script>
import Mapbox from "mapbox-gl";


export default {
  name: "MapboxMap",
  data() {
    // Set initial data, this.createMap() configures event listeners that update data based on user interaction
    return {
      //center: [144.9631,-37.8136], // St. Paul
      center: [-69.92355713,12.4375],
      zoom: 12,
      melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json'
    };
  },
  mounted() {
    // create the map after the component is mounted
    let map = this.createMap();
    this.createLayer(map)

  },
  
  methods: {
    // ================= CREATE BASE MAP ================= //
    createMap() {
      this.map = new Mapbox.Map({
          accessToken:"pk.eyJ1IjoiamFuZWxsZXQxIiwiYSI6ImNrZXYwd3VraDIyMm4ycXF2em9yanMzOHYifQ.gBExgtEISuunP4aq3jU77g",
          container: "map",
          style: 'mapbox://styles/janellet1/ckeziaeb03o3219s3eapgb30p',
          minzoom: 5,
          center: this.center, 
          zoom: this.zoom,
          hash: true // sets url's hash to #zoom/lat/lng
      });
    },

    // ================= ADD GeoJSON POLYGON LAYER ================= //
    createLayer(map) {
        map.addSource('some id', {
        type: 'geojson',
        data: 'https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_10m_ports.geojson'
        });
        map.addLayer({
            'id': 'outline',
            'type': 'line',
            'source': 'maine',
            'layout': {},
            'paint': {
            'line-color': '#000',
            'line-width': 3
            }
            });
    }
  }
  
};

</script>

<style scoped>
#map {
  height: 400px;
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  border: 1px solid darkgrey;
}
.text-container {
  max-width: 500px;
  display: flex;
  flex-direction: column;
  text-align: left;
  align-items: flex-start;
  margin: 0 auto; /* center text container */
}
</style>