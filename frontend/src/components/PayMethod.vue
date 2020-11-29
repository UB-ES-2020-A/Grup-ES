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
        <b-form-group
        label="Número de Tarjeta"
        label-for="card_number"
        :invalid-feedback="cardInvalid"
        :state="cardState"
        >
          <b-form-input
            id="card_number"
            v-model="card_number"
            :state="cardState"
            type="number"
            placeholder="#### #### #### ####"
          ></b-form-input>
        </b-form-group>
      </b-col>
      <b-col cols="6">
        <b-form-group
        label="Nombre del Titular"
        label-for="card_holder_name"
        :invalid-feedback="nameInvalid"
        :state="nameState"
        >
          <b-form-input
            id="card_holder_number"
            v-model="card_holder_name"
            :state="nameState"
            placeholder="NOMBRE APELLIDOS"
          ></b-form-input>
        </b-form-group>
      </b-col>
    </b-row>

    <b-row style="margin-top: 15px">
      <b-col cols="6">
        <label>Data de caducitat</label>
        <b-row>
          <b-col cols="4">
            <b-form-group
            label-for="month"
            :invalid-feedback="monthInvalid"
            :state="monthState"
            >
              <b-form-input
                id="month"
                v-model="month"
                :state="monthState"
                type="number"
              ></b-form-input>
          </b-col>
          <b-col cols="8">
            <b-form-group
            label-for="year"
            :invalid-feedback="yearInvalid"
            :state="yearState"
            >
              <b-form-input
                id="year"
                v-model="year"
                :state="yearState"
                type="number"
              ></b-form-input>
          </b-col>
        </b-row>
      </b-col>
      <b-col cols="6">
        <b-form-group
        label="CVC"
        label-for="card_cvc"
        :invalid-feedback="cvcInvalid"
        :state="cvcState"
        >
          <b-form-input
            id="card_cvc"
            v-model="card_cvc"
            :state="cvcState"
            type="number"
            placeholder="####"
          ></b-form-input>
        </b-form-group>
      </b-col>
    </b-row>
    <br>
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
  computed: {
    cardState () {
      if (this.card_number.toString().length === 16 && this.card_number >= 1000000000000) {
        return true
      }
      return false
    },
    cardInvalid () {
      if (this.card_number.toString().length === 16 && this.card_number < 1000000000000) {
        return 'Introduzca el número de tarjeta valido'
      }
    },
    nameState () {
      return this.card_holder_name.length > 0
    },
    nameInvalid () {
      if (this.card_holder_name.length < 0) {
        return 'Este campo no puede quedar vacio'
      }
    },
    monthState () {
      return this.month >= 1 && this.month <= 12
    },
    monthInvalid () {
      if (!(this.month >= 1 && this.month <= 12)) {
        return 'Introduzca un mes valido'
      }
    },
    yearState () {
      return this.year > 2020 && this.year <= 2026
    },
    yearInvalid () {
      if (!(this.year > 2020 && this.year <= 2026)) {
        return 'Introduzca un año valido'
      }
    },
    cvcState () {
      return this.card_cvc >= 100 && this.card_cvc <= 9999
    },
    cvcInvalid () {
      if (!(this.card_cvc >= 100 && this.card_cvc <= 9999)) {
        return 'El CVC no es valido'
      }
    }
  },
  data () {
    return {
      show_c: true,
      card_number: 0,
      card_holder_name: '',
      month: 12,
      year: 2021,
      card_cvc: 100,
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
    submitCard () {
      if (this.checkForm()) {
        var tmpitems = JSON.parse(localStorage.getItem('cartItems'))
        var cartItems = []
        if (tmpitems !== null) {
          cartItems = tmpitems
        }
        var isbns = []
        var prices = []
        var quantities = []
        for (var i = 0; i < cartItems.length; i++) {
          isbns.push(cartItems[i].book.isbn)
          prices.push(cartItems[i].book.precio)
          quantities.push(cartItems[i].quantity)
        }
        const parameters = {
          isbns: isbns,
          prices: prices,
          email: this.user.email,
          quantities: quantities
        }
        const path = this.$API_URL + 'transaction'
        axios.post(path, parameters, {auth: {username: this.user.token}})
          .then((res) => {
            console.log('PAID SUCCESSFULLY')
            alert('Transaction correctly realized!')
            cartItems = []
            localStorage.setItem('cartItems', JSON.stringify(cartItems))
          })
          .catch((error) => {
            console.error(error)
          })
      }
    }
  }
}
</script>
