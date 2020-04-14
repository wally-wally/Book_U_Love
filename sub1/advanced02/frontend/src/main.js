import Vue from 'vue'
import App from './App.vue'

import Vuetify from 'vuetify/lib'
import 'vuetify/dist/vuetify.min.css'
import 'font-awesome/css/font-awesome.min.css'

import ChartPlugin from './plugins/ChartPlugin.js'

import AOS from 'aos'
import 'aos/dist/aos.css'

Vue.prototype.$EventBus = new Vue();
Vue.config.productionTip = false

Vue.use(Vuetify)
Vue.use(ChartPlugin)
Vue.use(AOS)
AOS.init()

new Vue({
  vuetify: new Vuetify({
    iconfont: 'fa',
    theme: {
      primary: '#3f51b5',
      secondary: '#b0bec5',
      accent: '#8c9eff',
      error: '#b71c1c'
    }
  }),
  render: h => h(App),
}).$mount('#app')
