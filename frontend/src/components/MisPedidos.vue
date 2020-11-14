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
<li class="nav-item" v-if= "session_boolean === true"><a class="nav-link"><h4> {{ this.user.username }}</h4></a></li>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>

<!-- body -->
<div v-if= "session_boolean === true">
  <br>
  <br>
  <div class="container" v-if= "see_cart === false">
    <h3> Mis Pedidos </h3>
    <b-row>
      <b-col  v-for="(pedido) in pedidos" :key="pedido.id_transaction">
        <!-- ATR:
        .isbn,
        .price,
        .id_user,
        .quantity,
        .date-->
        <br>
        <h5>Factura: {{ pedido.id_transaction}}</h5>
        <b-col>
        <img :src="getURL(pedido.book)" style="height:109px; width:70px;" alt=""  @click = "gotobook(pedido.book.isbn)">
        </b-col>
        <br>
        <h6 @click = "gotobook(book.isbn)">Título del libro: {{ pedido.book.titulo }}</h6>
        <h6>Autor del libro: {{ pedido.book.autor }}</h6>
        <h6>Precio: {{ pedido.price}}</h6>
        <h6>Cantidad: {{ pedido.quantity}}</h6>
        <h6>Fecha de compra: {{ pedido.date}}</h6>
      </b-col>
    </b-row>
  </div>
</div>
<div v-if= "session_boolean === false">
  <br>
  <br>
  <div class="container" v-if= "see_cart === false">
    <h3> Mis Pedidos </h3>
    <h5> LogIn para poder ver tus pedidos </h5>
  </div>
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
      pedidos: [],
      cartItems: [],
      see_cart: false,
      price: 0.0,
      user: {},
      session_status: 'Log In',
      session_boolean: false,
      search: '',
      booksquery: []
    }
  },
  created () {
    this.fetch_cache()
    this.load_pedidos()
    this.get_books()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    load_pedidos () {
      const path = 'http://127.0.0.1:5000/transactions/' + this.user.email

      axios.get(path, { auth: { username: this.user.token } })
        .then((res) => {
          this.pedidos = res.data.transactions
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
    get_books () {
      const path = 'http://127.0.0.1:5000/books'
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
