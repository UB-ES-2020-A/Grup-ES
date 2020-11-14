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
     <div class="col-2"  style="margin-left:30px; margin-top:50px" v-for="(lib) in library" v-bind:key="lib.book.isbn">
       <b-col align-self="center">
       <img :src="getURL(lib)" style="height:409px; width:240px;" alt=""  @click = "gotobook(lib)">
       <b-col align-self="center" style="margin-top: 10px">
       <h4 @click = "gotobook(lib)">  {{ lib.book.titulo }} </h4>
       </b-col>
       <b-col align-self="center">
       <h7>{{ lib.book.autor }}</h7>
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
      library: [],
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
  },
  methods: {
    gotobook (lib) {
      this.$router.push({ path: '/book', query: {bk: lib.book.isbn} })
    },
    load_library () {
      const path = 'https://grup-es.herokuapp.com/library/' + this.user.email
      axios.get(path, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.library = res.data.library
          console.log(this.library)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (lib) {
      return lib.book.url_imagen
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
      const path = 'https://grup-es.herokuapp.com/'
      axios.get(path)
        .then((res) => {
          this.$router.push({path: '/'})
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
