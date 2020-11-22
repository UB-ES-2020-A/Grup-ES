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
       <form ref="form" @submit.stop.prevent="handleSubmit">
       <b-row>
       <b-col>
        <b-form-group
          label="Username"
          label-for="username-input"
          invalid-feedback="usernameInput"
        >
        <b-form-input
          id="username-input"
          v-model="this.$props.user.username"
          type="text"
        ></b-form-input>
      </b-form-group>
      <b-button size="md" variant="danger">Canviar nom d'usuari</b-button>
      </b-col>
      </b-row>
      </form>
      </b-tab>
      <b-tab title="Credencials">
      <form ref="form" @submit.stop.prevent="handleSubmit">
      <b-row>
      <b-col>
       <b-form-group
         label="Introdueix l'actual contrasenya"
         label-for="pwdnow-input"
         invalid-feedback="pwdInput"
       >
       <b-form-input
         id="pwdnow-input"
         v-model="this.$props.user.username"
         type="password"
       ></b-form-input>
     </b-form-group>
     <b-form-group
       label="Introdueix la nova contrasenya"
       label-for="pwdnew1-input"
       invalid-feedback="pwdInput"
     >
     <b-form-input
       id="pwdnew1-input"
       v-model="this.$props.user.username"
       type="password"
     ></b-form-input>
   </b-form-group>
   <b-form-group
     label="Repeteix la nova contrasenya"
     label-for="pwdnew2-input"
     invalid-feedback="pwdInput"
   >
   <b-form-input
     id="pwdnew2-input"
     v-model="this.$props.user.username"
     type="password"
   ></b-form-input>
   </b-form-group>
     <b-button size="md" variant="danger">Canviar contrasenya</b-button>
     </b-col>
     </b-row>
     </form>
      </b-tab>
      <b-tab title="Configuració avançada">
      <form ref="form" @submit.stop.prevent="handleSubmit">
      <b-row>
      <b-col>
       <b-form-group
         label="Introdueix el teu correu electrònic"
         label-for="mail-input"
         invalid-feedback="pwdInput"
       >
       <b-form-input
         id="mail-input"
         v-model="this.$props.user.email"
         type="email"
       ></b-form-input>
     </b-form-group>
     <b-form-group
       label="Contrasenya"
       label-for="pwd-input"
       invalid-feedback="pwdInput"
     >
     <b-form-input
       id="pwd-input"
       type="password"
     ></b-form-input>
   </b-form-group>
   <b-form-group
     label="Repeteix la contrasenya"
     label-for="pwd2-input"
     invalid-feedback="pwdInput"
   >
   <b-form-input
     id="pwd2-input"
     type="password"
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

export default {
  props: {
    user: Object
  },
  data () {
    return {
      username: '',
      mail1: ''
    }
  },
  methods: {
  }
}
</script>
