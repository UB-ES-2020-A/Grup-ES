<template>
<div id="app">
 <navbar ref="c" @changeShowState="show = !show"/>
<div class="body">
<div class="container" v-if= "show === true">
  <br>
  <br>
   <h3> Resultats de la cerca </h3>
   <b-row>
     <b-col  v-for="(book) in books" :key="book.isbn">
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
   <b-row v-if="books.length === 0">
    <h3 class = "text-muted">
      No hi han hagut resultats coincidents amb la cerca
      <b-icon icon="search" font-scale="2.5"></b-icon>
    </h3>
   </b-row>
</div>

<!-- footer -->
<br>
<br>
</div>
<foot/>
</div>
</template>

<script>
import axios from 'axios'
import navbar from './subcomponents/navbar'
import foot from './subcomponents/foot'

export default {
  components: {
    navbar,
    foot
  },
  data () {
    return {
      show: true,
      user: {},
      books: [],
      userRole: 'User'
    }
  },
  created () {
    this.fetch_cache()
    this.load_search(this.$route.query)
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    load_search (query) {
      const path = this.$API_URL + 'search'
      const params = query
      params['score'] = true

      axios.get(path, { params: params })
        .then((res) => {
          this.books = res.data.books
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
  },
  beforeRouteUpdate (to, from, next) {
    this.load_search(to.query)
    next()
  }
}
</script>
