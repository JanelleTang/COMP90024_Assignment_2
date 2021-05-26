 
// # ============= COMP90024 - Assignment 2 ============= #
// #                               
// # The University of Melbourne           
// # Team 37
// #
// # ** Authors: **
// # 
// # JJ Burke              1048105
// # Janelle Tang          694209
// # Shuang Qiu            980433
// # Declan Baird-Watson   640975
// # Avinash Rao           1024577 
// # 
// # Location: Melbourne
// # ==================================================== #

import Vue from "vue";
import App from "./App.vue";
import router from './routes/router.js'
import * as VueGoogleMaps from 'vue2-google-maps'
import BootstrapVue from 'bootstrap-vue'
import vuetify from '@/plugins/vuetify' // path to vuetify export
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'

Vue.use(VueGoogleMaps, {
  load: {
    key: 'AIzaSyAEzPa6JQe9jpdO1XY3oocY8a3GtMtvdv0',
    libraries: 'places'
  }
})

Vue.use(BootstrapVue)
Vue.config.productionTip = false;

new Vue({
  router,
  vuetify,
  render: (h) => h(App),
}).$mount("#app");
