<template>
<div id="app">
<!-- container for static pics -->
<navbar @changeShowState="show = !show"/>
<br>
<br>
<div class="body">
<b-container v-if= "show === true">
  <b-carousel
  id="carousel"
  style="text-shadow: 0px 0px 2px #0000"
  :interval="2000"
  img-width="550"
  img-height="300"
  >
  <b-carousel-slide v-for="i in 2" :key = "i"
      :img-src="loadSlides(i)" style="height:550; width:300;"
  ></b-carousel-slide>
  <b-carousel>
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
       <b-icon icon="star-fill" v-if="book.score >= 1" font-scale="1.5"></b-icon>
       <b-icon icon="star" v-if="book.score < 1" font-scale="1.5"></b-icon>
       <b-icon icon="star-fill" v-if="book.score >= 2" font-scale="1.5"></b-icon>
       <b-icon icon="star" v-if="book.score < 2" font-scale="1.5"></b-icon>
       <b-icon icon="star-fill" v-if="book.score >= 3" font-scale="1.5"></b-icon>
       <b-icon icon="star" v-if="book.score < 3" font-scale="1.5"></b-icon>
       <b-icon icon="star-fill" v-if="book.score >= 4" font-scale="1.5"></b-icon>
       <b-icon icon="star" v-if="book.score<4" font-scale="1.5"></b-icon>
       <b-icon icon="star-fill" v-if="book.score >= 5" font-scale="1.5"></b-icon>
       <b-icon icon="star" v-if="book.score < 5" font-scale="1.5"></b-icon>
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
        <b-icon icon="star-fill" v-if="book.score >= 1" font-scale="1.5"></b-icon>
        <b-icon icon="star" v-if="book.score < 1" font-scale="1.5"></b-icon>
        <b-icon icon="star-fill" v-if="book.score >= 2" font-scale="1.5"></b-icon>
        <b-icon icon="star" v-if="book.score < 2" font-scale="1.5"></b-icon>
        <b-icon icon="star-fill" v-if="book.score >= 3" font-scale="1.5"></b-icon>
        <b-icon icon="star" v-if="book.score < 3" font-scale="1.5"></b-icon>
        <b-icon icon="star-fill" v-if="book.score >= 4" font-scale="1.5"></b-icon>
        <b-icon icon="star" v-if="book.score<4" font-scale="1.5"></b-icon>
        <b-icon icon="star-fill" v-if="book.score >= 5" font-scale="1.5"></b-icon>
        <b-icon icon="star" v-if="book.score < 5" font-scale="1.5"></b-icon>
        <h6>{{ book.precio }}</h6>
        <b-button variant="danger" @click="add_cart(book)">Add to cart</b-button>
      </b-col>
      </b-row>
  </div>
<!-- footer -->
</div>
<br>
<br>
<foot/>
</div>
</template>

<script>
import axios from 'axios'
import navbar from './subcomponents/navbar'
import foot from './subcomponents/foot'
import 'bootstrap-vue/dist/bootstrap-vue.css'

export default {
  components: {
    navbar,
    foot
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
      const path = this.$API_URL + 'books'
      const params = { numBooks: 2, param: 'isbn', order: 'asc', score: true }
      axios.get(path, { params: params })
        .then((res) => {
          this.best_sellers = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_new_releases () {
      const path = this.$API_URL + 'books'
      const params = { numBooks: 2, param: 'isbn', order: 'asc', score: true }
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
    },
    loadSlides (imgnum) {
      var image = require('../assets/carousel/book_' + imgnum + '.jpg')
      return image
    }
  }
}
</script>
