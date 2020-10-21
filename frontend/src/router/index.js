import Vue from 'vue'
import Router from 'vue-router'
import RegisterForm from '@/components/RegisterForm.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'RegisterForm',
      component: RegisterForm
    }
  ]
})
