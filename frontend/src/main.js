import Vue from 'vue'
import App from './App.vue'
import router from './router.js'
import BootstrapVue from "bootstrap-vue";
import "bootstrap-vue/dist/bootstrap-vue.css";
import "bootstrap/dist/css/bootstrap.min.css";
import 'mapbox-gl/dist/mapbox-gl.css';
import 'mapbox-gl/dist/mapbox-gl.js';
import * as VueGoogleMaps from 'vue2-google-maps'

Vue.config.productionTip = false
Vue.use(BootstrapVue);
Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAEzPa6JQe9jpdO1XY3oocY8a3GtMtvdv0',
    libraries: 'places'
  }
})

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')


 