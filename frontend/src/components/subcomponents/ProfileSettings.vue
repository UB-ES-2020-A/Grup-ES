<template>
  <div>
    <b-modal
    id="settings"
    title="Configuració del perfil"
    size="xl"
    hide-footer="true"
    >
    <b-tabs content-class="mt-3">
      <b-tab title="Usuari" active>
       <form ref="form">
       <b-row>
       <b-col>
        <b-form-group
          label="Username"
          label-for="username-input"
          invalid-feedback="Camp a omplenar"
        >
        <b-form-input
          id="username-input"
          v-model="username"
          type="text"
          :state = usernameState
        ></b-form-input>
      </b-form-group>
      <b-button size="md" @click = "checkUsernameChange" variant="danger">Canviar nom d'usuari</b-button>
      </b-col>
      </b-row>
      </form>
      </b-tab>
      <b-tab title="Credencials">
      <form ref="form">
      <b-row>
      <b-col>
       <b-form-group
         label="Introdueix l'actual contrasenya"
         label-for="pwdnow-input"
         invalid-feedback="Camp necessari"
       >
       <b-form-input
         id="pwdnow-input"
         v-model="currentpassword"
         type="password"
         :state = passwordState
       ></b-form-input>
     </b-form-group>
     <b-form-group
       label="Introdueix la nova contrasenya"
       label-for="pwdnew1-input"
       invalid-feedback="Les contrasenyes no coincideixen"
     >
     <b-form-input
       id="pwdnew1-input"
       v-model="newpassword"
       type="password"
       :state = passwordnewState
     ></b-form-input>
   </b-form-group>
   <b-form-group
     label="Repeteix la nova contrasenya"
     label-for="pwdnew2-input"
     invalid-feedback="Les contrasenyes no coincideixen"
   >
   <b-form-input
     id="pwdnew2-input"
     v-model="newpassword2"
     type="password"
     :state = passwordnew2State
   ></b-form-input>
   </b-form-group>
     <b-button size="md" @click = "checkChangePassword" variant="danger">Canviar contrasenya</b-button>
     </b-col>
     </b-row>
     </form>
      </b-tab>
      <b-tab title="Configuració avançada">
      <form ref="form">
      <b-row>
      <b-col>
       <b-form-group
         label="Introdueix el teu correu electrònic"
         label-for="mail-input"
       >
       <b-form-input
         id="mail-input"
         v-model="email"
         type="email"
         :state = emailState
       ></b-form-input>
     </b-form-group>
     <b-form-group
       label="Contrasenya"
       label-for="pwd-input"
     >
     <b-form-input
       id="pwd-input"
       model="passdelete"
       type="password"
       :state = passdeleteState
     ></b-form-input>
   </b-form-group>
   <b-form-group
     label="Repeteix la contrasenya"
     label-for="pwd2-input"
   >
   <b-form-input
     id="pwd2-input"
     model="confirmpass"
     type="password"
     :state = confirmpassState
   ></b-form-input>
   </b-form-group>
     <b-button size="md" variant="danger">Desactivar compte</b-button>
     </b-col>
     </b-row>
     </form>
      </b-tab>
    </b-tabs>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  props: {
    user: Object
  },
  data () {
    return {
      username: '',
      email: '',
      password: '',
      newpassword: '',
      newpassword2: '',
      pass: '',
      confirmpass: '',
      usernameState: null,
      passwordState: null,
      passwordnewState: null,
      passwordnew2State: null,
      emailState: null,
      passdeleteState: null,
      confirmpassState: null
    }
  },
  methods: {
    changeUsername () {
      const path = 'https://grup-es.herokuapp.com/user/' + this.user.email
      const parameters = {
        username: this.username
      }
      axios.put(path, parameters)
        .then((res) => {
          alert('Username Modified correctly')
          this.clearModal()
        })
        .catch((error) => {
          console.error(error)
          this.clearModal()
        })
    },
    changePassword () {
      const path = 'https://grup-es.herokuapp.com/user/' + this.user.email
      const parameters = {
        newpassword: this.newpassword,
        password: this.password
      }
      axios.put(path, parameters)
        .then((res) => {
          alert('Password Modified correctly')
          this.clearModal()
        })
        .catch((error) => {
          console.error(error)
          this.clearModal()
        })
    },
    checkUsernameChange () {
      if (this.username.length > 0) {
        this.usernameState = true
        this.changeUsername()
      } else {
        this.usernameState = false
      }
    },
    checkChangePassword () {
      if (this.password.length > 0) {
        this.passwordState = true
      } else {
        this.passwordState = false
      }
      if (this.newpassword.length > 0 && this.newpassword2.length > 0 &&
      this.newpassword === this.newpassword2) {
        this.newpassword2State = true
        this.newpasswordState = true
      } else {
        this.newpassword2State = false
        this.newpasswordState = false
      }
      if (this.passwordState && this.newpasswordState && this.newpassword2State) {
        this.changePassword()
      }
    }
  }
}
</script>
