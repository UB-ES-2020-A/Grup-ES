<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand> NavBar</b-navbar-brand>
   <b-nav-form>
      <b-form-input autocomplete="off" v-model="search"  list="booksearch" @change="onInputDataList()" id="inputsearch" size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
      <datalist id="booksearch">
        <option v-for="book in filteredList" :key="book.isbn" :value="book.titulo" :id="book.isbn">
          {{ book.autor }}
        </option>
      </datalist>
      <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
   </b-nav-form>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
   <li class="nav-item"><a class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></b-icon></a></li>
   <li class="nav-item"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon>
</a></li>
   <li class="nav-item"><a class="nav-link"><b-button variant="danger" @click="logIn()">{{ session_status }}</b-button>
</a></li>
<li class="nav-item" v-if= "session_boolean === true">
    <b-nav-item-dropdown id="my-nav-dropdown" :text="this.user.username" toggle-class="nav-link-custom" right>
    <b-dropdown-item @click="goLibrary()">Biblioteca</b-dropdown-item>
    <b-dropdown-item @click="goPedidos()">Mis Pedidos</b-dropdown-item>
    </b-nav-item-dropdown>
</li>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>

<!-- body -->
<b-container>
  <div class="row d-flex justify-content-center">
  <div class="col-lg">
  <div class="form-control bg-light" style="margin-top: 100px">
  <div class="form-label-group">
    <div style="margin-top: 10px" class="row justify-content-center"><h4>Targeta de Crèdit</h4></div>

    <b-row style="margin-top: 15px">
      <b-col cols="6">
        <label>Número de Targeta</label>
        <input id="card_number" class="form-control" type="number"
        placeholder="#### #### #### ####" required autofocus v-model="card_number">
      </b-col>
      <b-col cols="6">
        <label>Nom del titular</label>
        <input id="card_holder_name" class="form-control"
        placeholder="NOM COGNOM" required autofocus v-model="card_holder_name">
      </b-col>
    </b-row>

    <b-row style="margin-top: 15px">
      <b-col cols="6">
        <label>Data de caducitat</label>
        <b-row>
          <b-col cols="4">
            <input id="month" class="form-control" type="number"
            placeholder="01" required autofocus v-model="month">
          </b-col>
          <b-col cols="8">
            <input id="year" class="form-control" type="number"
            placeholder="2021" required autofocus v-model="year">
          </b-col>
        </b-row>
      </b-col>
      <b-col cols="6">
        <label>CVC</label>
        <input id="card_cvc" class="form-control" type="number"
        placeholder="0000" required autofocus v-model="card_cvc">
      </b-col>
    </b-row>
    <br>
    <h5>Total a pagar: {{ calculate_total_price() }}$</h5>
    <b-col>
      <b-button size="lg" variant="primary" style="margin-top: 15px" @click="submitCard()">Submit</b-button>
    </b-col>
    <b-row style="margin-top: 10px"></b-row>
    <label v-if="show" style="color: red">{{this.error}}</label>
  </div>
  </div>
  </div>
  </div>
</b-container>

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
          <h6>{{ total_amount(item.book, item.quantity) }} $</h6>
          </b-row>
          <br>
          <b-row>
          <b-form-spinbutton id="sb-inline" v-model="item.quantity" @change="save_quantity(item.book, item.quantity)"
           min="1" style="width:45%"></b-form-spinbutton>
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
      cartItems: [],
      see_cart: false,
      price: 0.0,
      user: {},
      session_status: 'Log In',
      session_boolean: false,
      search: '',
      booksquery: [],
      error: '',
      show: false
    }
  },
  created () {
    this.fetch_cache()
    this.get_books()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
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
      return Number(book.precio * quantity).toFixed(2)
    },
    calculate_total_price () {
      var price = 0.0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price += this.total_amount(this.cartItems[i].book, this.cartItems[i].quantity)
      }
      this.price = price
      return Number(this.price).toFixed(2)
    },
    getURL (book) {
      return book.url_imagen
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
    return_book (item) {
      var deleteIdx = this.cartItems.indexOf(item)
      if (deleteIdx !== -1) {
        this.cartItems.splice(deleteIdx, 1)
      }
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
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
        console.log(this.user.username)
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    goLibrary () {
      this.$router.push({path: '/biblioteca'})
    },
    goPedidos () {
      this.$router.push({path: '/mispedidos'})
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
    checkForm: function (e) {
      this.errors = []

      if (!this.card_number || !this.card_holder_name || !this.card_cvc || !this.year || !this.month) {
        this.errors.push('És requereix emplenar tots els camps!')
      }

      if (this.card_number > 9999999999999999999 || this.card_number < 1000000000000) {
        this.errors.push('Número de targeta no vàlid!')
      }

      if (this.year > 2026 || this.year < 2020 || this.month < 1 || this.month > 12) {
        this.errors.push('Data de caducitat no vàlida!')
      }

      if (this.card_cvc < 100 || this.card_cvc > 9999) {
        this.errors.push('CVC no vàlid!')
      }

      if (!this.errors.length) {
        this.show = false
        return true
      }
      this.show = true
      this.error = this.errors[0]
      return false
    },
    addToLibrary (parameters) {
      const path = 'https://grup-es.herokuapp.com/library'
      axios.post(path, parameters, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          console.log('BOOK ADDED TO LIBRARY')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    post_transaction (book, quantity) {
      const parameters = {
        isbn: book.isbn,
        price: book.precio,
        email: this.user.email,
        quantity: quantity
      }
      const path = 'https://grup-es.herokuapp.com/transaction'
      axios.post(path, parameters, {auth: {username: this.user.token}})
        .then((res) => {
          console.log('PAID SUCCESSFULLY')
          alert('Transaction correctly realized!')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    submitCard () {
      if (this.checkForm()) {
        for (var i = 0; i < this.cartItems.length; i++) {
          this.post_transaction(this.cartItems[i].book, this.cartItems[i].quantity)
          const parameters = {
            isbn: this.cartItems[i].book.isbn,
            email: this.user.email
          }
          this.addToLibrary(parameters)
        }
        this.cartItems = []
        localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
      }
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
