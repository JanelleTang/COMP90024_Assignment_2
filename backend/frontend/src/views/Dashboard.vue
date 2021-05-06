<template>
  <div class="dashboard">
    <v-container>
      <h1>Climate Change Sentiment in Australian Cities</h1>
    </v-container>
    <v-row class="ml-14 mr-8">
      <v-col
        cols="12"
        sm="6"
        md="10"
      >
          <div id="map-container"></div>
      </v-col>
      <v-col
        cols="6"
        sm="6"
        md="2"
      >
      <v-card>
        <button id="fit">Australia</button>
      </v-card>
          
      </v-col>
    </v-row>
  </div>
</template>
<script>
import axios from "axios"
// import { getAPI } from "../axios";
import Mapbox from "mapbox-gl";
//import d3 from "d3";



  export default {
      name:'gmap',
      data () {
          return {
              center: [144.9631, -37.8136],
              zoom: 9,
              melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json',
              django_geo: "http://127.0.0.1:8000/api/data.geojson",
              locations: [["Melbourne", 144.9631,-37.8136],
              ["Sydney",151.2093,-33.8688],
              ["Adelaide",138.6007,-34.9285],
              ["Brisbane",153.0260,-27.4705]],
              url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              bounds: null,
              }
      },
      created() {
          axios.get(this.django_geo).then(response => {
            this.APIdata = JSON.stringify(response.data)
          });

      },
      mounted() {
          this.getGeoJSON()
          this.createMap();
          this.load_json();
          this.boundingBox();

      },

      methods: {
          getGeoJSON(){
            axios.get(this.django_geo).then(response =>{
              let geo_data = response.data.features;
              this.geoConf = {
                "type":"FeatureCollection",
                "features": geo_data
              }

            })
          },
          // ================= CREATE BASE MAP ================= //
          createMap() {
              this.map = new Mapbox.Map({
                  accessToken:"pk.eyJ1IjoiamFuZWxsZXQxIiwiYSI6ImNrZXYwd3VraDIyMm4ycXF2em9yanMzOHYifQ.gBExgtEISuunP4aq3jU77g",
                  container: "map-container",
                  style: 'mapbox://styles/janellet1/ckeziaeb03o3219s3eapgb30p',
                  minzoom: 5,
                  center: this.center, 
                  zoom: this.zoom,
                  doubleClickZoom: false,
                  pitchWithRotate: false,	
                  hash: true // sets url's hash to #zoom/lat/lng
              });
            },
          load_json() {
              this.map.on('load', () => {
                  this.map.addSource('melb_lga', {
                      type: 'geojson',
                      data: this.django_geo,
                      });
                  // Add a new layer to visualize the polygon.
                  this.map.addLayer({
                  'id': 'melb_lga_fill',
                  'type': 'fill',
                  'source': 'melb_lga', 
                  'paint': {
                    'fill-color': [
                        'match',
                        ['get','sentiment_rank'],
                        1,
                        '#d73027',
                        2,
                        '#f46d43',
                        3,
                        '#fee08b',
                        4,
                        '#a6d96a',
                        5,
                        '#1a9850',
                        /* other */ '#ccc'
                    ],
                    'fill-opacity': 0.7//parseFloat(['get', "sentiment_value"])
                  }
                  });
                  /* ------- Add a black outline around the polygon. ------- */
                  this.map.addLayer({
                    'id': 'melb_lga_line',
                    'type': 'line',
                    'source': 'melb_lga',
                    'paint': {
                      'line-color': 'rgba(60,60,255,0.5)',
                      'line-width': 2
                    }
                  });
                  /* ------- Add a popup tooltip on Click ------- */
                  this.map.on('click', 'melb_lga_fill', (e) => {
                    new Mapbox.Popup({closeOnClick: true,offset: 5})
                    .setLngLat(e.lngLat)
                    .setHTML(e.features[0].properties.name)

                    .addTo(this.map);
                    });
                    
                    // Change the cursor to a pointer when the mouse is over the states layer.
                    this.map.on('mouseenter', 'melb_lga_fill', () => {
                    this.map.getCanvas().style.cursor = 'pointer';
                    });
                    
                    // Change it back to a pointer when it leaves.
                    this.map.on('mouseleave', 'melb_lga_fill', () => {
                    this.map.getCanvas().style.cursor = '';
                    });
            });
          },
          boundingBox(){
            document.getElementById('fit').addEventListener('click', () => {
              this.map.fitBounds([
              [113.338953078, -43.6345972634],
              [153.569469029, -10.6681857235]
            ]);
});
          },
      },

  }
</script>
<style>
#map-container{
      height: 600px;
      width: 100%;
      max-width: 1100px;
      margin: 0 auto;
      border: 1px solid darkgrey;

}

#fit-au {
display: block;
position: relative;
margin: 0px auto;
width: 50%;
height: 40px;
padding: 10px;
border: none;
border-radius: 3px;
font-size: 12px;
text-align: center;
color: #fff;
background: #ee8a65;
position: absolute;
   top: 10px;
   left: 10px;
   z-index: 1;
   pointer-events: all;
}
</style>