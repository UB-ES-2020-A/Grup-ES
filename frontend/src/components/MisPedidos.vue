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
        <b-row>
          <b-col  v-for="(pedido) in pedidos" :key="pedido.id_transaction">
            <!-- ATR:
            .isbn,
            .price,
            .id_user,
            .quantity,
            .date-->
            <div class="card">
              <div class="card-header">Factura: {{ pedido.id_transaction}}</div>
              <div class="card-body">
                <b-col>
                <img :src="getURL(pedido.book)" style="height:109px; width:70px;" alt=""  @click = "gotobook(pedido.book.isbn)">
                </b-col>
                <br>
                <h6 @click = "gotobook(book.isbn)">Título del libro: {{ pedido.book.titulo }}</h6>
                <h6>Autor del libro: {{ pedido.book.autor }}</h6>
                <h6>Precio: {{ pedido.price}}</h6>
                <h6>Cantidad: {{ pedido.quantity}}</h6>
                <h6>Fecha de compra: {{ pedido.date}}</h6>
              </div>
            </div>
          </b-col>
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
      const path = 'https://grup-es.herokuapp.com/transactions/' + this.user.email

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
