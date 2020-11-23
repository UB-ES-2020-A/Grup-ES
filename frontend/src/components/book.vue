<template>
  <div id="app">
   <navbar @changeShowState="show = !show"/>
  <div class="body">
   <div v-if="show === true">
   <br>
   <br>
   <b-container v-if= "show === true">
      <b-row>
        <b-col class="text-center" cols="4">
          <br>
          <img :src="getURL(this.single_book)" style="height:436px; width:280px;" alt="" >
          <br>
          <br>
          <b-icon icon="star-fill" v-if="single_book.score >= 1" font-scale="3"></b-icon>
          <b-icon icon="star" v-if="single_book.score < 1" font-scale="3"></b-icon>
          <b-icon icon="star-fill" v-if="single_book.score >= 2" font-scale="3"></b-icon>
          <b-icon icon="star" v-if="single_book.score < 2" font-scale="3"></b-icon>
          <b-icon icon="star-fill" v-if="single_book.score >= 3" font-scale="3"></b-icon>
          <b-icon icon="star" v-if="single_book.score < 3" font-scale="3"></b-icon>
          <b-icon icon="star-fill" v-if="single_book.score >= 4" font-scale="3"></b-icon>
          <b-icon icon="star" v-if="single_book.score<4" font-scale="3"></b-icon>
          <b-icon icon="star-fill" v-if="single_book.score >= 5" font-scale="3"></b-icon>
          <b-icon icon="star" v-if="single_book.score < 5" font-scale="3"></b-icon>
        </b-col>
        <b-col cols="5">
          <br>
          <h2> {{ this.single_book.titulo }} </h2>
          <p> <h4> de {{ this.single_book.autor }} </h4> <p>
          <hr/>
          <h5> Sinopsis </h5>
          <p>
          {{ this.single_book.sinopsis }}
          </p>
        </b-col>
        <b-col class = "justify-content-center">
        <b-container fluid class = "border bg-light" style="padding:15px">
          <h5> Comprar el llibre </h5>
          <b>{{ this.single_book.precio }} $</b>
          <br>
          <br>
          <b-button style="width:100%" variant="danger" @click="add_cart(single_book)">Afegir a la cistella</b-button><br><br>
          <b-button style="width:100%" variant="dark">Comprar ara</b-button><br><br>
          <b-button style="width:100%" variant="dark" > Afegir a la llista de desitjos</b-button>
          </b-container>
        </b-col>
      </b-row>
  </b-container>
  <br>
  <br>
  <!--Sección de reviews-->
  <b-container class='bg-info rounded'>
      <br>
      <form ref="review-form" v-if="session_boolean === true">
        <b-icon icon="star-fill" v-if="score >= 1" @click="score = 1" font-scale="2.5"></b-icon>
        <b-icon icon="star" v-if="score < 1" @click="score = 1" font-scale="2.5"></b-icon>
        <b-icon icon="star-fill" v-if="score >= 2" @click="score = 2" font-scale="2.5"></b-icon>
        <b-icon icon="star" v-if="score < 2" @click="score = 2" font-scale="2.5"></b-icon>
        <b-icon icon="star-fill" v-if="score >= 3" @click="score = 3" font-scale="2.5"></b-icon>
        <b-icon icon="star" v-if="score < 3" @click="score = 3" font-scale="2.5"></b-icon>
        <b-icon icon="star-fill" v-if="score >= 4" @click="score = 4" font-scale="2.5"></b-icon>
        <b-icon icon="star" v-if="score<4" @click="score = 4" font-scale="2.5"></b-icon>
        <b-icon icon="star-fill" v-if="score >= 5" @click="score = 5" font-scale="2.5"></b-icon>
        <b-icon icon="star" v-if="score < 5" @click="score = 5" font-scale="2.5"></b-icon>
        <b-form-group label="Reseña" label-for="review-input">
          <b-form-textarea id="review-input" v-model="review" placeholde="Añade un comentario">
          </b-form-textarea>
        </b-form-group>
        <div class="text-right">
          <button type="button" class="btn btn-dark" @click="submit(single_book, user)">POST</button>
        </div>
      </form>
      <hr>
      <v-row v-for="(review) in this.single_book.reviews" :key="review.user_id">
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">
              <b-icon icon="star-fill" v-if="review.score >= 1" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score < 1" font-scale="2.5"></b-icon>
              <b-icon icon="star-fill" v-if="review.score >= 2" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score < 2" font-scale="2.5"></b-icon>
              <b-icon icon="star-fill" v-if="review.score >= 3" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score < 3" font-scale="2.5"></b-icon>
              <b-icon icon="star-fill" v-if="review.score >= 4" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score<4" font-scale="2.5"></b-icon>
              <b-icon icon="star-fill" v-if="review.score >= 5" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score < 5" font-scale="2.5"></b-icon>
            </h5>
            <h6 class="card-subtitle mb-2 text-muted">user with id {{review.user_id}} commented:</h6>
            <p class="card-text">{{review.review}}</p>
          </div>
        </div>
        <br>
      </v-row>
  </b-container>
  </div>
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

      // LogIn status
      user: {},
      session_boolean: false,

      score: 1,
      review: '',
      single_book: {}
    }
  },
  created () {
    this.load_book()
    this.fetch_login_status()
  },
  methods: {
    load_book () {
      const path = 'https://grup-es.herokuapp.com/book/' + this.$route.query.bk + '?reviews=true&score=true'
      axios.get(path)
        .then((res) => {
          this.single_book = res.data.book
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (book) {
      return book.url_imagen
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
    submit (book, user) {
      const path = 'https://grup-es.herokuapp.com/review' + '?isbn=' + this.$route.query.bk + '&email=' + user.email + '&score=' + this.score + '&review=' + this.review
      axios.post(path, {}, {auth: {username: this.user.token}})
        .then((res) => {
          this.review = ''
          this.load_book()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    fetch_login_status () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_boolean = true
      }
    }
  }
}
</script>
