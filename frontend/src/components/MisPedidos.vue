<template>
<div id="app">
 <navbar @changeShowState="show = !show"/>
<!-- body -->
<div class="body">
  <div v-if="show === true">
    <div v-if= "session_boolean === true">
      <br>
      <br>
      <div class="container">
        <h3> Mis Pedidos </h3>
        <b-row  v-for="(fact) in pedidos" :key="fact[0].id_transaction">
          <!-- ATR:
          .isbn,
          .price,
          .id_user,
          .quantity,
          .date-->
          <br>
          <div class="card">
            <div class="card-header">Factura: {{ fact[0].id_transaction}}</div>
            <div class="card-body">
              <b-col v-for="(line) in fact" :key="line.book.isbn">
                <hr>
                <b-col>
                <img :src="getURL(line.book)" style="height:109px; width:70px;" alt=""  @click = "gotobook(line.book.isbn)">
                </b-col>
                <br>
                <h6 @click = "gotobook(line.book.isbn)">Título del libro: {{ line.book.titulo }}</h6>
                <h6>Autor del libro: {{ line.book.autor }}</h6>
                <h6>Precio: {{ line.price}}</h6>
                <h6>Cantidad: {{ line.quantity}}</h6>
                <h6>Fecha de compra: {{ line.date}}</h6>
              </b-col>
            </div>
          </div>
        </b-row>
      </div>
    </div>
    <div v-if= "session_boolean === false">
      <br>
      <br>
      <div class="container">
        <h3> Mis Pedidos </h3>
        <h5> LogIn para poder ver tus pedidos </h5>
      </div>
    </div>
  </div>

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
      show: true,
      pedidos: [],

      // Session
      user: {},
      session_boolean: false
    }
  },
  created () {
    this.fetch_session()
    this.load_pedidos()
  },
  methods: {
    gotobook (isbn) {
      this.$router.push({ path: '/book', query: {bk: isbn} })
    },
    load_pedidos () {
      const path = this.$API_URL + 'transactions/' + this.user.email

      axios.get(path, { auth: { username: this.user.token } })
        .then((res) => {
          this.pedidos = res.data.transactions
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (book) {
      return book.url_imagen
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
