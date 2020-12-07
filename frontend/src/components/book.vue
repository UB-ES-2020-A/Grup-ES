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
          <b-button style="width:100%" variant="dark" @click="add_wishlist(single_book)"> Afegir a la llista de desitjos</b-button>
          </b-container>
        </b-col>
      </b-row>
  </b-container>
  <br>
  <br>
  <!--Sección de reviews-->
  <b-container class='bg-info rounded'>
      <br>
      <div v-if="can_post === true">
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
      </div>
      <v-row v-for="(review) in this.single_book.reviews" :key="review.user_id">
        <div class="card">
          <div class="card-body">
            <div v-if="!is_modifying(review)">
            <b-row>
              <b-col>
                <h5 class="card-title">
                  <div>
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
                  </div>
                </h5>
              </b-col>
              <b-col>
                <div class="text-right text-top" style="height=100px">
                  <b-icon icon="pencil-fill" v-if="modify_visibility(review)" font-scale="1" @click="change_modify_state(review)"></b-icon>
                  <b-icon icon="trash-fill" v-if="delete_visibility(review)" font-scale="1" v-b-modal.conf-del @click="set_focus(review)"></b-icon>
                </div>
              </b-col>
            </b-row>
            <h6 class="card-subtitle mb-2 text-muted">{{review.username}} with id {{review.user_id}} commented:</h6>
            <p class="card-text">{{review.review}}</p>
            </div>
            <form ref="review-form" v-if="is_modifying(review)">
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
                <b-form-textarea id="review-modify-input" v-model="review_modify_input" placeholde="Añade un comentario">
                </b-form-textarea>
              </b-form-group>
              <div class="text-right">
                <button type="button" class="btn btn-danger" @click="change_modify_state(review)">CANCEL</button>
                <button type="button" class="btn btn-dark" @click="modify(review, single_book, user)">OK</button>
              </div>
            </form>
          </div>
        </div>
        <br>
      </v-row>
  </b-container>
  </div>
  </div>
  <foot/>
  <b-modal
    id="conf-del"
    title="Seguro que quiere eliminar la review?"
    @ok="delete_review(focused_review)">
    <p> Atención: está acción es irreversible! <p>
  </b-modal>
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
      // Roles
      adminRole: 'Admin',

      show: true,
      can_post: true,

      // LogIn status
      user: {},
      session_boolean: false,

      score: 1,
      review: '',
      single_book: {},

      // Delete
      focused_review: {},

      // Modify
      modifying_review: {},
      modifying: false,
      review_modify_input: ''
    }
  },
  created () {
    this.fetch_login_status()
    this.load_book(this.$route.query)
  },
  methods: {
    load_book (query) {
      const path = this.$API_URL + 'book/' + query.bk
      const params = {
        reviews: true,
        score: true
      }
      axios.get(path, { params: params })
        .then((res) => {
          this.single_book = res.data.book
          this.redirectNotFound(this.single_book)
          this.can_post = true
          var i
          console.log(this.single_book)
          console.log(this.single_book.reviews)
          for (i = 0; i < this.single_book.reviews.length; i++) {
            console.log(this.single_book.reviews[i])
            if (this.single_book.reviews[i].user_id === this.user.id) {
              this.can_post = false
            }
          }
        })
        .catch((error) => {
          console.error(error)
        })
    },
    redirectNotFound (book) {
      if (book.vendible === false) {
        // redirigir a not found page
        console.log('not vendible')
      }
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
      const path = this.$API_URL + 'review' + '?isbn=' + this.$route.query.bk + '&email=' + user.email + '&score=' + this.score + '&review=' + this.review
      axios.post(path, {}, {auth: {username: this.user.token}})
        .then((res) => {
          this.review = ''
          this.load_book(this.$route.query)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    delete_review (review) {
      const path = this.$API_URL + 'review/' + review.user_id + '/' + review.isbn
      axios.delete(path, {auth: {username: this.user.token}})
        .then((res) => {
          this.load_book(this.$route.query)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    delete_visibility (review) {
      return (review.user_id === this.user.id) || (this.user.role === this.adminRole)
    },
    modify_visibility (review) {
      return review.user_id === this.user.id
    },
    is_modifying (review) {
      return review === this.modifying_review && this.modifying
    },
    change_modify_state (review) {
      this.modifying = !this.modifying
      this.modifying_review = review
      this.review_modify_input = review.review
      this.score = review.score
    },
    modify (review) {
      const path = this.$API_URL + 'review/' + review.user_id + '/' + review.isbn
      const data = {
        score: this.score,
        review: this.review_modify_input
      }
      axios.put(path, data, {auth: {username: this.user.token}})
        .then((res) => {
          this.load_book(this.$route.query)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    set_focus (review) {
      this.focused_review = review
    },
    fetch_login_status () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_boolean = true
      }
    },
    add_wishlist (book) {
      const path = this.$API_URL + 'library/' + this.user.email
      const parameters = {
        isbn: book.isbn,
        library_type: 'WishList',
        state: 'Nan'
      }
      const auth = {auth: {username: this.user.token}}
      axios.post(path, parameters, auth)
        .then((res) => {
          console.log('BOOK ADDED TO WISHLIST')
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  beforeRouteUpdate (to, from, next) {
    this.load_book(to.query)
    next()
  }
}
</script>
