<template>
  <div id="app">
   <navbar @changeShowState="show = !show"/>
  <div style="display: flex; min-height: 100vh; flex-direction: column;">
   <div v-if="show === true">
   <br>
   <br>
   <b-container v-if= "show === true">
      <b-row>
        <b-col cols="4">
          <br>
          <img :src="getURL(this.single_book)" style="height:436px; width:280px;" alt="" >
          <br>
          <br>
          <h6> Puntuació </h6>
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
      single_book: {}
    }
  },
  created () {
    this.load_book()
  },
  methods: {
    load_book () {
      const path = 'https://grup-es.herokuapp.com/book/' + this.$route.query.bk
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
    }
  }
}
</script>
