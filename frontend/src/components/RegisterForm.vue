<template>
  <div id="app">
  <div>
    <navbar ref="c" @changeShowState="show = !show"/>

    <b-container v-if= "show === true">
      <div class="row d-flex justify-content-center">
      <div class="col-md">
      <div class="form-control  bg-light" style="margin-top: 100px">
      <div class="form-label-group">
              <h5>Crear cuenta</h5>
              <b-form-group
              label="Username"
              label-for="inputUsername"
              valid-feedback="El username es valido"
              :invalid-feedback="userInvalid"
              :state="userState"
              style="margin-top: 15px"
              >
                <b-form-input
                  id="inputUsername"
                  v-model="username"
                  :state="userState"
                  type="username"
                ></b-form-input>
              </b-form-group>

              <b-form-group
              label="Correo Electronico"
              label-for="inputEmail"
              valid-feedback="El correo electrónico es valido"
              :invalid-feedback="emailInvalid"
              :state="emailState"
              style="margin-top: 15px"
              >
                <b-form-input
                  id="inputEmail"
                  v-model="email"
                  :state="emailState"
                  type="email"
                ></b-form-input>
              </b-form-group>

              <b-form-group
              label="Contraseña"
              label-for="inputPassword1"
              valid-feedback="Contraseña valida"
              :invalid-feedback="pwd1Invalid"
              :state="pwd1State"
              style="margin-top: 15px"
              >
                <b-form-input
                  id="inputPassword1"
                  v-model="password1"
                  :state="pwd1State"
                  type="password"
                ></b-form-input>
              </b-form-group>

              <b-form-group
              label="Confirmar contraseña"
              label-for="inputPassword2"
              :invalid-feedback="pwd2Invalid"
              :state="pwd2State"
              style="margin-top: 15px"
              >
                <b-form-input
                  id="inputPassword2"
                  v-model="password2"
                  :state="pwd2State"
                  type="password"
                ></b-form-input>
              </b-form-group>

              <b-button variant="danger" style="margin-top: 20px" @click="checkInputs()">Crear usuario</b-button>
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
    userState () {
      return this.username.length >= 4
    },
    userInvalid () {
      if (this.username.length < 4) {
        return 'El usuario debe tener más de 4 carácteres'
      }
    },
    emailState () {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      return re.test(this.email)
    },
    emailInvalid () {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if (!re.test(this.email)) {
        return 'El correo electrónico es invalido'
      }
    },
    pwd1State () {
      var pw = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/
      return pw.test(this.password1)
    },
    pwd1Invalid () {
      var pw = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/
      if (!pw.test(this.password1)) {
        return 'La contraseña debe contener 6 carácteres, un número, una mayuscula, una minuscula.'
      }
    },
    pwd2State () {
      if (this.password1 !== '' && this.password2 === this.password1) {
        return true
      }
      return false
    },
    pwd2Invalid () {
      if (this.password1 === '' || this.password2 !== this.password1) {
        return 'Las contraseñas deben de coincidir'
      }
    }
  },
  components: {
    navbar
  },
  data () {
    return {
      show: true,
      username: '',
      email: '',
      password: '',
      password1: '',
      password2: ''
    }
  },
  methods: {
    createUser () {
      const parameters = {
        username: this.username,
        email: this.email,
        password: this.password1
      }
      const path = this.$API_URL + 'user'
      axios.post(path, parameters)
        .then((res) => {
          this.initForm()
          alert('Account created')
          this.$refs.c.$bvToast.show('toast')
          setTimeout(() => this.$router.push({path: '/userlogin'}), 5000)
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
    },
    checkInputs () {
      if (this.userState && this.emailState && this.pwd1State && this.pwd2State) {
        this.createUser()
      } else {
        alert('Algún parametro es incorrecto o no ha sido introducido')
      }
    }
  }
}
</script>
