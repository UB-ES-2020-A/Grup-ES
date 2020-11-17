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
        <b-container style="padding: 20px" v-if=" send === false">
        <h4><b>¿Olvidaste tu contraseña?</b></h4>
        <br>
        <p>Introduce la dirección de correo electrónico asociada a tu cuenta. Te enviaremos un enlace para que restablezcas tu contraseña.</p>
        <input type="email" id="inputEmail" class="form-control"
        placeholder="Correo electrónico" autofocus v-model="email" style="margin-top: 15px">
        <b-button block variant="danger" style="margin-top: 20px" @click="sendEmail()">Enviar</b-button>
        <b-button variant="link" @click="goLogin()">Cancelar</b-button>
        </b-container>
        <b-container style="padding: 20px" v-if= "send === true">
        <h4><b>Comprueba tu correo electrónico</b></h4>
        <br>
        <p>Te hemos enviado un enlace para que restablezcas tu contraseña.</p>
        <b-button block variant="danger" style="margin-top: 20px" @click="goLogin()">Volver a iniciar sesión</b-button>
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
    send: false,
    email: '',
    password: '',
    user_id: ''
  }),
  methods: {
    sendEmail () {
      const path = 'https://grup-es.herokuapp.com/recovery'
      const parameters = {
        email: this.email
      }
      axios.post(path, parameters)
        .then((res) => {
          this.send = true
          console.log('email sended')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    goLogin () {
      this.$router.push({path: '/userlogin'})
    }
  }
}
</script>
