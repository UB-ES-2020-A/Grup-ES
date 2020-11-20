<template>
<div id="app">
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
  <b-button v-b-modal.modifybooks @click="getisbn(book)" variant="primary">Modificar llibre</b-button>
  <b-button v-b-modal.deletebooks @click="getisbn(book)" variant="danger">Eliminar llibre</b-button>
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
      bookIsbn: 0
    }
  },
  created () {
    this.get_books()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    getURL (book) {
      return book.url_imagen
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
    getisbn (book) {
      this.bookIsbn = book.isbn
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
