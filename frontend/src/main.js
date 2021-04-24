import Vue from "vue";
import App from "./App.vue";
// import ElementUI from "element-ui";
// import "element-ui/lib/theme-chalk/index.css";
// import locale from "element-ui/lib/locale/lang/en";
import router from "./router";

// Vue.use(ElementUI, { locale });

import axios from "axios";
Vue.prototype.axios = axios;

Vue.config.productionTip = false;

new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
