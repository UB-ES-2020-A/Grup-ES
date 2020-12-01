<template>
<div id="app">
<navbar @changeShowState="show = !show"/>
<br>
<div class="body" v-if="show === true">
<b-container>
  <b-row>
    <b-col sm="6" md="4" lg="4" xl="4">
    <h4> Transaccions efectuades : {{ allTransactions.length }} </h4>
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
    <b-form-input v-model="search" placeholder="Filter by ID"></b-form-input>
    </b-col>
</b-row>
</b-container>
<br>
<br>
<b-container>
 <b-card-group deck v-for="(transaction) in allTransactions" :key="transaction[0].id_transaction">
  <b-card bg-variant="light" text-variant="dark">
  <b-card-title> Transaction ID : {{ transaction[0].id_transaction }} </b-card-title>
  <b-card-sub-title class="mb-2">User ID : {{ transaction[0].user_id }}</b-card-sub-title>
  <b-card-sub-title class="mb-2">Date : {{ transaction[0].date }}</b-card-sub-title>
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
      user: {}
    }
  },
  created () {
    this.fetch_session()
    this.getTransactions()
  },
  methods: {
    getTransactions () {
      const path = this.$API_URL + 'transactions/' + this.user.email
      axios.get(path, { auth: { username: this.user.token } })
        .then((res) => {
          this.allTransactions = res.data.transactions
          console.log(res)
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
    }
  }
}
</script>
