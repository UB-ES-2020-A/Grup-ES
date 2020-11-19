<template>
<div id="app">
<!-- container for static pics -->
<navbar @changeShowState="show = !show"/>
<br>
<br>
<b-container v-if= "show === true">
 <img :src="'https://placehold.it/1100x300/?text=' + picturestock" alt="">
</b-container>
<br>

<div class="container" v-if= "show === true">
   <h3> Best sellers </h3>
   <b-row>
     <b-col  v-for="(book) in best_sellers" :key="book.isbn">
       <br>
       <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book.isbn)">
       <h6  @click = "gotobook(book.isbn)">{{ book.titulo }}</h6>
       <h5>{{ book.autor }}</h5>
       <h6>Valoració</h6>
       <h6>{{ book.precio }}</h6>
       <b-button variant="danger" @click="add_cart(book)">Add to cart</b-button>
       </b-col>
   </b-row>
</div>
   <br>
   <br>
  <div class="container" v-if= "show === true">
      <h3> New releases </h3>
      <b-row>
      <b-col  v-for="(book) in new_releases" :key="book.isbn">
        <br>
        <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book.isbn)">
        <h6 @click = "gotobook(book.isbn)">  {{ book.titulo }}</h6>
        <h5>{{ book.autor }}</h5>
        <h6>Valoració</h6>
        <h6>{{ book.precio }}</h6>
        <b-button variant="danger" @click="add_cart(book)">Add to cart</b-button>
      </b-col>
      </b-row>
  </div>
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
import navbar from './subcomponents/navbar'

export default {
  components: {
    navbar
  },
  data () {
    return {
      best_sellers: [],
      new_releases: [],
      show: true
    }
  },
  created () {
    this.load_new_releases()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
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
      var tmpitems = JSON.parse(localStorage.getItem('cartItems'))
      var cartItems = []
      if (tmpitems !== null) {
        cartItems = tmpitems
      }
      var alreadyIn = false
      var i
      for (i = 0; i < cartItems.length; i++) {
        if (book.isbn === cartItems[i].book.isbn) {
          cartItems[i].quantity += 1
          alreadyIn = true
        }
      }
      if (!alreadyIn) {
        cartItems.push({'book': book, 'quantity': 1})
      }
      localStorage.setItem('cartItems', JSON.stringify(cartItems))
    },
    getURL (book) {
      return book.url_imagen
    }
  }
}
</script>
