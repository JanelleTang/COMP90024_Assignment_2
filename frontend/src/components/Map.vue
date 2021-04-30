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
      center: [144.9631,-37.8136], // St. Paul
      //center: [-70.00014, 46.69317],
      zoom: 9,
      melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json'
    };
  },
  mounted() {
    // create the map after the component is mounted
    this.createMap();

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
      this.map.on('load', () => {
            this.map.addSource('maine', {
                type: 'geojson',
                data: this.melb_geo,
                });
            // Add a new layer to visualize the polygon.
            this.map.addLayer({
            'id': 'maine',
            'type': 'fill',
            'source': 'maine', // reference the data source
            'layout': {},
            'paint': {
            'fill-color': '#0080ff', // blue color fill
            'fill-opacity': 0.5
            }
            });
            // Add a black outline around the polygon.
            this.map.addLayer({
            'id': 'outline',
            'type': 'line',
            'source': 'maine',
            'layout': {},
            'paint': {
            'line-color': '#000',
            'line-width': 3
            }
});
      });
    },

    // ================= ADD GeoJSON POLYGON LAYER ================= //

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