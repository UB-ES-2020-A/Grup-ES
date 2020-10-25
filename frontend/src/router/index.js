import Vue from 'vue'
import Router from 'vue-router'
import DeleteBooks from '@/components/DeleteBooks.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'delete_books',
      component: DeleteBooks
    }
  ]
})
