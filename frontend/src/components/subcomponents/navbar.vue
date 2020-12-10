<template>
  <div ref="navbar">
   <b-navbar toggleable="lg" type="dark" variant="info">
    <b-navbar-brand @click="goStart()">
    <img src="../../assets/Bookshelter.png" class="d-inline-block align-top" width="200" height="60">
    </b-navbar-brand>
    <b-nav-form>
       <b-form-input autocomplete="off" v-model="search" @change="onInputDataList()" list="booksearch" id="inputsearch" size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
       <datalist id="booksearch">
         <option v-for="book in filteredList" :key="book.isbn" :value="book.titulo" :id="book.isbn">
           {{ book.autor }}
         </option>
       </datalist>
       <b-button size="md" class="my-2 my-sm-0" @click="onSearch()">Search</b-button>
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
        <li class="nav-item" v-if="session_boolean === true && user.role == userRole" ><a class="nav-link"><b-icon icon="bookmark-heart" @click="goWishlist()" font-scale="2.5"></b-icon></a></li>
        <li class="nav-item" v-if="session_boolean === true && user.role == userRole"><a class="nav-link"><b-icon title="Strikethrough" @click="show_cart(); calculate_total_price()" icon="basket" font-scale="2.5"></b-icon></a></li>
        <li class="nav-item" v-if= "session_boolean === false"><a class="nav-link"><b-button variant="danger" @click="logIn()">{{ session_status }}</b-button></a></li>
        <li class="nav-item" v-if= "session_boolean === true">
          <b-button v-b-toggle.sidebar-right> {{ this.user.username }}</b-button>
        </li>
       </ul>
       <div>
           <b-sidebar id="sidebar-right" text-variant="light" title="BookShelter" bg-variant="dark" right shadow>
             <div class="px-3 py-2">
                <h4> Hola {{ this.user.username }} </h4>
                <nav class="mb-3">
                <b-nav vertical>
                  <b-nav-item active v-if="user.role === userRole" @click="goProfile()">El meu Perfil</b-nav-item>
                  <b-nav-item active v-if="user.role == userRole" @click="goLibrary()">Biblioteca</b-nav-item>
                  <b-nav-item active @click="goPedidos()">Comandes</b-nav-item>
                  <b-nav-item active v-if="user.role === adminRole" @click="goStock()">Stock</b-nav-item>
                  <b-nav-item active v-if="user.role === adminRole" @click="goTransactions()">Transaccions</b-nav-item>
                </b-nav>
                </nav>
             </div>
             <template #footer="{ hide }">
             <div class="d-flex bg-dark text-light align-items-center px-3 py-2">
              <b-button size="sm"  variant="danger" @click="logIn()">{{ session_status }}</b-button>
             </div>
            </template>
          </b-sidebar>
      </div>
    </b-navbar-nav>
   </b-navbar>
   <!-- cart -->
   <b-container v-if= "see_cart === true">
     <br>
     <br>
     <br>
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
             <div>
             <label for="sb-inline">Quantitat</label>
             <b-form-spinbutton id="sb-inline" v-model="item.quantity" @change="save_quantity(item.book, item.quantity)" min="1">
             </b-form-spinbutton>
             </div>
             </b-row>
             <br>
             <br>
             <b-row>
             <h6>Preu: {{ total_amount(item.book, item.quantity) }} $</h6>
             </b-row>
             <br>
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
         <b-icon icon="arrow-left-circle-fill" variant="info" font-scale="3" @click="show_cart()"
         style="position: fixed; left: 100; top: 150;"></b-icon>
       </b-row>
   </b-container>
   <!--toast-->
   <b-toast id="toast" toaster="b-toaster-top-center" variant="primary" solid autoHideDelay="5000">
     <template #toast-title>
       <div class="d-flex flex-grow-1 align-items-baseline">
         <b-img blank blank-color="#ff5555" class="mr-2" width="12" height="12"></b-img>
         <strong class="mr-auto">Notice!</strong>
       </div>
     </template>
     <b-row style="margin-left:5px">
     Se ha enviado un correo de confirmación a su cuenta.
     </b-row>
     <br>
   </b-toast>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      // LogIn status
      user: {},
      session_status: 'Log In',
      session_boolean: false,
      adminRole: 'Admin',
      userRole: 'User',
      // Search
      search: '',
      booksquery: [],

      // Advanced search
      isbn: '',
      isbnState: null,
      title: '',
      autor: '',
      editorial: '',
      advancedsearch: [],

      // Cart
      cartItems: [],
      see_cart: false,
      price: 0.0
    }
  },
  created () {
    this.fetch_cache()
    this.get_books()
  },
  methods: {
    goStart () {
      if (this.see_cart) {
        this.show_cart()
      }
      this.$router.push({path: '/'})
    },
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    showToast (message) {
      // Use a shorter name for this.$createElement
      const h = this.$createElement
      // Increment the toast count
      this.count++
      // Create the message
      const vNodesMsg = h(
        'p',
        { class: ['text-center', 'mb-0'] },
        [message[1]]
      )
      // Create the title
      const vNodesTitle = h(
        'div',
        { class: ['d-flex', 'flex-grow-1', 'align-items-baseline', 'mr-2'] },
        [
          h('strong', { class: 'mb-0' }, message[0])
        ]
      )
      // Pass the VNodes as an array for message and title
      this.$bvToast.toast([vNodesMsg], {
        title: [vNodesTitle],
        toaster: 'b-toaster-top-center',
        solid: true,
        variant: 'info'
      })
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
        this.showToast(['Info', 'Has cerrado sesion correctamente'])
        setTimeout(() => {
          this.$router.push({path: '/'})
          location.reload()
        }, 2000)
      }
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

    // Search
    get_books () {
      const path = this.$API_URL + 'books'
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
          this.search = ''
          this.gotobook(datalist[i].id)
        }
      }
    },
    checkOk () {
      if ((this.isbn.length <= 13 && this.isbn.length > 0) || (this.title.length > 0 || this.autor.length > 0 || this.editorial.length > 0)) {
        this.$nextTick(() => {
          this.$bvModal.hide('modal-1')
        })
        this.isbnState = true
        return true
      }
      return false
    },
    handleOk (bvModalEvt) {
      bvModalEvt.preventDefault()
      if (this.checkOk()) {
        var params = {}
        if (this.isbn !== '') {
          params['isbn'] = this.isbn
        }
        if (this.title !== '') {
          params['titulo'] = this.title
        }
        if (this.autor !== '') {
          params['autor'] = this.autor
        }
        if (this.editorial !== '') {
          params['editorial'] = this.editorial
        }
        this.$router.push({ path: '/search', query: params })
      }
    },
    clearModal () {
      this.isbn = ''
      this.title = ''
      this.autor = ''
      this.editorial = ''
      this.isbnState = null
    },
    getAdvancedSearch (parameters) {
      const path = this.$API_URL + 'search'
      axios.get(path, { params: parameters })
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
    goDelBook () {
      this.$router.push({path: '/delete'})
    },
    goModBook () {
      this.$router.push({path: '/modify'})
    },
    onSearch () {
      if (this.search.length > 0) {
        this.$router.push({ path: '/search', query: {titulo: this.search} })
      }
    },
    goStock () {
      this.$router.push({path: '/shopstock'})
    },
    goWishlist () {
      this.$router.push({path: '/wishlist'})
    },
    goProfile () {
      this.$router.push({path: '/profile'})
    },
    goTransactions () {
      this.$router.push({path: '/stocktransactions'})
    },
    // Cart
    show_cart () {
      this.see_cart = !this.see_cart
      if (this.see_cart) {
        this.fetch_cache()
      }
      this.$emit('changeShowState')
    },
    total_amount (book, quantity) {
      var preu = book.precio * quantity
      return parseFloat(preu.toFixed(2))
    },
    calculate_total_price () {
      var price = 0.0
      var i
      for (i = 0; i < this.cartItems.length; i++) {
        price = price + this.total_amount(this.cartItems[i].book, this.cartItems[i].quantity)
      }
      return parseFloat(price.toFixed(2))
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
      for (i = 0; i < this.cartItems.length; i++) {
        if (book.isbn === this.cartItems[i].book.isbn) {
          this.cartItems[i].quantity = quantity
        }
      }
      localStorage.setItem('cartItems', JSON.stringify(this.cartItems))
      console.log(quantity)
    },
    finalizePurchase () {
      this.$router.push({path: '/paymethod'})
    },
    getURL (book) {
      return book.url_imagen
    }
  },
  computed: {
    filteredList () {
      if (this.booksquery.length !== 0 && this.search !== '') {
        return this.booksquery.books.filter(book => book.titulo.toLowerCase().includes(this.search.toLowerCase()) && book.vendible)
      } else {
        return ''
      }
    }
  }
}
</script>
