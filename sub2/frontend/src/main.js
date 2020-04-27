import Vue from "vue";
import App from "./App.vue";
import '@/utils/filter.js'

import router from '@/router/index.js'
import store from './store/index.js'

import vuetify from "@/plugins/vuetify";
import infiniteScroll from "vue-infinite-scroll";

import AOS from 'aos'
import 'aos/dist/aos.css'

import ChartPlugin from './plugins/ChartPlugin.js'

Vue.config.productionTip = false;
Vue.use(infiniteScroll);
Vue.use(AOS)
Vue.use(ChartPlugin)
AOS.init()

new Vue({
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount("#app");
