<template>
<div id="app">
<div>
 <b-navbar toggleable="lg" type="dark" variant="info">
  <b-navbar-brand href="#">NavBar</b-navbar-brand>
  <b-nav-form>
     <b-form-input size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
     <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
  </b-nav-form>
  <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
  <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
    <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></a></li>
    <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon></a></li>
    <li class="nav-item"><a class="nav-link"><b-button variant="danger">Log In</b-button>
</a></li>
   </ul>
  </b-navbar-nav>
 </b-navbar>
</div>
 <br>
 <br>
 <b-container v-if= "see_cart === false">
    <b-row>
      <b-col cols="4">
        <br>
        <img :src="getURL()" style="height:436px; width:280px;" alt="" >
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
        <p>
      </b-col>
      <b-col class = "justify-content-center">
      <b-container fluid class = "border bg-light" style="padding:15px">
        <h5> Comprar el llibre </h5>
        <b>{{ this.single_book.precio }} $<b>
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
<!-- cart -->

<b-container v-if= "see_cart === true">
 <h2> CISTELLA {{ this.cartItems.length }} PRODUCTES </h2>
</b-container>
<br>
 <b-container v-if= "see_cart === true">
    <b-row>
      <b-col cols="8">
        <b-container fluid style="padding:35px">
        <b-row class = "border bg-light" v-for="(item) in cartItems" :key="item.book.isbn" style="padding:35px; margin-bottom:10px">
          <b-col>
          <img :src="getURL(item.book)" style="height:109px; width:70px;" alt=""  @click = "gotobook(item.book)">
          </b-col>
          <b-col>
          <h6 @click = "gotobook(book)"> {{ item.book.titulo }}</h6>
          <h5> {{ item.book.autor }}</h5>
          </b-col>
          <b-col>
          <b-row>
          <h6>{{ total_amount(item.book.precio, item.quantity) }}</h6>
          </b-row>
          <br>
          <b-row>
          <b-form-spinbutton id="sb-inline" v-model="item.quantity" @click="total_amount(item.book.precio, item.quantity);
          calculate_total_price();" min="1" style="width:45%"></b-form-spinbutton>
          </b-row>
          </b-col>
          <hr/>
      </b-row>
      </b-container>
      </b-col>
      <b-col>
       <b-container fluid class = "border bg-light" style="padding:15px">
        <p> Tens un codi de descompte? <p>
        <b-nav-form>
           <b-form-input size="sm" class="mr-sm-2" placeholder="Introdueix el teu codi descompte"></b-form-input>
           <b-button size="sm" class="my-2 my-sm-0" type="submit">Validar</b-button>
        </b-nav-form>
      </b-container>
      <b-container fluid class = "border bg-light" style="padding:15px; margin-top:10px">
      <br>
        <h5> Resum </h5>
        <br>
        <h6> {{ this.price }}$ </h6>
        <hr/>
        <h6> Despeses enviament : Gratuït</h6>
        <hr/>
        <h5> Total : {{ this.price }} $ </h5>
        <br>
        <b-button style="width:100%" variant="danger">Finalitzar compra</b-button><br><br>
        </b-container>
      </b-col>
    </b-row>
</b-container>
<footer style="height:auto; background-color:black; bottom:0;">
  <h5 style="color:white; padding:20px; margin:0; text-align:center;">Contact, bla, bla</h5>
</footer>
 </div>
 </template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      single_book: {},
      see_cart: false,
      cartItems: [],
      price: 0.0
    }
  },
  created () {
    this.load_book()
  },
  methods: {
    load_book () {
      const path = 'http://127.0.0.1:5000/book/' + this.$route.query.bk
      axios.get(path)
        .then((res) => {
          this.single_book = res.data.book
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL () {
      return this.single_book.url_imagen
    },
    show_cart () {
      this.see_cart = !this.see_cart
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
    total_amount (price, quantity) {
      return price * quantity
    },
    calculate_total_price () {
      var price = 0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price += this.total_amount(this.cartItems[i].book.precio, this.cartItems[i].quantity)
      }
      this.price = price
    }

  }
}
</script>
