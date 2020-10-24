import Vue from 'vue'
import Router from 'vue-router'
import AddBooks from '@/components/AddBooks.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'add_books',
      component: AddBooks
    }
  ]
})
