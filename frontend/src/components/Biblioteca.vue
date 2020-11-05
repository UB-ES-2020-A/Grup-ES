<template>
<div id="app">
  <!--navbar-->
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand> NavBar</b-navbar-brand>
   <b-nav-form>
      <b-form-input size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
      <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
   </b-nav-form>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
   <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></b-icon></a></li>
   <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon>
</a></li>
   <li class="nav-item"><a class="nav-link"><b-button variant="danger" @click="logIn()">Log In</b-button>
</a></li>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>
<!--body-->
<b-container fluid="sm" style="margin-left:100px; margin-right:50px">
<b-container fluid style="height: 100px; background: #808080;" >
  <b-row align-h="end">
    <b-col cols="3">
      <b-input-group class="mb-2" style="margin-top:25px">
      <b-input-group-prepend is-text>
        <b-icon icon="search"></b-icon>
      </b-input-group-prepend>
      <b-form-input type="search" placeholder="Search terms"></b-form-input>
    </b-input-group>
    </b-col>
  </b-row>
  </b-container>
  <!--select biblio-->
  <b-row>
    <b-col cols="2">
    <b-form-select
      v-model="selected"
      :options="options"
      class="mb-3"
      value-field="value"
      text-field="text"
      disabled-field="notEnabled"
      style="margin-top: 20px"
    ></b-form-select>
    </b-col>
  </b-row>
  <hr>
  <b-row align-h="end">
    <b-col cols="3">
    <b-form-select
      v-model="sFilter"
      :options="filters"
      class="mb-3"
      value-field="value"
      text-field="filter"
      disabled-field="notEnabled"
    ></b-form-select>
    </b-col>
  </b-row>

  <b-row>
    <div class="form-control bg-light">
     <b-row>
     <div class="col-2"  style="margin-left:30px; margin-top:50px" v-for="(book) in new_releases" :key="book.isbn">
       <b-col align-self="center">
       <img :src="getURL(book)" style="height:409px; width:240px;" alt=""  @click = "gotobook(book)">
       <b-col align-self="center" style="margin-top: 10px">
       <h4 @click = "gotobook(book)">  {{ book.titulo }}</h4>
       </b-col>
       <b-col align-self="center">
       <h7>{{ book.autor }}</h7>
       </b-col>
       </b-col>
     </div>
     </b-row>
     </div>
  </b-row>
</b-container>
<br>
<br>
<footer style="height:auto; background-color:black;">
<h5 style="color:white; padding:20px; margin:0; text-align:center; bottom:0;">Contact, bla, bla</h5>
</footer>
</div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      best_sellers: [],
      new_releases: [],
      cartItems: [],
      see_cart: false,
      items: 0,
      price: 0.0,
      selected: 'A',
      sFilter: 'A',
      options: [
        { value: 'A', text: 'Mis Libros' },
        { value: 'B', text: 'Sin Leer' }
      ],
      filters: [
        { value: 'A', filter: 'Fecha de inclusión: Más reciente' },
        { value: 'B', filter: 'Fecha de inclusión: Más antiguos' },
        { value: 'C', filter: 'Titulo: de A a Z' },
        { value: 'D', filter: 'Titulo: de Z a A' },
        { value: 'E', filter: 'Autor: de A a Z' },
        { value: 'F', filter: 'Autor: de Z a A' }
      ]
    }
  },
  created () {
    this.load_new_releases()
  },
  methods: {
    gotobook (book) {
      this.$router.push({ path: '/book', query: {bk: book.isbn} })
    },
    load_best_sellers () {
      const path = 'https://grup-es.herokuapp.com/books'
      const params = { numBooks: 2, param: 'isbn', order: 'asc' }
      axios.get(path, params)
        .then((res) => {
          this.best_sellers = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_new_releases () {
      const path = 'https://grup-es.herokuapp.com/books'
      const params = { numBooks: 2, param: 'isbn', order: 'asc' }
      axios.get(path, params)
        .then((res) => {
          this.new_releases = res.data.books
        })
        .catch((error) => {
          console.error(error)
        })
    },
    add_cart (book) {
      var alreadyIn = false
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        if (book.isbn === this.cartItems[i].book.isbn) {
          this.cartItems[i].quantity += 1
          alreadyIn = true
        }
      }
      if (!alreadyIn) {
        this.cartItems.push({'book': book, 'quantity': 1})
      }
    },
    show_cart () {
      this.see_cart = !this.see_cart
    },
    total_amount (price, quantity) {
      return price * quantity
    },
    calculate_total_price () {
      var price = 0.0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price += this.total_amount(this.cartItems[i].book.precio, this.cartItems[i].quantity)
      }
      this.price = price
      return this.price
    },
    getURL (book) {
      return book.url_imagen
    },
    logIn () {
      this.$router.push({path: '/userlogin'})
    },
    return_book (item) {
      var deleteIdx = this.cartItems.indexOf(item)
      this.items -= 1
      if (deleteIdx !== -1) {
        this.cartItems.splice(deleteIdx, 1)
      }
    }

  }
}
</script>
