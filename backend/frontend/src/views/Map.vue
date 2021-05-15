/* eslint-disable */
<template>
  <div class="Map">
    <Sidebar></Sidebar>
      <v-app>
    <v-content>
        <v-row class="mx-4 mt-n3">
            <v-col
            cols="12"
            md="8"
            lg="10"

            >
                <div id="map-container"></div>   
            </v-col>
            <v-col
            cols="12"
            md="4"
            lg="2"
            >
                    <v-card class="">
            <v-card-title class="text-center">
                Climate Change Sentiment in Australian Cities
            </v-card-title>
            <v-card-text>
                Add some graphs here (change on click)
            </v-card-text>

      </v-card>
            </v-col>
        </v-row>


        <!-- <v-container fluid class="align-start px-10 d-flex flex-row">
            
        <v-row class="">
                <div id="map-container"></div>      
        </v-row>
        </v-container> -->
    </v-content>
    </v-app>
  </div>
</template>
<script>
import Mapbox from "mapbox-gl";
//import d3 from "d3";
import Sidebar from "@/components/Sidebar"


  export default {
      name:'Map',
      data () {
          return {
              center: [144.9631, -37.8136],
              zoom: 9,
              lga_geodata: "http://127.0.0.1:8000/api/lga_data.geojson",
              city_geodata: "http://127.0.0.1:8000/api/city_data.geojson",
              locations: [["Melbourne", 144.9631,-37.8136],
              ["Sydney",151.2093,-33.8688],
              ["Adelaide",138.6007,-34.9285],
              ["Brisbane",153.0260,-27.4705]],
              url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              bounds: null,

              }
      },
      components:{
        // Navbar,
        Sidebar,
      },

      mounted() {
          this.createMap();
          this.load_json();
          this.boundingBoxAU();
          this.boundingBoxVIC();
          this.boundingBoxNSW();

      },

      methods: {
          // ================= CREATE BASE MAP ================= //
          createMap() {
              this.map = new Mapbox.Map({
                  accessToken:"pk.eyJ1IjoiamFuZWxsZXQxIiwiYSI6ImNrZXYwd3VraDIyMm4ycXF2em9yanMzOHYifQ.gBExgtEISuunP4aq3jU77g",
                  container: "map-container",
                  style: 'mapbox://styles/janellet1/ckoe0bqgk1yyf18nz5tij50u6',
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
                  this.map.resize();
                  // ========== ADDING LGA LAYER ========== //
                  this.map.addSource('lga_layer', {
                      type: 'geojson',
                      data: this.lga_geodata,
                      // minzoom: 10,
                      // maxzoom: 18,
                      });
                  // Add a new layer to visualize the polygon.
                  this.map.addLayer({
                  'id': 'lga_fill',
                  'type': 'fill',
                  'source': 'lga_layer', 
                  'minzoom':5,
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
                    'id': 'lga_line',
                    'type': 'line',
                    'source': 'lga_layer',
                    'minzoom':5,
                    'paint': {
                      'line-color': 'rgba(60,60,255,0.5)',
                      'line-width': 2
                    }
                  });
                  /* ------- Add a popup tooltip on Click ------- */
                  this.map.on('click', 'lga_fill', (e) => {
                    new Mapbox.Popup({closeOnClick: true,offset: 5})
                    .setLngLat(e.lngLat)
                    .setHTML(e.features[0].properties.name)

                    .addTo(this.map);
                    });
                    
                    // Change the cursor to a pointer when the mouse is over the states layer.
                    this.map.on('mouseenter', 'lga_fill', () => {
                    this.map.getCanvas().style.cursor = 'pointer';
                    });
                    
                    // Change it back to a pointer when it leaves.
                    this.map.on('mouseleave', 'lga_fill', () => {
                    this.map.getCanvas().style.cursor = '';
                    });
                  
                  // ========== ADDING CITY LAYER ========== //
                  this.map.addSource('city_layer', {
                      type: 'geojson',
                      data: this.city_geodata,
                      // minzoom: 5,
                      // maxzoom: 10,
                      });
                  this.map.addLayer({
                    'id': 'city-circle',
                    'type': 'circle',
                    'source': 'city_layer',
                    'maxzoom':5,
                    'paint': {
                        'circle-radius': 30,
                        'circle-color': [
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
                        'circle-stroke-color': 'white',
                        'circle-stroke-width': 3,
                        'circle-opacity': 0.6,
                        },
                  });
            });
          },
          boundingBoxAU(){
            document.getElementById('fit-au').addEventListener('click', () => {
              this.map.fitBounds([
              [113.338953078, -43.6345972634],
              [153.569469029, -10.6681857235]
                ]);
            });
          },
          boundingBoxVIC(){
            document.getElementById('fit-vic').addEventListener('click', () => {
              this.map.fitBounds([
              [142.128154,-38.852748],
              [148.060771,-33.871461]
                ]);
            });
          },
          boundingBoxNSW(){
            document.getElementById('fit-nsw').addEventListener('click', () => {
              this.map.fitBounds([
              [146.03,-37.22],
              [154.14,-28.43]
                ]);
            });
          },
      },

  }
</script>
<style>
#map-container{
    padding: 0; 
    margin: 0; 
    display: flex;
    height:75vh;
    min-height:400px;
    position:relative;
    border: 1px solid darkgrey;
}

/* #fit-au {
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
} */



.mapboxgl-ctrl-attrib-inner{
    font-size:0em;

}

</style>