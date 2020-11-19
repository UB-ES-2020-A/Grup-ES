<template>
<div id="app">
 <navbar @changeShowState="show_c = !show_c"/>
<!-- body -->
<div class="body">
<b-container v-if= "show_c === true">
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
    <br>
    <h5>Total a pagar: {{ calculate_total_price() }}$</h5>
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
<!-- footer -->
<br>
<br>
</div>
<foot/>
</div>
</template>

<script>
import axios from 'axios'
import navbar from './subcomponents/navbar'
import foot from './subcomponents/foot'

export default {
  components: {
    navbar,
    foot
  },
  data () {
    return {
      show_c: true,

      user: {},

      error: '',
      show: false
    }
  },
  created () {
    this.fetch_cache()
  },
  methods: {
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_boolean = true
      }
    },
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
    addToLibrary (parameters) {
      const path = 'https://grup-es.herokuapp.com/library'
      axios.post(path, parameters, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          console.log('BOOK ADDED TO LIBRARY')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    post_transaction (book, quantity) {
      const parameters = {
        isbn: book.isbn,
        price: book.precio,
        email: this.user.email,
        quantity: quantity
      }
      const path = 'https://grup-es.herokuapp.com/transaction'
      axios.post(path, parameters, {auth: {username: this.user.token}})
        .then((res) => {
          console.log('PAID SUCCESSFULLY')
          alert('Transaction correctly realized!')
        })
        .catch((error) => {
          console.error(error)
        })
    },
    submitCard () {
      if (this.checkForm()) {
        var tmpitems = JSON.parse(localStorage.getItem('cartItems'))
        var cartItems = []
        if (tmpitems !== null) {
          cartItems = tmpitems
        }
        for (var i = 0; i < cartItems.length; i++) {
          this.post_transaction(cartItems[i].book, cartItems[i].quantity)
          const parameters = {
            isbn: cartItems[i].book.isbn,
            email: this.user.email
          }
          this.addToLibrary(parameters)
        }
        cartItems = []
        localStorage.setItem('cartItems', JSON.stringify(cartItems))
      }
    }
  }
}
</script>
