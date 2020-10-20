<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand href="#">NavBar</b-navbar-brand>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
     <li id="menu-item-42" class="nav-item menu-item menu-item-type-post_type menu-item-object-page menu-item-home current-menu-item page_item page-item-6 current_page_item menu-item-42"><a href="XXX" class="nav-link">     <b-icon icon="basket" font-scale="2.5"></b-icon>
</a></li>
     <li id="menu-item-963" class="nav-item menu-item menu-item-type-post_type menu-item-object-page menu-item-963"><a href="XXX" class="nav-link">     <b-button variant="danger">Log In</b-button>
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

<!-- Carousel -->
<style>
.container{
padding : 1px;

}
</style>
<div class="container">
   <h3> Best sellers </h3>
   <b-row>
     <b-col  v-for="i in 6" :key="i">
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
</template>

<script>
export default {
  data () {
    return {

    }
  }
}
</script>
