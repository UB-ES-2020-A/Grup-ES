<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand href="#">NavBar</b-navbar-brand>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
     <b-button variant="danger">Log In</b-button>
   </b-navbar-nav>
  </b-navbar>
 </div>

<!-- container for static pics -->


<b-container>
 <img :src="'https://placehold.it/800x300/?text=' + picturestock" alt="">
</b-container>

<!-- Carousel -->
<div class="container">
   <h3> Best sellers </h3>
   <div class="row">
     <div class="col-lg-4 col-md-6 mb-4" v-for="i in 3" :key="i">
       <br>
       <img :src="'https://placehold.it/200x200/?text=' + i + '-' + i" alt="">
       <h6>Llibre</h6>
       <div v-for="j in 1" :key="j">
          <h5>AUTOR</h5>
       </div>
       <h6>Valoració</h6>
       <h6>PREU</h6>
       <b-button variant="danger">Add to cart</b-button>
     </div>
   </div>
 </div>
  </div>
</template>

<script>
export default {
  data () {
    return {

    }
  }
}
</script>
