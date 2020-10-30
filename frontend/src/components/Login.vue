<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-md-4">
      <div class="form-control" style="margin-top: 150px">
      <div class="form-label-group">
              <b-button variant="link" style="margin-left: 100px">¿Quieres crear una cuenta?</b-button>
              <br>
              <br>
              <h5>Iniciar Sesión</h5>
              <input type="email" id="inputEmail" class="form-control"
              placeholder="Correo electrónico" required autofocus v-model="email" style="margin-top: 15px">
              <input type="password" id="inputPassword" class="form-control"
              placeholder="Password" required v-model="password" style="margin-top: 20px">
              <b-form-text style="margin-top: 15px; margin-left: 5px">
                Al continuar confirmas que aceptas las <a href="#">Condiciones de uso</a> y las <a href="#">Políticas de privacidad</a>
              </b-form-text>
              <b-button block variant="danger" style="margin-top: 20px" @click="checkLogin()">Log In</b-button>
              <b-button block variant="link" style="margin-top: 10px">¿Olvidaste contraseña?</b-button>
              <hr>
              <b-button block variant="primary" v-google-signin-button="clientId" class="google-signin-button"> Continue with Google</b-button>
      </div>
      </div>
      </div>
      </div>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data: () => ({
    clientId: '374016962135-l70k72dvqf1ugd3pirf58ti292v8gk1a.apps.googleusercontent.com',
    username: '',
    email: '',
    password: '',
    role: '',
    token: ''
  }),
  methods: {
    OnGoogleAuthSuccess (idToken) {
      console.log(idToken)
      // Receive the idToken and make your magic with the backend
    },
    OnGoogleAuthFail (error) {
      console.log(error)
    },
    checkLogin () {
      const parameters = {
        username: this.username,
        email: this.email,
        password: this.password
      }
      const path = 'http://127.0.0.1:5000/login'
      axios.post(path, parameters)
        .then((res) => {
          this.getAccount()
          this.token = res.data.token
          console.log('ACCOUNT LOGED')
          alert('User loged')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getAccount () {
      const path = 'http://127.0.0.1:5000/user/' + this.email
      axios.get(path)
        .then((res) => {
          this.role = res.data.role
          console.log('ACCOUNT GETTED')
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
