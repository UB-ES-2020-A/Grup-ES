import { BootstrapVue, BootstrapVueIcons } from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router/index.js'
import GoogleSignInButton from 'vue-google-signin-button-directive'

Vue.use(BootstrapVue)
Vue.use(BootstrapVueIcons)
Vue.config.productionTip = false
Vue.prototype.$API_URL = 'http://localhost:5000/'

new Vue({
  router,
  GoogleSignInButton,
  render: (h) => h(App)
}).$mount('#app')
