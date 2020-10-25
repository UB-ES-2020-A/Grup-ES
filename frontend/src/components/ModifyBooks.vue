<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-sm">
      <div class="form-control bg-light" style="margin-top: 100px">
      <div class="form-label-group">
              <div class="row justify-content-center"><h4>Modificar libro</h4></div>
              <b-row>
              <b-col cols="8">
              <b-container>
              <b-row align-h="between">
                <b-col cols="5">
                  <input id="isbn" class="form-control"
                  placeholder="ISBN" required autofocus v-model="isbn" style="margin-top: 15px">
                </b-col>
                <b-col cols="3">
                  <input id="stock" class="form-control"
                  placeholder="Stock" required autofocus v-model="stock" style="margin-top: 15px">
                </b-col>
                <b-col cols="3">
                  <input id="price" class="form-control"
                  placeholder="Precio" required autofocus v-model="price" style="margin-top: 15px">
                </b-col>
              </b-row>
             <input id="title" class="form-control"
             placeholder="Titulo" required autofocus v-model="title" style="margin-top: 15px">
             <input id="author" class="form-control"
             placeholder="Autor" required autofocus v-model="author" style="margin-top: 15px">
             <b-row align-h="between">
               <b-col cols="8">
                 <input id="publisher" class="form-control"
               placeholder="Editorial" required autofocus v-model="publisher" style="margin-top: 15px">
               </b-col>
               <b-col cols="4">
                 <input id="date" class="form-control"
               placeholder="YYYY-MM-DD" required autofocus v-model="date" style="margin-top: 15px">
               </b-col>
             </b-row>
             <b-form-file accept=".jpg, .png, .jpeg" v-model="file1" :state="Boolean(file1)"
             placeholder="Elige la imagen o dejala aqui..." drop-placeholder="Deja aqui la imagen..." style="margin-top: 15px"></b-form-file>
             <b-form-textarea id="sinopsis" placeholder="Sinopsis" required autofocus v-model="publisher" style="margin-top: 15px"></b-form-textarea>
             </b-container>
             <div class=" row d-flex text-center">
             <b-col align-self="center">
               <b-button size="lg" variant="primary" style="margin-top: 15px; margin-botton: 30px">Modificar</b-button>
             </b-col>
             </div>
             </b-col>
             <b-col>
               <img :src="'https://placehold.it/240x340/'" >
             </b-col>
             </b-row>

      </div>
      </div>
      </div>
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
      file1: null
    }
  },
  methods: {
  }
}
</script>
