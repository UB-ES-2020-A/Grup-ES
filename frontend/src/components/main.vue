<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand> NavBar</b-navbar-brand>
   <b-nav-form>
      <b-form-input size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
      <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
   </b-nav-form>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
   <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></b-icon></a></li>
   <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon>
</a></li>
   <li class="nav-item"><a class="nav-link"><b-button variant="danger" @click="logIn()">Log In</b-button>
</a></li>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>
<!-- container for static pics -->
<br>
<br>
<b-container v-if= "see_cart === false">
 <img :src="'https://placehold.it/1100x300/?text=' + picturestock" alt="">
</b-container>
<br>

<div class="container" v-if= "see_cart === false">
   <h3> Best sellers </h3>
   <b-row>
     <b-col  v-for="(book) in best_sellers" :key="book.isbn">
       <br>
       <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book)">
       <h6  @click = "gotobook(book)">{{ book.titulo }}</h6>
       <h5>{{ book.autor }}</h5>
       <h6>Valoració</h6>
       <h6>{{ book.precio }}</h6>
       <b-button variant="danger" @click="add_cart(book)">Add to cart</b-button>
       </b-col>
   </b-row>
</div>
   <br>
   <br>
  <div class="container" v-if= "see_cart === false">
      <h3> New releases </h3>
      <b-row>
      <b-col  v-for="(book) in new_releases" :key="book.isbn">
        <br>
        <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book)">
        <h6 @click = "gotobook(book)">  {{ book.titulo }}</h6>
        <h5>{{ book.autor }}</h5>
        <h6>Valoració</h6>
        <h6>{{ book.precio }}</h6>
        <b-button variant="danger" @click="add_cart(book)">Add to cart</b-button>
      </b-col>
      </b-row>
  </div>
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
          <h6>{{ total_amount(item.book, item.quantity) }} $</h6>
          </b-row>
          <br>
          <b-row>
          <b-form-spinbutton id="sb-inline" v-model="item.quantity" @click="total_amount(item.book, item.quantity);
          calculate_total_price();" min="1" style="width:45%"></b-form-spinbutton>
          </b-row>
          </b-col>
          <b-col>
            <b-button variant="danger" @click="return_book(item)">Eliminar</b-button>
          </b-col>
          <hr/>
      </b-row>
      </b-container>
      </b-col>
      <b-col>
       <b-container fluid class = "border bg-light" style="padding:15px">
        <p> Tens un codi de descompte? </p>
        <b-nav-form>
           <b-form-input size="sm" class="mr-sm-2" placeholder="Introdueix el teu codi descompte"></b-form-input>
           <b-button size="sm" class="my-2 my-sm-0" type="submit">Validar</b-button>
        </b-nav-form>
      </b-container>
      <b-container fluid class = "border bg-light" style="padding:15px; margin-top:10px">
      <br>
        <h5> Resum </h5>
        <br>
        <h6> {{ calculate_total_price() }}$ </h6>
        <hr/>
        <h6> Despeses enviament : Gratuït</h6>
        <hr/>
        <h5> Total : {{ calculate_total_price() }} $ </h5>
        <br>
        <b-button style="width:100%" variant="danger">Finalitzar compra</b-button><br><br>
        </b-container>
      </b-col>
    </b-row>
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
      best_sellers: [],
      new_releases: [],
      cartItems: [],
      see_cart: false,
      price: 0.0,
      user: {}
    }
  },
  created () {
    this.load_new_releases()
    this.fetch_cache()
  },
  methods: {
    gotobook (book) {
      this.$router.push({ path: '/book', query: {bk: book.isbn} })
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
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
    },
    show_cart () {
      this.see_cart = !this.see_cart
    },
    total_amount (book, quantity) {
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        if (book.isbn === this.cartItems[i].book.isbn) {
          this.cartItems[i].quantity = quantity
        }
      }
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
      return book.precio * quantity
    },
    calculate_total_price () {
      var price = 0.0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price += this.total_amount(this.cartItems[i].book, this.cartItems[i].quantity)
      }
      this.price = price
      return this.price
    },
    getURL (book) {
      return book.url_imagen
    },
    logIn () {
      this.$router.push({path: '/userlogin'})
    },
    return_book (item) {
      var deleteIdx = this.cartItems.indexOf(item)
      if (deleteIdx !== -1) {
        this.cartItems.splice(deleteIdx, 1)
      }
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
    },
    fetch_cache () {
      var tmpitems = JSON.parse(localStorage.getItem('cartItems'))
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpitems !== null) {
        this.cartItems = tmpitems
      }
      if (tmpuser !== null) {
        this.userObj = tmpuser
      }
    }
  }
}
</script>
