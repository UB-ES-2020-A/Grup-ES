import BootstrapVue from 'bootstrap-vue'
import '@/../bootstrap/css/bootstrap.css'
import Vue from 'vue'
import App from './App.vue'
import router from './router'
import GoogleSignInButton from 'vue-google-signin-button-directive'

Vue.use(BootstrapVue)
Vue.config.productionTip = false

new Vue({
  router,
  GoogleSignInButton,
  render: (h) => h(App)
}).$mount('#app')
