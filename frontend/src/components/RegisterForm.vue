<template>
  <div id="app">
  <div>
    <navbar @changeShowState="show = !show"/>

    <b-container v-if= "show === true">
      <div class="row d-flex justify-content-center">
      <div class="col-md">
      <div class="form-control  bg-light" style="margin-top: 100px">
      <div class="form-label-group">
              <h5>Crear cuenta</h5>
              <label style="margin-top: 15px">Username</label>
              <input type="username" id="inputUsername" class="form-control"
              placeholder="Username" required autofocus v-model="username">

              <label style="margin-top: 15px">Correo electronico</label>
              <input type="e-mail" id="inputEmail" class="form-control"
              placeholder="Correo Electronico" required autofocus v-model="email">

              <label style="margin-top: 15px">Contraseña</label>
              <input type="password" id="inputPassword1" class="form-control"
              placeholder="Contraseña" required v-model="password1">

              <label style="margin-top: 15px">Confirmar contraseña</label>
              <input type="password" id="inputPassword2" class="form-control"
              placeholder="Confirmar contraseña" required v-model="password2">

              <b-button variant="danger" style="margin-top: 20px" @click="createUser()">Crear usuario</b-button>
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
import navbar from './subcomponents/navbar'

export default {
  components: {
    navbar
  },
  data () {
    return {
      show: true,

      username: '',
      email: '',
      password: ''
    }
  },
  methods: {
    createUser () {
      const parameters = {
        username: this.username,
        email: this.email,
        password: this.password1
      }
      const path = 'https://grup-es.herokuapp.com/user'
      axios.post(path, parameters)
        .then((res) => {
          this.initForm()
          console.log('ACCOUNT CREATED')
          alert('Account created')
          this.$router.push({path: '/userlogin'})
        })
        .catch((error) => {
          console.error(error)
          this.initForm()
          alert('Username already in use')
        })
    },
    initForm () {
      this.username = ''
      this.email = ''
      this.password1 = ''
      this.password2 = ''
    }
  }
}
</script>
