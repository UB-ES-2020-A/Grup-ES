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
          label="Nou Username"
          label-for="username-input"
          invalid-feedback="Camp a omplenar (Cal que tingui més de 4 caràcters)"
        >
        <b-form-input
          id="username-input"
          v-model="username"
          type="text"
          :state = usernameState
        ></b-form-input>
        <b-form-group
          label="Password"
          label-for="usernamepwd-input"
          invalid-feedback="Camp a omplenar"
        >
        <b-form-input
          id="usernamepwd-input"
          v-model="usernamepwd"
          type="password"
          :state = usernamepwdState
        ></b-form-input>
      </b-form-group>
      <b-button size="md" @click = "checkUsernameChange()" variant="danger">Canviar nom d'usuari</b-button>
      </b-col>
      </b-row>
      </form>
      </b-tab>
      <b-tab title="Correu electrònic">
       <form ref="form">
       <b-row>
       <b-col>
        <b-form-group
          label="Nou correu"
          label-for="newemail-input"
          invalid-feedback="Format incorrecte"
        >
        <b-form-input
          id="newemail-input"
          v-model="newEmail"
          type="email"
          :state = newEmailState
        ></b-form-input>
        <b-form-group
          label="Password"
          label-for="emailpwd-input"
          invalid-feedback="Camp a omplenar"
        >
        <b-form-input
          id="emailpwd-input"
          v-model="emailPwd"
          type="password"
          :state = emailPwdState
        ></b-form-input>
      </b-form-group>
      <b-button size="md" @click = "checkChangeEmail()" variant="danger">Canviar correu electrònic</b-button>
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
       label="Introdueix la nova contrasenya: Cal que tingui un nombre, un caràcter, una majuscula i una minuscula"
       label-for="pwdnew1-input"
       invalid-feedback="La contrasenya no és correcta"
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
     invalid-feedback="La contrasenya no és correcta"
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
     <b-button size="md" @click="checkDeactivateAccount()" variant="danger">Desactivar compte</b-button>
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
      usernamepwd: '',
      newEmail: '',
      emailPwd: '',
      email: '',
      currentpassword: '',
      newpassword: '',
      newpassword2: '',
      usernameState: null,
      usernamepwdState: null,
      passwordState: null,
      passwordnewState: null,
      passwordnew2State: null,
      emailState: null,
      newEmailState: null,
      emailPwdState: null
    }
  },
  methods: {
    changeUsername () {
      const path = this.$API_URL + 'user/' + this.$props.user.email
      const auth = {
        auth: {username: this.$props.user.token}
      }
      const parameters = {
        username: this.username,
        password: this.usernamepwd
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          this.$refs.c.showToast(['Info', 'Nombre de usuario actualizado'])
          this.changeLocalStorage(res.data.user.username, null, res.data.token)
          this.$bvModal.hide('settings')
          location.reload()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    changePassword () {
      const path = this.$API_URL + 'user/' + this.$props.user.email
      const parameters = {
        new_password: this.newpassword,
        password: this.currentpassword
      }
      axios.put(path, parameters, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          this.$refs.c.showToast(['Info', 'Contraseña actualizada'])
          this.$bvModal.hide('settings')
          location.reload()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    changeEmail () {
      const path = this.$API_URL + 'user/' + this.$props.user.email
      const parameters = {
        email: this.newEmail,
        password: this.emailPwd
      }
      axios.put(path, parameters, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          this.$refs.c.showToast(['Info', 'Correo electrónico actualizado'])
          this.changeLocalStorage(null, res.data.user.email, res.data.token)
          this.$bvModal.hide('settings')
          location.reload()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    checkUsernameChange () {
      if (this.username.length > 4) {
        this.usernameState = true
      } else {
        this.usernameState = false
      }
      if (this.usernamepwd.length > 0) {
        this.usernamepwdState = true
      } else {
        this.usernamepwdState = false
      }
      if (this.usernameState && this.usernamepwdState) {
        this.changeUsername()
      }
    },
    checkChangePassword () {
      var pw = /(?=.*\d)(?=.*[a-z])(?=.*[A-Z])\w{6,}$/
      if (pw.test(this.currentpassword)) {
        this.passwordState = true
      } else {
        this.passwordState = false
      }
      if (pw.test(this.newpassword) && pw.test(this.newpassword2) &&
      this.newpassword === this.newpassword2) {
        this.passwordnewState = true
        this.passwordnew2State = true
      } else {
        this.passwordnewState = false
        this.passwordnew2State = false
      }
      if (this.passwordState && this.passwordnew2State && this.passwordnewState) {
        this.changePassword()
      }
    },
    checkChangeEmail () {
      var re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      if (re.test(this.newEmail)) {
        this.newEmailState = true
      } else {
        this.newEmailState = false
      }
      if (this.emailPwd.length > 0) {
        this.emailPwdState = true
      } else {
        this.emailPwdState = false
      }
      if (this.emailPwdState && this.newEmailState) {
        this.changeEmail()
      }
    },
    changeLocalStorage (username, email, token) {
      var user = JSON.parse(localStorage.getItem('user_session'))
      if (username) {
        user.username = username
      }
      if (email) {
        user.email = email
      }
      if (token) {
        user.token = token
      }
      localStorage.setItem('user_session', JSON.stringify(user))
    },
    deactivateAccount () {
      const path = this.$API_URL + 'user/' + this.email
      axios.delete(path, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          this.$refs.c.showToast(['Info', 'Su cuenta ha sido desactivada'])
          this.$bvModal.hide('settings')
          localStorage.removeItem('user_sesion')
          setTimeout(() => this.$router.push({path: '/'}), 3000)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    checkDeactivateAccount () {
      if (this.email.length > 0) {
        this.emailState = true
      } else {
        this.emailState = false
      }
      if (this.emailState) {
        this.deactivateAccount()
      }
    }
  }
}
</script>
