<template>
<div id="app">
<navbar @changeShowState="show = !show"/>
<!--body-->
<div class="body">
<div v-if= "show === true">
  <b-container fluid="sm" style="margin-left:100px; margin-right:50px">
  <b-container fluid style="height: 100px; background: #808080;" >
    <b-row align-h="end">
      <b-col cols="3">
        <b-input-group class="mb-2" style="margin-top:25px">
        <b-input-group-prepend is-text>
          <b-icon icon="search"></b-icon>
        </b-input-group-prepend>
        <b-form-input type="search" placeholder="Search terms"></b-form-input>
      </b-input-group>
      </b-col>
    </b-row>
    </b-container>
    <!--select biblio-->
    <b-row>
      <b-col cols="2">
      <b-form-select
        v-model="selected"
        :options="options"
        class="mb-3"
        value-field="value"
        text-field="text"
        disabled-field="notEnabled"
        style="margin-top: 20px"
      ></b-form-select>
      </b-col>
    </b-row>
    <hr>
    <b-row align-h="end">
      <b-col cols="3">
      <b-form-select
        v-model="sFilter"
        :options="filters"
        class="mb-3"
        value-field="value"
        text-field="filter"
        disabled-field="notEnabled"
      ></b-form-select>
      </b-col>
    </b-row>

    <b-row>
      <div class="form-control bg-light">
       <b-row>
       <div class="col-2"  style="margin-left:30px; margin-top:50px" v-for="(book) in list" v-bind:key="book.isbn">
       <b-col align-self="center">
       <img :src="getURL(book)" style="height:409px; width:240px;" alt=""  @click = "gotobook(book)">
       <b-row>
       <b-col align-self="center" style="margin-top: 10px" cols="10">
       <h5 @click = "gotobook(book)">  {{ book.titulo }} </h5>
       </b-col>
       <b-col align-self="center" style="margin-top: 10px" cols="2">
       <b-dropdown variant="link" no-caret>
        <template #button-content>
          <b-icon icon="three-dots"></b-icon>
        </template>
        <b-dropdown-item @click="markFinished(book)">Marcar como Leido</b-dropdown-item>
        <b-dropdown-item @click="markPending(book)">Marcar como Pendientes</b-dropdown-item>
        <b-dropdown-item @click="markReading(book)">Leyendo Actualmente</b-dropdown-item>
        <b-dropdown-item @click="moveArchive(book)">Archivar</b-dropdown-item>
       <b-dropdown-item-button>
       </b-col>
       </b-row>
       <b-col>
       <h7>{{ book.autor }}</h7>
       </b-col>
       </b-col>
       </div>
       </b-row>
       </div>
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
      list: [],
      library: [],
      bought: [],
      user: {},
      book: {},
      selected: 'A',
      sFilter: 'A',
      options: [
        { value: 'A', text: 'Mis Libros' },
        { value: 'B', text: 'Sin Leer' }
      ],
      filters: [
        { value: 'A', filter: 'Fecha de inclusión: Más reciente' },
        { value: 'B', filter: 'Fecha de inclusión: Más antiguos' },
        { value: 'C', filter: 'Titulo: de A a Z' },
        { value: 'D', filter: 'Titulo: de Z a A' },
        { value: 'E', filter: 'Autor: de A a Z' },
        { value: 'F', filter: 'Autor: de Z a A' }
      ]
    }
  },
  created () {
    this.fetch_cache()
    this.load_library()
    this.list = this.bought
  },
  methods: {
    gotobook (book) {
      this.$router.push({ path: '/book', query: {bk: book.isbn} })
    },
    load_library () {
      const path = this.$API_URL + 'userLibrary/' + this.user.email
      axios.get(path, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.library = res.data.library
          console.log(this.library)
          this.manage_library()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (book) {
      return book.url_imagen
    },
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        console.log(this.user.username)
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    manage_library () {
      var i
      for (i = 0; i < this.library.length; i++) {
        if (this.library[i].library_type === 'Bought') {
          this.bought.push(this.library[i].book)
        }
      }
      console.log(this.bought)
    },
    markFinished (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Finished'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          alert('Book marked as finished')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    markPending (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Pending'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          alert('Book marked as pending')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    markReading (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Reading'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          alert('Book marked as reading')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    moveArchive (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/visibility/' + book.isbn
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.delete(path, auth)
        .then((res) => {
          alert('Book moved to archive')
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
