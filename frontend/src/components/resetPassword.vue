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
        <b-form-group
        label-for="pwd1"
        valid-feedback="Contraseña valida"
        :invalid-feedback="pwd1Invalid"
        :state="pwd1State"
        style="margin-top: 15px"
        >
          <b-form-input
            id="pwd1"
            placeholder="Contraseña"
            v-model="pwd1"
            :state="pwd1State"
            type="password"
          ></b-form-input>
        </b-form-group>

        <b-form-group
        label-for="pwd2"
        :invalid-feedback="pwd2Invalid"
        :state="pwd2State"
        style="margin-top: 15px"
        >
          <b-form-input
            id="pwd2"
            placeholder="Confirmar contraseña"
            v-model="pwd2"
            :state="pwd2State"
            type="password"
          ></b-form-input>
        </b-form-group>
        <b-button block variant="danger" style="margin-top: 20px" @click="checkPassword()">Cambiar Contraseña</b-button>
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
  computed: {
    pwd1State () {
      var pw = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/
      return pw.test(this.pwd1)
    },
    pwd1Invalid () {
      var pw = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/
      if (!pw.test(this.pwd1)) {
        return 'la contraseña debe contener 6 carácteres, un número, una mayuscula, una minuscula.'
      }
    },
    pwd2State () {
      if (this.pwd1 !== '' && this.pwd2 === this.pwd1) {
        return true
      }
      return false
    },
    pwd2Invalid () {
      if (this.pwd1 === '' || this.pwd2 !== this.pwd1) {
        return 'Las contraseñas deben de coincidir'
      }
    }
  },
  components: {
    navbar
  },
  data: () => ({
    show: true,

    key: '',
    user: {},
    pwd1: '',
    pwd2: ''
  }),
  created () {
    this.key = this.$route.query.key
    this.load_user()
  },
  methods: {
    resetPassword () {
      const path = this.$API_URL + 'recovery/' + this.key
      const parameters = {
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
      const path = this.$API_URL + 'recovery/' + this.key
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
    },
    checkPassword () {
      if (this.pwd1State && this.pwd2State) {
        this.resetPassword()
      } else {
        alert('Algún parametro es incorrecto o no ha sido introducido')
      }
    }
  }
}
</script>
