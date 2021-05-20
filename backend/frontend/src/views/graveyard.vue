



<template>
  <div class="container">
    <h2>Map</h2>
    <div id="map-container"></div>
  </div>
</template>

<script>
import L from "leaflet";
import $ from 'jquery'
import { getAPI } from 'axios'
export default {
  data () {
    return {
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 9,
      center: [-37.8136,144.9631], 
      bounds: null,
      django_geo: "http://172.26.128.53/api/data.geojson",
      melb_geo: 'https://data.gov.au/geoserver/vic-local-government-areas-psma-administrative-boundaries/wfs?request=GetFeature&typeName=ckan_bdf92691_c6fe_42b9_a0e2_a4cd716fa811&outputFormat=json',
      APIData: []
    };
  },
  created () {
            getAPI.get('/api/data.geojson',)
            .then(response => {
            console.log('Post API has recieved data')
            this.APIData = response.data
            })
            .catch(err => {
            console.log(err)
            })
        },
  mounted(){
    this.createMap();
    this.addGeoJSON();
  },
  methods: {
    createMap(){
      this.map = L.map('map-container').setView([-37.8136,144.9631],9);
      this.tileLayer = L.tileLayer(this.url,{
        maxZoom:18,
      });
      this.tileLayer.addTo(this.map);
    },
    
    addGeoJSON(){
      $.getJSON(this.melb_geo, function(data) {
          L.geoJson(data, {
              style: {
                fillColor:"blue",
              }
          }).addTo(this.map);
      });
    },
  }
}
</script>
<style scoped>
#map-container { height: 600px; }
</style>