<template>
<div id="app">
 <div>
  <b-navbar toggleable="lg" type="dark" variant="info">
   <b-navbar-brand href="#">NavBar</b-navbar-brand>
   <b-navbar-nav class="ml-auto"> <!-- Right aligned -->
   <ul id="menu-main-nav" class="navbar-nav nav-fill w-100">
     <li id="menu-item-40" class="nav-item menu-item menu-item-type-post_type menu-item-object-page menu-item-40"><a href="XXX" class="nav-link"><b-icon icon="bookmark-heart" font-scale="2.5"></a></li>
     <li id="menu-item-42" class="nav-item menu-item menu-item-type-post_type menu-item-object-page menu-item-home current-menu-item page_item page-item-6 current_page_item menu-item-42"><a href="XXX" class="nav-link"><b-icon icon="basket" font-scale="2.5"></b-icon>
</a></li>
     <li id="menu-item-963" class="nav-item menu-item menu-item-type-post_type menu-item-object-page menu-item-963"><a href="XXX" class="nav-link"><b-button variant="danger">Log In</b-button>
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
        <h2> TÍTOL LLIBRE </h2>
        <p> <h4> de Autor X </h4> <p>
        <hr/>
        <h5> Sinopsis </h5>
        <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec magna risus, accumsan in finibus nec, varius a mi. Curabitur dapibus suscipit sem pretium elementum. In eget bibendum velit, non mollis dui. Praesent eget lacus vitae turpis consequat finibus in ut ante. In at egestas nunc. Proin ac semper ex. Pellentesque non tincidunt orci. Etiam tristique convallis est non finibus. Aenean ullamcorper hendrerit arcu, at hendrerit ante consequat a. Etiam ullamcorper dapibus erat in laoreet. Suspendisse lorem lacus, facilisis sed lectus ut, ultrices posuere sapien. Vestibulum viverra ac elit nec elementum. Pellentesque ut feugiat ante. Duis ornare purus non tellus vestibulum lobortis. Phasellus efficitur, turpis sit amet laoreet efficitur, metus felis hendrerit leo, sed ultricies odio ex malesuada felis.

        Nam iaculis id magna vitae finibus. Donec at elementum diam, ac fringilla urna. Etiam quis ex euismod, viverra nunc quis, imperdiet nunc. Maecenas in nibh mattis, finibus nisi ac, rhoncus orci. Nulla maximus id nisi et aliquet. Nunc nibh ante, semper vel finibus sed, tempus vel massa. Vestibulum convallis pretium posuere. Cras consectetur vehicula felis, ut dictum justo. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Curabitur accumsan tincidunt tellus. Vivamus arcu eros, congue eu ornare nec, ullamcorper vel odio.
        <p>
      </b-col>
      <b-col class = "justify-content-center">
      <b-container fluid class = "border bg-light" style="padding:15px">
        <h5> Comprar el llibre </h5>
        <b>Preu 7.59$<b>
        <br>
        <br>
        <b-button style="width:100%" variant="danger">Afegir a la cistella</b-button><br><br>
        <b-button style="width:100%" variant="dark">Comprar ara</b-button><br><br>
        <b-button style="width:100%" variant="dark">Afegir a la llista de desitjos</b-button>
        </b-container>
      </b-col>
    </b-row>
 <b-container>
 </div>
 </template>
