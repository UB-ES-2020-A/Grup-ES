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
<!-- container for static pics -->
<br>
<br>
<b-container>
 <img :src="'https://placehold.it/1100x300/?text=' + picturestock" alt="">
</b-container>
<br>

<!-- Carousel -->

<div class="container">
   <h3> Best sellers </h3>
   <b-row>
     <b-col  v-for="i in 6" :key="i" @click = "gotobook()">
       <br>
       <img :src="'https://placehold.it/140x218/?text=' + i + '-' + i" alt="">
       <h6>Llibre</h6>
       <div v-for="j in 1" :key="j">
          <h5>AUTOR</h5>
       </div>
       <h6>Valoració</h6>
       <h6>PREU</h6>
       <b-button variant="danger">Add to cart</b-button>
   </b-col>
   </b-row>
   </div>
   <br>
   <br>
   <div class="container">
      <h3> New releases </h3>
      <b-row>
        <b-col  v-for="i in 6" :key="i" @click = "gotobook()">
          <br>
          <img :src="'https://placehold.it/140x218/?text=' + i + '-' + i" alt="">
          <h6>Llibre</h6>
          <div v-for="j in 1" :key="j">
             <h5>AUTOR</h5>
          </div>
          <h6>Valoració</h6>
          <h6>PREU</h6>
          <b-button variant="danger">Add to cart</b-button>
      </b-col>
      </b-row>
      </div>
      <br>
      <br>
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

    }
  },
  methods: {
    gotobook () {
      const path = 'http://127.0.0.1:5000/'
      axios.get(path)
        .then((res) => {
          this.$router.push({path: '/book'})
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
