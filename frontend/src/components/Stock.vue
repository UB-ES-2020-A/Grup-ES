<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand> NavBar</b-navbar-brand>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
   <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></b-icon></a></li>
   <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon>
</a></li>
   <li class="nav-item"><a class="nav-link"><b-button variant="danger" @click="logIn()">{{ session_status }}</b-button>
</a></li>
<li class="nav-item" v-if= "session_boolean === true">
    <b-nav-item-dropdown id="my-nav-dropdown" :text="this.user.username" toggle-class="nav-link-custom" right>
    <b-dropdown-item @click="goLibrary()">Biblioteca</b-dropdown-item>
    <b-dropdown-item @click="goPedidos()">Mis Pedidos</b-dropdown-item>
    </b-nav-item-dropdown>
</li>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>
<br>

<b-container>
  <b-row>
    <b-col sm="6" md="4" lg="4" xl="4">
    <h4> Llibres en stock : {{ booksquery.books.length }} </h4>
    </b-col>
  </b-row>
</b-container>
<br>
<b-container>
<b-row align-v="center">
    <b-col sm="6" xl="8">
    <b-form-input v-model="search" placeholder="Filter by title"></b-form-input>
    </b-col>
</b-row>
</b-container>
<br>
<br>
<b-container>
 <b-card-group deck v-for="(book) in filteredList" :key="book.isbn">
  <b-card bg-variant="light" text-variant="dark">
  <b-card-title> {{ book.titulo }} - {{ book.isbn }}</b-card-title>
  <b-card-sub-title class="mb-2">{{ book.autor }}</b-card-sub-title>
  <b-card-text>Stock: {{ book.stock }}</b-card-text>
  <b-card-text>PVP: {{ book.precio }} $</b-card-text>
</b-card>
</b-card-group>
</b-container>
<!-- footer -->
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
      booksquery: [],
      search: ''
    }
  },
  created () {
    this.get_books()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    getURL (book) {
      return book.url_imagen
    },
    get_books () {
      const path = 'https://grup-es.herokuapp.com/books'
      axios.get(path)
        .then((res) => {
          this.booksquery = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  computed: {
    filteredList () {
      if (this.booksquery.length !== 0 && this.search !== '') {
        return this.booksquery.books.filter(book => book.titulo.toLowerCase().includes(this.search.toLowerCase()))
      } else {
        return this.booksquery.books
      }
    }
  }
}
</script>
