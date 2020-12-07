<template>
<div id="app" v-if="user.role === adminRole">
<navbar @changeShowState="show = !show"/>
<br>
<div class="body" v-if="show === true">
<b-container>
  <b-row>
    <b-col sm="6" md="4" lg="4" xl="4">
    <h4> Transaccions a mostrar : {{ allTransactions.length }} </h4>
    </b-col>
    <b-col sm="3" md="2" lg="2" xl="2" align-v="left">
    </b-col>
  </b-row>
</b-container>
<addbooks/>
<br>
<b-container>
<b-row align-v="center">
    <b-col sm="6" xl="8">
    <b-form-input v-model="search" type="number" placeholder="Filter by ID"></b-form-input>
    </b-col>
</b-row>
<br>
<b-row align-v="center">
    <b-col sm="2" xl="2">
    <b-form-input v-model="isbnSearch" type="number" placeholder="ISBN"></b-form-input>
    </b-col>
    <b-col sm="2" xl="2">
    <b-form-input v-model="userSearch" type="number" placeholder="User ID"></b-form-input>
    </b-col>
    <b-col sm="2" xl="4">
    <b-form-select v-model="selected" :options="options"></b-form-select>
    </b-col>
    <b-col sm="2" xl="2">
    <b-button @click="advancedSearch()" variant="secondary">Cerca</b-button>
    </b-col>
    <b-col sm="2" xl="2">
    <b-button @click="cleanInputs();makeToast()" variant="secondary">Neteja</b-button>
    </b-col>
</b-row>
</b-container>
<br>
<br>
<b-container>
 <b-card-group deck v-for="(transaction) in filteredList" :key="transaction[0].id_transaction">
  <b-card bg-variant="light" text-variant="dark">
  <b-card-title> Transaction ID : {{ transaction[0].id_transaction }} </b-card-title>
  <b-card-sub-title class="mb-2">User ID : {{ transaction[0].user_id }}</b-card-sub-title>
  <b-card-sub-title class="mb-2">Date : {{ transaction[0].date }}</b-card-sub-title>
  <b-card-sub-title class="mb-2">Preu total : {{ getPreuTotal(transaction) }} $ </b-card-sub-title>
   <b-collapse :id="'collapse-' + transaction[0].id_transaction" class="mt-2">
      <b-card v-for="(line) in transaction" :key="line.book.isbn">
        <h4> {{ line.book.titulo }} - {{ line.book.isbn }} </h4>
        <p> Autor: {{ line.book.autor }} </p>
        <p> Preu del llibre: {{ line.book.precio }} $ </p>
        <p> Quantitat comprada: {{ transaction[0].quantity }} </p>
        <p> Preu pagat: {{ line.book.precio * transaction[0].quantity }} $</p>
      </b-card>
   </b-collapse>
   <br>
   <b-button v-b-toggle = "'collapse-' + transaction[0].id_transaction" variant="secondary">Detalls</b-button>
  </b-card>
</b-card-group>
<h3 v-if="allTransactions.length === 0"> No hi han transaccions a mostrar </h3>
<h3 v-if="filteredList.length === 0 && allTransactions.length !== 0"> No hi han transaccions a mostrar amb aquest ID </h3>
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
      allTransactions: [],
      search: '',
      show: true,
      user: {},
      userRole: 'User',
      price: 0.0,
      selected: null,
      isbnSearch: null,
      userSearch: null,
      options: [
        { value: null, text: 'Data' },
        { value: 'asc', text: 'Més antigues primer' },
        { value: 'desc', text: 'Més noves primer' }
      ]
    }
  },
  created () {
    this.fetch_session()
    this.getTransactions()
  },
  methods: {
    getTransactions () {
      const path = this.$API_URL + 'allTransactions'
      axios.get(path, { auth: { username: this.user.token } })
        .then((res) => {
          this.allTransactions = res.data.transactions
        })
        .catch((error) => {
          console.error(error)
        })
    },
    fetch_session () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_boolean = true
      }
    },
    getPreuTotal (trans) {
      var i
      var price = 0.0
      for (i = 0; i < trans.length; i++) {
        price += trans[i].price * trans[i].quantity
      }
      price = parseFloat(price.toFixed(2))
      return price
    },
    advancedSearch () {
      const path = this.$API_URL + 'allTransactions'
      var params = this.parseParameters()
      const headers = {'auth': { username: this.user.token },
        params: params}
      axios.get(path, headers)
        .then((res) => {
          this.allTransactions = res.data.transactions
          console.log(res.data.transactions)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    parseParameters () {
      var obj = {}
      if (this.isbnSearch) {
        obj.isbn = this.isbnSearch
      }
      if (this.userSearch) {
        obj.user_id = this.userSearch
      }
      if (this.selected) {
        obj.date = this.selected
      }
      return obj
    },
    cleanInputs () {
      this.isbnSearch = null
      this.userSearch = null
      this.selected = null
      this.search = ''
      this.getTransactions()
    },
    makeToast () {
      this.$bvToast.toast('Els camps han sigut netejats', {
        title: 'Camps nets',
        variant: 'info',
        solid: true
      })
    },
    redirect () {
      if (this.user.role === this.userRole) {
        window.location.replace('/notfound')
      }
    }
  },
  computed: {
    filteredList () {
      if (this.allTransactions.length !== 0 && this.search !== '') {
        return this.allTransactions.filter(trans => trans[0].id_transaction.toString().includes(this.search))
      } else {
        return this.allTransactions
      }
    }
  }
}
</script>
