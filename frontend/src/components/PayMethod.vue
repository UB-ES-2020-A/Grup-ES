<template>
  <div id="app">
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand >NavBar</b-navbar-brand>
    </b-navbar>

    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-lg">
      <div class="form-control bg-light" style="margin-top: 100px">
      <div class="form-label-group">
        <div style="margin-top: 10px" class="row justify-content-center"><h4>Targeta de Crèdit</h4></div>

        <b-row style="margin-top: 15px">
          <b-col cols="6">
            <label>Número de Targeta</label>
            <input id="card_number" class="form-control" type="number"
            placeholder="#### #### #### ####" required autofocus v-model="card_number">
          </b-col>
          <b-col cols="6">
            <label>Nom del titular</label>
            <input id="card_holder_name" class="form-control"
            placeholder="NOM COGNOM" required autofocus v-model="card_holder_name">
          </b-col>
        </b-row>

        <b-row style="margin-top: 15px">
          <b-col cols="6">
            <label>Data de caducitat</label>
            <b-row>
              <b-col cols="4">
                <input id="month" class="form-control" type="number"
                placeholder="01" required autofocus v-model="month">
              </b-col>
              <b-col cols="8">
                <input id="year" class="form-control" type="number"
                placeholder="2021" required autofocus v-model="year">
              </b-col>
            </b-row>
          </b-col>
          <b-col cols="6">
            <label>CVC</label>
            <input id="card_cvc" class="form-control" type="number"
            placeholder="0000" required autofocus v-model="card_cvc">
          </b-col>
        </b-row>
        <b-col>
          <b-button size="lg" variant="primary" style="margin-top: 15px" @click="submitCard()">Submit</b-button>
        </b-col>
        <b-row style="margin-top: 10px"></b-row>
        <label v-if="show" style="color: red">{{this.error}}</label>
      </div>
      </div>
      </div>
      </div>
    </b-container>

  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      card_number: '',
      card_holder_name: '',
      month: '',
      year: '',
      card_cvc: '',
      show: false,
      error: 'e'
    }
  },
  methods: {
    checkForm: function (e) {
      this.errors = []

      if (!this.card_number || !this.card_holder_name || !this.card_cvc || !this.year || !this.month) {
        this.errors.push('És requereix emplenar tots els camps!')
      }

      if (this.card_number > 9999999999999999999 || this.card_number < 1000000000000) {
        this.errors.push('Número de targeta no vàlid!')
      }

      if (this.year > 2026 || this.year < 2020 || this.month < 1 || this.month > 12) {
        this.errors.push('Data de caducitat no vàlida!')
      }

      if (this.card_cvc < 100 || this.card_cvc > 9999) {
        this.errors.push('CVC no vàlid!')
      }

      if (!this.errors.length) {
        this.show = false
        return true
      }
      this.show = true
      this.error = this.errors[0]
      return false
    },
    submitCard () {
      if (this.checkForm()) {
        const parameters = {
          card_number: this.card_number,
          card_holder_name: this.card_holder_name,
          month: this.month,
          year: this.year,
          card_cvc: this.card_cvc
        }
        const path = 'https://grup-es.herokuapp.com/transaction/' + this.isbn
        axios.put(path, parameters)
          .then((res) => {
            console.log('PAID SUCCESSFULLY')
            alert('Transaction correctly realized!')
          })
          .catch((error) => {
            console.error(error)
          })
      }
    }
  }
}
</script>
