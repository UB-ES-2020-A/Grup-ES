import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main.vue'
import book from '@/components/book.vue'
import cart from '@/components/cart.vue'
Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'main',
      component: main
    },
    {
      path: '/book',
      name: 'book',
      component: book
    },
    {
      path: '/cart',
      name: 'cart',
      component: cart
    }
  ]
})
