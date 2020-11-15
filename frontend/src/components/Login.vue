<template>
  <div id="app">
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand >NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-md-4">
      <div class="form-control  bg-light" style="margin-top: 150px">
      <div class="form-label-group">
              <b-button variant="link" style="margin-left: 100px" @click="goRegister()">¿Quieres crear una cuenta?</b-button>
              <br>
              <br>
              <h5>Iniciar Sesión</h5>
              <input type="email" id="inputEmail" class="form-control"
              placeholder="Correo electrónico" required autofocus v-model="email" style="margin-top: 15px">
              <input type="password" id="inputPassword" class="form-control"
              placeholder="Password" required v-model="password" style="margin-top: 20px">
              <b-form-text style="margin-top: 15px; margin-left: 5px">
                Al continuar confirmas que aceptas las <a>Condiciones de uso</a> y las <a>Políticas de privacidad</a>
              </b-form-text>
              <b-button block variant="danger" style="margin-top: 20px" @click="checkLogin()">Log In</b-button>
              <b-button block variant="link" style="margin-top: 10px" @click="changePassword()">¿Olvidaste contraseña?</b-button>
              <hr>
              <b-button block variant="primary" v-google-signin-button="clientId" class="google-signin-button"> Continue with Google</b-button>
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
    clientId: '374016962135-l70k72dvqf1ugd3pirf58ti292v8gk1a.apps.googleusercontent.com',
    username: '',
    email: '',
    password: '',
    role: '',
    token: '',
    userObject: {username: '', email: '', role: '', token: ''}
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
        email: this.email,
        password: this.password
      }
      const path = 'http://127.0.0.1:5000/login'
      const path2 = 'http://127.0.0.1:5000/user/' + this.email
      axios.all([
        axios.post(path, parameters),
        axios.get(path2)
      ])
        .then(axios.spread((datapost, dataget) => {
          this.token = datapost.data.token
          this.username = dataget.data.user.username
          this.email = dataget.data.user.email
          this.role = dataget.data.user.role
          this.createUserObject(this.username, this.email, this.role, this.token)
          this.$router.push({path: '/'})
          this.initForm()
        }))
    },
    createUserObject (username, email, role, token) {
      this.userObject.username = username
      this.userObject.email = email
      this.userObject.role = role
      this.userObject.token = token
      localStorage.setItem('user_session', JSON.stringify(this.userObject))
      console.log(this.userObject.username, this.userObject.email, this.userObject.role, this.userObject.token)
    },
    goRegister () {
      this.$router.push({path: '/userregister'})
    },
    initForm () {
      this.email = ''
      this.password = ''
    },
    changePassword () {
      const path = 'http://127.0.0.1:5000/'
      axios.get(path)
        .then((res) => {
          this.$router.push({path: '/change'})
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
