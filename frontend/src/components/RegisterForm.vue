<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-md">
      <div class="form-control" style="margin-top: 100px">
      <div class="form-label-group">
              <h5>Crear cuenta</h5>
              <label style="margin-top: 15px">Username</label>
              <input type="username" id="inputUsername" class="form-control"
              placeholder="Username" required autofocus v-model="username">

              <label style="margin-top: 15px">Correo electronico</label>
              <input type="e-mail" id="inputEmail" class="form-control"
              placeholder="Correo Electronico" required autofocus v-model="email1">

              <label style="margin-top: 15px">Contraseña</label>
              <input type="password" id="inputPassword1" class="form-control"
              placeholder="Contraseña" required v-model="password1">

              <label style="margin-top: 15px">Confirmar contraseña</label>
              <input type="password" id="inputPassword2" class="form-control"
              placeholder="Confirmar contraseña" required v-model="password2">

              <b-button variant="danger" style="margin-top: 20px">Crear usuario</b-button>
      </div>
      </div>
      </div>
      </div>
    </b-container>
  </div>
</template>

<script>
export default {
  data () {
    return {
    }
  },
  methods: {
  }
}
</script>
