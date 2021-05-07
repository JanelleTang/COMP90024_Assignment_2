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
import axios from "axios"
// import { getAPI } from "../axios";
import Mapbox from "mapbox-gl";
//import d3 from "d3";
import Sidebar from "@/components/Sidebar"


  export default {
      name:'Map',
      data () {
          return {
              center: [144.9631, -37.8136],
              zoom: 9,
              melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json',
            //   django_geo: "http://127.0.0.1:8000/api/data.geojson",
            django_geo: "",
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
      created() {
          axios.get(this.django_geo).then(response => {
            this.APIdata = JSON.stringify(response.data)
          });

      },
      mounted() {
          this.getGeoJSON()
          this.createMap();
          this.load_json();
          this.boundingBoxAU();
          this.boundingBoxVIC();

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
                  this.map.resize();
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
      },

  }
</script>
<style>
#map-container{
    padding: 0; 
    margin: 0; 
    display: flex;
    height:100%;
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