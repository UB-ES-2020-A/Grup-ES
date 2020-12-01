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
        <b-row class="rounded" v-for="(fact) in pedidos" :key="fact[0].id_transaction">
          <!-- ATR:
          .isbn,
          .price,
          .id_user,
          .quantity,
          .date-->
          <b-col cols=12>
            <b-row class="bg-info">
              <b-col>
                <br>
                <h4>Factura {{ fact[0].id_transaction}}</h4>
                <h6 class="text-white">{{ fact[0].date}}<h6>
              </b-col>
            </b-row>
            <b-row style="background-color: rgb(212, 225, 248)">
              <b-col v-for="(line) in fact" :key="line.book.isbn" cols="1">
                <img :src="getURL(line.book)" style="height:150px; width:100px;" alt=""  @click = "gotobook(line.book.isbn)">
              </b-col>
            </b-row>
            <b-row class="bg-light">
              <div class="table-responsive">
                <table class="table">
                  <thead>
                    <tr>
                      <th scope="col" width=25%>ISBN</th>
                      <th scope="col" width=45%>Título</th>
                      <th scope="col" width=15%>Precio</th>
                      <th scope="col" width=15%>Cantidad</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(line) in fact" :key="line.book.isbn">
                      <th scope="row">{{line.book.isbn}}</th>
                      <td>{{line.book.titulo}}</td>
                      <td>{{line.price}}€</td>
                      <td>{{line.quantity}}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </b-row>
            <b-row>
              <br>
            </b-row>
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
