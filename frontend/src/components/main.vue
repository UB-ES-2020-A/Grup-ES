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
  fade
  style="text-shadow: 0px 0px 2px #0000"
  :interval="5000"
  >
  <b-carousel-slide v-for="i in 3" :key = "i"
      :img-src="loadSlides(i)"
  >
    <h1 style="color: black;"> Troba les millors novetats a BookShelter </h1>
  </b-carousel-slide>
  <b-carousel>
</b-container>
<br>
<div class="container" v-if= "show === true">
   <h3> Best sellers </h3>
   <br>
   <h5> Els llibres que arrasen <h5>
   <b-row>
     <b-col  v-for="(book) in best_sellers" :key="book.isbn">
       <br>
       <b-card
          img-alt="Image"
          img-top
          tag="article"
          style="max-width: 15rem;"
          class="mb-2"
        >
      <a> <b-card-img :src="getURL(book)"  @click = "gotobook(book.isbn)">
        </b-card-img> </a>
      <br>
      <a> <b-card-title @click = "gotobook(book.isbn)"> {{ book.titulo }} </b-card-title> </a>
      <b-card-text>
        <h5>{{ book.autor }}</h5>
      </b-card-text>
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
      <b-card-text>
        <h6>Preu: {{ book.precio }}</h6>
      </b-card-text>
        <b-button v-if="user.role == userRole" variant="danger" @click="add_cart(book)">Add to cart</b-button>
      </b-card>
      </b-col>
   </b-row>
</div>
   <br>
   <br>
  <div class="container" v-if= "show === true">
      <h3> New releases </h3>
      <br>
      <h5> Nous llibres que no et deixaran indiferent <h5>
      <b-row>
      <b-col  v-for="(book) in new_releases" :key="book.isbn">
        <br>
        <b-card
           img-alt="Image"
           img-top
           tag="article"
           style="max-width: 15rem;"
           class="mb-2"
         >
       <a> <b-card-img :src="getURL(book)"  @click = "gotobook(book.isbn)">
         </b-card-img> </a>
       <br>
       <a> <b-card-title @click = "gotobook(book.isbn)"> {{ book.titulo }} </b-card-title> </a>
       <b-card-text>
         <h5>{{ book.autor }}</h5>
       </b-card-text>
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
       <b-card-text>
         <h6>Preu: {{ book.precio }}</h6>
       </b-card-text>
         <b-button v-if="user.role == userRole" variant="danger" @click="add_cart(book)">Add to cart</b-button>
       </b-card>
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
      show: true,
      user: {},
      userRole: 'User'
    }
  },
  created () {
    this.fetch_cache()
    this.load_new_releases()
    this.load_best_sellers()
  },
  methods: {
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    load_best_sellers () {
      const path = this.$API_URL + 'trending'
      const params = { numBooks: 5, score: true }
      axios.get(path, { params: params })
        .then((res) => {
          this.best_sellers = res.data.books
          this.best_sellers = this.check_vendible(this.best_sellers)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_new_releases () {
      const path = this.$API_URL + 'books'
      const params = { numBooks: 5, param: 'isbn', order: 'asc', score: true }
      axios.get(path, { params: params })
        .then((res) => {
          this.new_releases = res.data.books
          this.new_releases = this.check_vendible(this.new_releases)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    check_vendible (array) {
      var i
      var arr = []
      for (i = 0; i < array.length; i++) {
        if (array[i].vendible) {
          arr.push(array[i])
        }
      }
      return arr
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
