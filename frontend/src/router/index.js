import Vue from 'vue'
import Router from 'vue-router'
import main from '@/components/main.vue'
import book from '@/components/book.vue'
import Login from '@/components/Login.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import resetPassword from '@/components/resetPassword.vue'
import MisPedidos from '@/components/MisPedidos.vue'
import Biblioteca from '@/components/Biblioteca.vue'
import changePassword from '@/components/changePassword.vue'
import PayMethod from '@/components/PayMethod.vue'
import Search from '@/components/Search.vue'
import Stock from '@/components/Stock.vue'
import UserProfile from '@/components/UserProfile.vue'
import Wishlist from '@/components/Wishlist.vue'
import Transactions from '@/components/Transactions.vue'
import NotFound from '@/components/NotFound.vue'

Vue.use(Router)

export default new Router({
  mode: 'history',
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
      path: '/userregister',
      name: 'RegisterForm',
      component: RegisterForm
    },
    {
      path: '/userlogin',
      name: 'Login',
      component: Login
    },
    {
      path: '/reset',
      name: 'resetPassword',
      component: resetPassword
    },
    {
      path: '/mispedidos',
      name: 'MisPedidos',
      component: MisPedidos
    },
    {
      path: '/biblioteca',
      name: 'Biblioteca',
      component: Biblioteca
    },
    {
      path: '/change',
      name: 'changePassword',
      component: changePassword
    },
    {
      path: '/paymethod',
      name: 'PayMethod',
      component: PayMethod
    },
    {
      path: '/search',
      name: 'Search',
      component: Search
    },
    {
      path: '/shopstock',
      name: 'Stock',
      component: Stock
    },
    {
      path: '/profile',
      name: 'UserProfile',
      component: UserProfile
    },
    {
      path: '/wishlist',
      name: 'Wishlist',
      component: Wishlist
    },
    {
      path: '/stocktransactions',
      name: 'Transactions',
      component: Transactions
    },
    {
      path: '/notfound',
      name: 'NotFound',
      component: NotFound
    }
  ]
})
