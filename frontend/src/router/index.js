import Vue from 'vue'
import Router from 'vue-router'
import DeleteBooks from '@/components/DeleteBooks.vue'
import main from '@/components/main.vue'
import book from '@/components/book.vue'
import ModifyBooks from '@/components/ModifyBooks.vue'
import Login from '@/components/Login.vue'
import AddBooks from '@/components/AddBooks.vue'
import RegisterForm from '@/components/RegisterForm.vue'
import resetPassword from '@/components/resetPassword.vue'
import Biblioteca from '@/components/Biblioteca.vue'
import changePassword from '@/components/changePassword.vue'

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
      path: '/modify',
      name: 'modify_books',
      component: ModifyBooks
    },
    {
      path: '/userregister',
      name: 'RegisterForm',
      component: RegisterForm
    },
    {
      path: '/delete',
      name: 'delete_books',
      component: DeleteBooks
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
    },
    {
      path: '/reset',
      name: 'resetPassword',
      component: resetPassword
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
    }
  ]
})
