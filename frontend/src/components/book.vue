<template>
<div id="app">
<div>
 <b-navbar toggleable="lg" type="dark" variant="info">
  <b-navbar-brand href="#">NavBar</b-navbar-brand>
  <b-nav-form>
     <b-form-input size="md" class="mr-sm-2" placeholder="Search"></b-form-input>
     <b-button size="md" class="my-2 my-sm-0" type="submit">Search</b-button>
  </b-nav-form>
  <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
  <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
    <li class="nav-item"><a href="XXX" class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></a></li>
    <li class="nav-item"><a href="XXX" class="nav-link"><b-icon title="Strikethrough" icon="basket" font-scale="2.5"></b-icon>
</a></li>
    <li class="nav-item"><a href="XXX" class="nav-link"><b-button variant="danger">Log In</b-button>
</a></li>
   </ul>
  </b-navbar-nav>
 </b-navbar>
</div>
 <br>
 <br>
 <b-container>
    <b-row>
      <b-col cols="4">
        <br>
        <img :src="'https://placehold.it/280x436/'" alt="">
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
        <p>
      </b-col>
      <b-col class = "justify-content-center">
      <b-container fluid class = "border bg-light" style="padding:15px">
        <h5> Comprar el llibre </h5>
        <b>{{ this.single_book.precio }} $<b>
        <br>
        <br>
        <b-button style="width:100%" variant="danger">Afegir a la cistella</b-button><br><br>
        <b-button style="width:100%" variant="dark">Comprar ara</b-button><br><br>
        <b-button style="width:100%" variant="dark"> Afegir a la llista de desitjos</b-button>
        </b-container>
      </b-col>
    </b-row>
</b-container>
 <footer style="height:auto; background-color:black;">
   <h5 style="color:white; padding:20px; margin:0; text-align:center;">Contact, bla, bla</h5>
 </footer>
 </div>
 </template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      single_book: {}
    }
  },
  created () {
    this.load_book()
  },
  methods: {
    load_book () {
      const path = 'http://127.0.0.1:5000/book/' + this.$route.query.bk
      axios.get(path)
        .then((res) => {
          this.single_book = res.data
        })
        .catch((error) => {
          console.error(error)
        })
    }

  }
}
</script>
