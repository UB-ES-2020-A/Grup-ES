import Vue from 'vue'
import Router from 'vue-router'
import RegisterForm from '@/components/RegisterForm.vue'
import ModifyBooks from '@/components/ModifyBooks.vue'
import Login from '@/components/Login.vue'
import AddBooks from '@/components/AddBooks.vue'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/userregister',
      name: 'RegisterForm',
      component: RegisterForm
    },
    {
      path: '/modify',
      name: 'modify_books',
      component: ModifyBooks
    },
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/add',
      name: 'AddBooks',
      component: AddBooks
    }
  ]
})
