<template>
<div id="app" v-if="user.role === adminRole">
<navbar @changeShowState="show = !show"/>
<br>
<div class="body" v-if="show === true">
<b-container>
  <b-row>
    <b-col sm="6" md="4" lg="4" xl="4">
    <h4> Llibres en stock : {{ booksquery.books.length }} </h4>
    </b-col>
    <b-col sm="3" md="2" lg="2" xl="2" align-v="left">
      <b-button v-b-modal.addboks variant="success">Afegir llibre</b-button>
    </b-col>
  </b-row>
</b-container>
<addbooks/>
<br>
<b-container>
<b-row align-v="center">
    <b-col sm="6" xl="8">
    <b-form-input v-model="search" placeholder="Filter by title"></b-form-input>
    </b-col>
</b-row>
</b-container>
<br>
<br>
<modifybooks :isbnNum = "bookIsbn"/>
<deletebooks :isbnNum = "bookIsbn"/>
<b-container>
 <b-card-group deck v-for="(book) in filteredList" :key="book.isbn">
  <b-card bg-variant="light" text-variant="dark">
  <b-card-title> {{ book.titulo }} - {{ book.isbn }}</b-card-title>
  <b-card-sub-title class="mb-2">{{ book.autor }}</b-card-sub-title>
  <b-card-text>Stock: {{ book.stock }}</b-card-text>
  <b-card-text>PVP: {{ book.precio }} $</b-card-text>
  <b-card-text>Current Status: {{ bookStatus(book) }} </b-card-text>
  <b-button :disabled = "book.vendible == false" v-b-modal.modifybooks @click="getisbn(book)" variant="primary">Modificar llibre</b-button>
  <b-button :disabled = "book.vendible == false" v-b-modal.deletebooks @click="getisbn(book)" variant="danger">Eliminar llibre</b-button>
  <b-button v-if = "book.vendible == false" variant="success" @click="reactivateBook(book)">Reactivar llibre</b-button>
</b-card>
</b-card-group>
</b-container>
<!-- footer -->
<br>
<br>
</div>
<foot/>
</div>
</template>

<script>
import axios from 'axios'
import navbar from './subcomponents/navbar'
import addbooks from './subcomponents/AddBooks'
import modifybooks from './subcomponents/ModifyBooks'
import deletebooks from './subcomponents/DeleteBooks'
import foot from './subcomponents/foot'

export default {
  components: {
    navbar,
    addbooks,
    foot,
    modifybooks,
    deletebooks
  },
  data () {
    return {
      showadd: false,
      booksquery: [],
      search: '',
      show: true,
      bookIsbn: 0,
      userRole: 'User',
      user: {}
    }
  },
  created () {
    this.fetch_cache()
    this.redirect()
    this.get_books()
    this.fetch_session()
  },
  methods: {
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
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
    fetch_session () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_boolean = true
      }
    },
    getisbn (book) {
      this.bookIsbn = book.isbn
    },
    bookStatus (book) {
      if (book.vendible) {
        return "Disponible a l'stock"
      }
      return "No disponible a l'stock"
    },
    reactivateBook (book) {
      const path = this.$API_URL + 'book/' + book.isbn
      const parameters = {
        vendible: true
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          alert('Book Reactivated correctly')
          location.reload()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    redirect () {
      if (this.user.role === this.userRole) {
        window.location.replace('/notfound')
      }
    }
  },
  computed: {
    filteredList () {
      if (this.booksquery.length !== 0 && this.search !== '') {
        return this.booksquery.books.filter(book => book.titulo.toLowerCase().includes(this.search.toLowerCase()))
      } else {
        return this.booksquery.books
      }
    }
  }
}
</script>
