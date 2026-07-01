import Vue from 'vue'
import App from './App.vue'
import router from './router'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import './assets/styles/global.css'
import axios from 'axios';
import store from './store'
import SvgIcon from '@/components/Svgicon/index.vue'
import VueCompositionAPI from '@vue/composition-api';
Vue.component('svg-icon', SvgIcon)
Vue.use(ElementUI)
Vue.use(VueCompositionAPI);
Vue.config.productionTip = false

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
