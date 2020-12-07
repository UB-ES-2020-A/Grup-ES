<template>
<div id="app">
 <navbar @changeShowState="show = !show"/>
<div class="body">
<div class="container" v-if= "show === true">
  <br>
  <br>
   <h3> Resultados de la búsqueda </h3>
   <b-row>
     <b-col  v-for="(book) in books" :key="book.isbn">
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

      books: []
    }
  },
  created () {
    this.load_search(this.$route.query)
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    load_search (query) {
      const path = this.$API_URL + 'search'
      const params = query
      params['score'] = true

      axios.get(path, { params: params })
        .then((res) => {
          this.books = res.data.books
          this.books = this.check_vendible(this.books)
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
    }
  },
  beforeRouteUpdate (to, from, next) {
    this.load_search(to.query)
    next()
  }
}
</script>
