<template>
<div id="app">
  <!--navbar-->
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand @click="goStart()"> NavBar</b-navbar-brand>
   <b-nav-form>
      <b-form-input size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
      <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
   </b-nav-form>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
<b-nav-item-dropdown id="my-nav-dropdown" :text="this.user.username" toggle-class="nav-link-custom" right>
<b-dropdown-item @click="goLibrary()">Biblioteca</b-dropdown-item>
<b-dropdown-item @click="goPedidos()">Mis Pedidos</b-dropdown-item>
</b-nav-item-dropdown>
    </ul>
   </b-navbar-nav>
  </b-navbar>
 </div>
<!--body-->
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
    <b-col cols="3">
     <b-nav tabs style="margin-top: 40px">
       <b-nav-item @click="choose_bought()" v-on:click="archived = false">Mis Libros</b-nav-item>
       <b-nav-item @click="choose_archive()">Archivo</b-nav-item>
      </b-nav>
    </b-col>
  </b-row>
  <b-row align-h="between" style="margin-top: 20px">
    <b-col cols="3">
    <b-form-select
      v-model="selected"
      :options="options"
      class="mb-3"
      value-field="value"
      text-field="text"
      disabled-field="notEnabled"
      @change="getItem($event)"
      v-if="archived === false"
    ></b-form-select>
    </b-col>
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
       <b-col align-self="center" style="margin-top: 10px">
       <h4 @click = "gotobook(book)">  {{ book.titulo }} </h4>
       </b-col>
       <b-col align-self="center">
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
      list: [],
      library: [],
      bought: [],
      archive: [],
      pending: [],
      reading: [],
      finished: [],
      user: {},
      book: {},
      archived: false,
      show: 'A',
      selected: 'A',
      sFilter: 'A',
      options: [
        { value: 'A', text: 'Libros' },
        { value: 'B', text: 'Sin Leer' },
        { value: 'C', text: 'Leidos' }
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
      const path = 'https://grup-es.herokuapp.com/library/' + this.user.email
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
    goStart () {
      this.$router.push({path: '/'})
    },
    goLibrary () {
      this.$router.push({path: '/biblioteca'})
    },
    goPedidos () {
      this.$router.push({path: '/mispedidos'})
    },
    manage_library () {
      var i
      for (i = 0; i < this.library.length; i++) {
        if (this.library[i].library_type === 'Bought') {
          this.bought.push(this.library[i].book)
          switch (this.library[i].state) {
            case 'Pending':
              this.pending.push(this.library[i].book)
              break
            case 'Reading':
              this.reading.push(this.library[i].book)
              break
            case 'Finished':
              this.finished.push(this.library[i].book)
              break
          }
        }
      }
      console.log(this.bought)
    },
    choose_bought () {
      this.list = this.bought
    },
    choose_archive () {
      this.list = this.archive
      this.archived = true
    },
    choose_pending () {
      this.list = this.pending
    },
    choose_finished () {
      this.list = this.finished
    },
    getItem (event) {
      console.log(this.selected)
      switch (this.selected) {
        case 'A':
          this.choose_bought()
          break
        case 'B':
          this.choose_pending()
          break
        case 'C':
          this.choose_finished()
          break
      }
    }
  }
}
</script>
