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
       <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book.isbn)">
       <h6  @click = "gotobook(book.isbn)">{{ book.titulo }}</h6>
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
        <img :src="getURL(book)" style="height:209px; width:140px;" alt=""  @click = "gotobook(book.isbn)">
        <h6 @click = "gotobook(book.isbn)">  {{ book.titulo }}</h6>
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
        <b-button style="width:100%" variant="danger" @click="finalizePurchase()">Finalitzar compra</b-button><br><br>
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
      user: {},
      session_status: 'Log In',
      session_boolean: false,
      search: '',
      booksquery: [],
      isbn: '',
      isbnState: null,
      title: '',
      autor: '',
      editorial: '',
      advancedsearch: []
    }
  },
  created () {
    this.load_new_releases()
    this.fetch_cache()
    this.get_books()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
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
    },
    goLibrary () {
      this.$router.push({path: '/biblioteca'})
    },
    goPedidos () {
      this.$router.push({path: '/mispedidos'})
    },
    addToLibrary (parameters) {
      const path = 'https://grup-es.herokuapp.com/library'
      axios.post(path, parameters, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          console.log('BOOK ADDED TO LIBRARY')
          this.cartItems.splice(0, this.cartItems.length)
          alert('Book ADDED correctly to LIBRARY')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    finalizePurchase () {
      this.$router.push({path: '/paymethod'})
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
