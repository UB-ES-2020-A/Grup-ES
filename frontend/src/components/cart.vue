<template>
<div id="app">
<div>
 <b-navbar toggleable="lg" type="dark" variant="info">
  <b-navbar-brand href="#">NavBar</b-navbar-brand>
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
 <h2> CISTELLA X PRODUCTES </h2>
</b-container>
<br>
 <b-container>
    <b-row>
      <b-col cols="8">
        <b-container fluid style="padding:35px">
        <b-row class = "border bg-light" v-for="i in 9" :key="i" style="padding:35px; margin-bottom:10px">
          <b-col>
          <img :src="'https://placehold.it/70x109/?text=' + i + '-' + i" alt="">
          </b-col>
          <b-col>
          <h6>Llibre</h6>
          <div v-for="j in 1" :key="j">
             <h5>AUTOR</h5>
          </div>
          </b-col>
          <b-col>
          <b-row>
          <h6>PREU</h6>
          </b-row>
          <br>
          <b-row>
          <b-form-spinbutton id="sb-inline" style="width:45%"></b-form-spinbutton>
          </b-row>
          </b-col>
          <hr/>
      </b-row>
      </b-container>
      </b-col>
      <b-col>
       <b-container fluid class = "border bg-light" style="padding:15px">
        <p> Tens un codi de descompte? <p>
        <b-nav-form>
           <b-form-input size="sm" class="mr-sm-2" placeholder="Introdueix el teu codi descompte"></b-form-input>
           <b-button size="sm" class="my-2 my-sm-0" type="submit">Validar</b-button>
        </b-nav-form>
      </b-container>
      <b-container fluid class = "border bg-light" style="padding:15px; margin-top:10px">
      <br>
        <h5> Resum </h5>
        <br>
        <h6> Cistella (X) : 100.98$ </h6>
        <hr/>
        <h6> Despeses enviament : Gratuït</h6>
        <hr/>
        <h5> Total : 100.98$ </h5>
        <br>
        <b-button style="width:100%" variant="danger">Finalitzar compra</b-button><br><br>
        </b-container>
      </b-col>
    </b-row>
</b-container>
 <footer style="height:auto; background-color:black;">
   <h5 style="color:white; padding:20px; margin:0; text-align:center;">Contact, bla, bla</h5>
 </footer>
 </div>
 </template>
