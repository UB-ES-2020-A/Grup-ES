<template>
  <div id="app">
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-md-4">
      <div class="form-control  bg-light" style="margin-top: 150px">
      <div class="form-label-group">
        <b-container style="padding: 20px">
        <h4><b>Cambia su contraseña</b></h4>
        <br>
        <p>Introduzca su nueva contraseña. Después, vuelve a confirmarla</p>
        <input type="password" id="pwd1" class="form-control"
        placeholder="Contraseña" autofocus v-model="pwd1" style="margin-top: 15px">
        <input type="password" id="pwd2" class="form-control"
        placeholder="Confirmar contraseña" autofocus v-model="pwd2" style="margin-top: 15px">
        <b-button block variant="danger" style="margin-top: 20px" @click="goLogin()">Cambiar Contraseña</b-button>
        </b-container>
      </div>
      </div>
      </div>
      </div>
    </b-container>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data: () => ({
  }),
  methods: {
    goLogin () {
      const path = 'https://grup-es.herokuapp.com/'
      axios.get(path)
        .then((res) => {
          this.$router.push({path: '/userlogin'})
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
