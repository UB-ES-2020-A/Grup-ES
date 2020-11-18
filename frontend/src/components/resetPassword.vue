<template>
  <div id="app">
  <div>
    <navbar @changeShowState="show = !show"/>
    <b-container v-if= "show === true">
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
        <b-button block variant="danger" style="margin-top: 20px" @click="resetPassword()">Cambiar Contraseña</b-button>
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
import navbar from './subcomponents/navbar'

export default {
  components: {
    navbar
  },
  data: () => ({
    show: true,

    key: '',
    user: {},
    email: '',
    password: ''
  }),
  created () {
    this.key = this.$route.query.key
    this.load_user()
  },
  methods: {
    resetPassword () {
      const path = 'https://grup-es.herokuapp.com/recovery/' + this.key
      const parameters = {
        email: this.user.email,
        new_password: this.pwd1
      }
      axios.put(path, parameters)
        .then((res) => {
          console.log('PASSWORD UPDATED')
          alert('Password updated correctly')
          this.goLogin()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_user () {
      const path = 'https://grup-es.herokuapp.com/recovery/' + this.key
      axios.get(path)
        .then((res) => {
          this.user = res.data.user
          console.log(this.user)
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
