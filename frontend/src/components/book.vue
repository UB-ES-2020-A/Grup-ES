<template>
<div id="app">
<div>
 <b-navbar toggleable="lg" type="dark" variant="info">
  <b-navbar-brand href="#">NavBar</b-navbar-brand>
  <b-nav-form>
    <b-form-input autocomplete="off" v-model="search"  list="booksearch" @change="onInputDataList()" id="inputsearch" size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
     <datalist id="booksearch">
       <option v-for="book in filteredList" :key="book.isbn" :value="book.titulo" :id="book.isbn">
        {{ book.autor }}
      </option>
     </datalist>
     <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
     <b-icon icon="three-dots-vertical" v-b-modal.modal-1 font-scale="2"></b-icon>

     <b-modal
     id="modal-1"
     title="Cerca avançada"
     @ok="handleOk">
       <form ref="form" @submit.stop.prevent="handleSubmit">
         <b-form-group
           :state="isbnState"
           label="ISBN"
           label-for="isbn-input"
           invalid-feedback="ISBN invalid, use a 13 digit number"
         >
         <b-form-input
           id="isbn-input"
           v-model="isbn"
           :state="isbnState"
           required
         ></b-form-input>
       </b-form-group>
       <b-form-group
         label="Titol"
         label-for="title-input"
       >
       <b-form-input
         id="title-input"
         v-model="title"
       ></b-form-input>
     </b-form-group>

     <b-form-group
       label="Autor"
       label-for="autor-input"
     >
       <b-form-input
         id="autor-input"
         v-model="autor"
       ></b-form-input>
     </b-form-group>

     <b-form-group
       label="Editorial"
       label-for="editorial-input"
     >
     <b-form-input
       id="editorial-input"
       v-model="editorial"
     ></b-form-input>
   </b-form-group>
     </form>
     <p> Info: Minimum fields required is 1 <p>
     </b-modal>
  </b-nav-form>
  <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
  <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
    <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></b-icon></a></li>
    <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon></a></li>
    <li class="nav-item"><a class="nav-link"><b-button variant="danger" @click="logIn()">{{ session_status }}</b-button>
 </a></li>
<li class="nav-item" v-if= "session_boolean === true"><a class="nav-link"><h4> {{ this.user.username }}</h4></a></li>
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
          <img :src="getURL(item.book)" style="height:109px; width:70px;" alt=""  @click = "gotobook(item.book.isbn)">
          </b-col>
          <b-col>
          <h6 @click = "gotobook(book.isbn)"> {{ item.book.titulo }}</h6>
          <h5> {{ item.book.autor }}</h5>
          </b-col>
          <b-col>
          <b-row>
          <h6>{{ total_amount(item.book, item.quantity) }}</h6>
          </b-row>
          <br>
          <b-row>
          <b-form-spinbutton id="sb-inline" v-model="item.quantity" @change="save_quantity(item.book, item.quantity)"
            min="1" style="width:45%"></b-form-spinbutton>
          </b-row>
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
      price: 0.0,
      session_status: 'Log In',
      session_boolean: false,
      user: {},
      booksquery: [],
      search: '',
      isbn: '',
      isbnState: null,
      title: '',
      autor: '',
      editorial: '',
      advancedsearch: []
    }
  },
  created () {
    this.load_book()
    this.fetch_cache()
    this.get_books()
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
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
    },
    total_amount (book, quantity) {
      return Number(book.precio * quantity).toFixed(2)
    },
    calculate_total_price () {
      var price = 0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price += this.total_amount(this.cartItems[i].book, this.cartItems[i].quantity)
      }
      this.price = price
      return Number(this.price).toFixed(2)
    },
    save_quantity (book, quantity) {
      var i
      console.log('hola')
      for (i = 0; i < this.cartItems.length; i++) {
        if (book.isbn === this.cartItems[i].book.isbn) {
          this.cartItems[i].quantity = quantity
        }
      }
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
      console.log(quantity)
    },
    fetch_cache () {
      var tmpitems = JSON.parse(localStorage.getItem('cartItems'))
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpitems !== null) {
        this.cartItems = tmpitems
      }
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    logIn () {
      if (this.session_boolean === false) {
        this.$router.push({path: '/userlogin'})
      } else {
        localStorage.removeItem('user_session')
        localStorage.removeItem('cartItems')
        this.cartItems.splice(0, this.cartItems.length)
        this.session_status = 'Log In'
        this.session_boolean = false
        alert('Log out successfully')
      }
    },
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
      this.load_book()
      this.search = ''
    },
    get_books () {
      const path = 'https://grup-es.herokuapp.com/books'
      axios.get(path)
        .then((res) => {
          this.booksquery = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    },
    onInputDataList () {
      var datalist = document.getElementById('booksearch').childNodes
      var input = document.getElementById('inputsearch').value
      for (var i = 0; i < datalist.length; i++) {
        if (datalist[i].value === input) {
          this.gotobook(datalist[i].id)
          break
        }
      }
    },
    checkOk () {
      if (this.isbn.length === 13) {
        this.isbnState = true
      } else {
        this.isbnState = false
      }
      if (this.isbnState || (this.title.length > 0 || this.autor.length > 0 || this.editorial.length > 0)) {
        this.$nextTick(() => {
          this.$bvModal.hide('modal-1')
        })
        this.isbnState = true
        this.clearModal()
        return true
      }
      return false
    },
    handleOk (bvModalEvt) {
      bvModalEvt.preventDefault()
      this.checkOk()
    },
    clearModal () {
      this.isbn = ''
      this.title = ''
      this.autor = ''
      this.editorial = ''
      this.isbnState = null
    },
    getAdvancedSearch (parameters) {
      const path = 'https://grup-es.herokuapp.com/search'
      axios.get(path, parameters)
        .then((res) => {
          this.advancedsearch = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    }
  },
  computed: {
    filteredList () {
      if (this.booksquery.length !== 0 && this.search !== '') {
        return this.booksquery.books.filter(book => book.titulo.toLowerCase().includes(this.search.toLowerCase()))
      } else {
        return ''
      }
    }
  }
}
</script>
