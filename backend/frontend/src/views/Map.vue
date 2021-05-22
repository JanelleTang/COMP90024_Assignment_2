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
                Climate Change Sentiment
            </v-card-title>
            <v-card-text>
              <v-list nav dense>
                <v-list-item
                link
                v-for="item in legend_items"
                :key="item.text"
                >
                <v-icon :color="item.color">mdi-square-rounded</v-icon>
                <v-list-item-content>
                    {{ item.text }}
                </v-list-item-content>
                </v-list-item>
              </v-list>

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
              center: [133.7751, -25.2744],
              zoom: 3,
              lga_geodata: "api/lga_data.geojson",
              city_geodata: "api/city_data.geojson",
              // locations: [["Melbourne", 144.9631,-37.8136],
              // ["Sydney",151.2093,-33.8688],
              // ["Adelaide",138.6007,-34.9285],
              // ["Brisbane",153.0260,-27.4705]],
              url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
              bounds: null,
              legend_items:[
                {text: 'High Negative', color:'#DC143C'},
                {text: 'Negative', color:'#FF7F50'},
                {text: 'Low Negative', color:'#ffa53d'},
                {text: 'Neutral', color:'#FFD700'},
                {text: 'Low Positive', color:'#98FB98'},
                {text: 'Positive', color:'#32CD32'},
                {text: 'High Positive', color:'#006400'},
              ]
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
          this.boundingBoxSA();
          this.boundingBoxQLD();
          this.boundingBoxTAS();
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
                          -3,
                          '#DC143C',
                          -2,
                          '#FF7F50',
                          -1,
                          '#ffa53d',
                          0,
                          '#FFD700',
                          1,
                          '#98FB98',
                          2,
                          '#32CD32',
                          3,
                          '#006400',
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
                    var total_sent = parseFloat(e.features[0].properties.sentiment_value)
                    var total_tweets = e.features[0].properties.n_tweets
                    var av_sent = Math.round(total_sent/total_tweets*100)/100
                    new Mapbox.Popup({closeOnClick: true,offset: 5})
                    .setLngLat(e.lngLat)
                    .setHTML(`<b>${e.features[0].properties.display_name}</b> <br/> Average Sentiment: ${av_sent}<br/> Total Tweets: ${total_tweets}`)

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
                        // 'circle-radius': {
                        //   property: 'n_tweets',
                        //   stops:[
                        //     [0,5],
                        //     [100,15],
                        //     [300,25]
                        //     [500,35],
                        //   ]

                        // },
                        'circle-radius': 30,
                        'circle-color': [
                          'match',
                          ['get','sentiment_rank'],
                          -3,
                          '#DC143C',
                          -2,
                          '#FF7F50',
                          -1,
                          '#ffa53d',
                          0,
                          '#FFD700',
                          1,
                          '#98FB98',
                          2,
                          '#32CD32',
                          3,
                          '#006400',
                          /* other */ '#ccc'
                        ],
                        'circle-stroke-color': 'white',
                        'circle-stroke-width': 3,
                        'circle-opacity': 0.6,
                        },
                  });
				  
				  this.map.on('click', 'city-circle', (e) => {
                    var total_sent = parseFloat(e.features[0].properties.sentiment_value)
                    var total_tweets = e.features[0].properties.n_tweets
                    var av_sent = Math.round(total_sent/total_tweets*100)/100
                    new Mapbox.Popup({closeOnClick: true,offset: 5})
                    .setLngLat(e.lngLat)
                    .setHTML(`<b>${e.features[0].properties.display_name}</b> <br/> Average Sentiment: ${av_sent}<br/> Total Tweets: ${total_tweets}`)

                    .addTo(this.map);
                    });
                    
                    // Change the cursor to a pointer when the mouse is over the states layer.
                    this.map.on('mouseenter', 'city-circle', () => {
                    this.map.getCanvas().style.cursor = 'pointer';
                    });
                    
                    // Change it back to a pointer when it leaves.
                    this.map.on('mouseleave', 'city-circle', () => {
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
          boundingBoxNSW(){
            document.getElementById('fit-nsw').addEventListener('click', () => {
              this.map.fitBounds([
              [146.03,-37.22],
              [154.14,-28.43]
                ]);
            });
          },
          boundingBoxSA(){
            document.getElementById('fit-sa').addEventListener('click', () => {
              this.map.fitBounds([
              [141.0027,-38.113],
              [129.0013,-25.763]
                ]);
            });
          },
          boundingBoxTAS(){
            document.getElementById('fit-tas').addEventListener('click', () => {
              this.map.fitBounds([
              [143.7488,-39.1984777],
              [148.084,-45.17305]
                ]);
            });
          },
          boundingBoxQLD(){
            document.getElementById('fit-qld').addEventListener('click', () => {
              this.map.fitBounds([
              [137.994,-29.17926],
              [153.6116,-9.0880]
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
/* .legend-item{
  float:left;
} */
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

.mapboxgl-popup{position:absolute;top:0;left:0;display:flex;will-change:transform;pointer-events:none}.mapboxgl-popup-anchor-top,.mapboxgl-popup-anchor-top-left,.mapboxgl-popup-anchor-top-right{flex-direction:column}.mapboxgl-popup-anchor-bottom,.mapboxgl-popup-anchor-bottom-left,.mapboxgl-popup-anchor-bottom-right{flex-direction:column-reverse}.mapboxgl-popup-anchor-left{flex-direction:row}.mapboxgl-popup-anchor-right{flex-direction:row-reverse}.mapboxgl-popup-tip{width:0;height:0;border:10px solid transparent;z-index:1}.mapboxgl-popup-anchor-top .mapboxgl-popup-tip{align-self:center;border-top:none;border-bottom-color:#fff}.mapboxgl-popup-anchor-top-left .mapboxgl-popup-tip{align-self:flex-start;border-top:none;border-left:none;border-bottom-color:#fff}.mapboxgl-popup-anchor-top-right .mapboxgl-popup-tip{align-self:flex-end;border-top:none;border-right:none;border-bottom-color:#fff}.mapboxgl-popup-anchor-bottom .mapboxgl-popup-tip{align-self:center;border-bottom:none;border-top-color:#fff}.mapboxgl-popup-anchor-bottom-left .mapboxgl-popup-tip{align-self:flex-start;border-bottom:none;border-left:none;border-top-color:#fff}.mapboxgl-popup-anchor-bottom-right .mapboxgl-popup-tip{align-self:flex-end;border-bottom:none;border-right:none;border-top-color:#fff}.mapboxgl-popup-anchor-left .mapboxgl-popup-tip{align-self:center;border-left:none;border-right-color:#fff}.mapboxgl-popup-anchor-right .mapboxgl-popup-tip{align-self:center;border-right:none;border-left-color:#fff}.mapboxgl-popup-close-button{position:absolute;right:0;top:0;border:0;border-radius:0 3px 0 0;cursor:pointer;background-color:transparent}.mapboxgl-popup-close-button:hover{background-color:rgba(0,0,0,.05)}.mapboxgl-popup-content{position:relative;background:#fff;border-radius:3px;box-shadow:0 1px 2px rgba(0,0,0,.1);padding:10px 10px 15px;pointer-events:auto}.mapboxgl-popup-anchor-top-left .mapboxgl-popup-content{border-top-left-radius:0}.mapboxgl-popup-anchor-top-right .mapboxgl-popup-content{border-top-right-radius:0}.mapboxgl-popup-anchor-bottom-left .mapboxgl-popup-content{border-bottom-left-radius:0}.mapboxgl-popup-anchor-bottom-right .mapboxgl-popup-content{border-bottom-right-radius:0}.mapboxgl-popup-track-pointer{display:none}.mapboxgl-popup-track-pointer *{pointer-events:none;user-select:none}.mapboxgl-map:hover .mapboxgl-popup-track-pointer{display:flex}.mapboxgl-map:active .mapboxgl-popup-track-pointer{display:none}.mapboxgl-marker{position:absolute;top:0;left:0;will-change:transform;opacity:1;transition:opacity .2s}.mapboxgl-marker-occluded{opacity:.2}.mapboxgl-user-location-dot,.mapboxgl-user-location-dot:before{background-color:#1da1f2;width:15px;height:15px;border-radius:50%}.mapboxgl-user-location-dot:before{content:"";position:absolute;animation:mapboxgl-user-location-dot-pulse 2s infinite}.mapboxgl-user-location-dot:after{border-radius:50%;border:2px solid #fff;content:"";height:19px;left:-2px;position:absolute;top:-2px;width:19px;box-sizing:border-box;box-shadow:0 0 3px rgba(0,0,0,.35)}@keyframes mapboxgl-user-location-dot-pulse{0%{transform:scale(1);opacity:1}70%{transform:scale(3);opacity:0}to{transform:scale(1);opacity:0}}.mapboxgl-user-location-dot-stale{background-color:#aaa}.mapboxgl-user-location-dot-stale:after{display:none}.mapboxgl-user-location-accuracy-circle{background-color:rgba(29,161,242,.2);width:1px;height:1px;border-radius:100%}.mapboxgl-crosshair,.mapboxgl-crosshair .mapboxgl-interactive,.mapboxgl-crosshair .mapboxgl-interactive:active{cursor:crosshair}.mapboxgl-boxzoom{position:absolute;top:0;left:0;width:0;height:0;background:#fff;border:2px dotted #202020;opacity:.5}@media print{.mapbox-improve-map{display:none}}

</style>