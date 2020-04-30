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
import 'swiper/css/swiper.css'

import Swiper from 'swiper'
import VueAwesomeSwiper from 'vue-awesome-swiper'

Vue.config.productionTip = false;
Vue.use(infiniteScroll);
Vue.use(AOS)
Vue.use(ChartPlugin)
AOS.init()
Vue.use(VueAwesomeSwiper, {})

new Vue({
  Swiper,
  vuetify,
  router,
  store,
  render: h => h(App)
}).$mount("#app");
