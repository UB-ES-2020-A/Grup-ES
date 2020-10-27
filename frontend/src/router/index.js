import Vue from 'vue'
import Router from 'vue-router'
import ModifyBooks from '@/components/ModifyBooks.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'modify_books',
      component: ModifyBooks
    }
  ]
})
