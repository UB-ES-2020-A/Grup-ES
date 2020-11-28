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
          invalid-feedback="Camp a omplenar"
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
          v-model="emailPwdpwd"
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
      const parameters = {
        username: this.username,
        password: this.usernamepwd
      }
      const auth = {'auth': {
        username: this.$props.user.token}
      }
      axios.put(path, parameters, auth)
        .then((res) => {
          alert('Username Modified correctly')
          this.$bvModal.hide('settings')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    changePassword () {
      const path = this.$API_URL + 'user/' + this.$props.user.email
      const parameters = {
        new_password: this.newpassword,
        password: this.password
      }
      axios.put(path, parameters, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          alert('Password Modified correctly')
          this.$bvModal.hide('settings')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    changeEmail () {
      const path = this.$API_URL + 'user/' + this.$props.user.email
      const parameters = {
        email: this.newEmail,
        password: this.password
      }
      axios.put(path, parameters, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          alert('Email Modified correctly')
          this.$bvModal.hide('settings')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    checkUsernameChange () {
      if (this.username.length > 0) {
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
      if (this.currentpassword.length > 0) {
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
    },
    checkChangeEmail () {
      if (this.newEmail.length > 0) {
        this.newEmailState = true
      } else {
        this.currentEmailState = false
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
    changeLocalStorage (username, email) {
      var user = JSON.parse(localStorage.getItem('user_session'))
      if (username) {
        user.username = username
      }
      if (email) {
        user.email = email
      }
      localStorage.setItem('user_session', JSON.stringify(user))
    },
    deactivateAccount () {
      const path = this.$API_URL + 'user/' + this.email
      axios.delete(path, {
        auth: {username: this.$props.user.token}
      })
        .then((res) => {
          alert('Email Modified correctly')
          this.$bvModal.hide('settings')
          localStorage.removeItem('user_sesion')
          this.$router.push({ path: '/' })
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
