<template>
<div id="app">
<navbar @changeShowState="show = !show"/>
<div class="body" v-if="show === true">
  <settings :user="user"/>
  <b-container>
    <b-row>
    <b-col sm="12" md="6" lg="4" xl="4" class="border border-secondary">
      <b-row class="d-flex justify-content-center">
        <b-icon icon="person-circle" font-scale="4" class="m-3"></b-icon>
        <b-icon icon="pencil-fill" v-b-modal.settings font-scale="1"></b-icon>
      </b-row>
      <br>
      <b-row class="d-flex justify-content-center">
        <h4> {{user.username}} </h4>
      </b-row>
      <br>
      <b-row class="d-flex justify-content-center">
        <b-icon icon="mailbox" font-scale="1"></b-icon>
        <h4> {{user.email}} </h4>
      </b-row>
    </b-col>
    <b-col sm="12" md="5" lg="7" xl="7" offset-sm="0" offset-md="1" offset-lg="1" offset-xl="1">
      <b-row>
        <h3> La teva biblioteca </h3>
      </b-row>
      <b-row>
        <b-col  v-if="ped <= librarytoshow" v-for="ped in librarytoshow" :key="ped">
        <br>
        <img :src="getURL(pedidos[ped - 1].book)" style="height:209px; width:140px;" alt="">
        <h6>{{ pedidos[ped - 1].book.titulo }}</h6>
        <h5>{{ pedidos[ped - 1].book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <br>
      <b-row>
        <h3> Les teves últimes compres </h3>
      </b-row>
      <b-row>
        <b-col  v-if="ped <= transtoshow" v-for="ped in transtoshow" :key="ped">
        <br>
        <img :src="getURL(pedidos[ped - 1].book)" style="height:209px; width:140px;" alt="">
        <h6>{{ pedidos[ped - 1].book.titulo }}</h6>
        <h5>{{ pedidos[ped - 1].book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-button pill variant="outline-secondary" @click="transtoshow += 3"> + Veure'n més</b-button>
      </b-row>
      <br>
      <br>
      <b-row>
        <h3> La teva llista de desitjos </h3>
      </b-row>
      <b-row>
        <b-col  v-if="ped <= wishestoshow" v-for="ped in wishestoshow" :key="ped">
        <br>
        <img :src="getURL(pedidos[ped - 1].book)" style="height:209px; width:140px;" alt="">
        <h6>{{ pedidos[ped - 1].book.titulo }}</h6>
        <h5>{{ pedidos[ped - 1].book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-button pill variant="outline-secondary" @click="wishestoshow += 3"> + Veure'n més</b-button>
      </b-row>
      <br>
      <br>
      <b-row>
        <h3> La teves reviews </h3>
      </b-row>
      <b-row v-for="(review) in reviews" :key="review.user_id">
      <div class="card">
        <div class="card-body">
          <h5 class="card-title">
            <b-icon icon="star-fill" v-if="review.score >= 1" font-scale="2.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 1" font-scale="2.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 2" font-scale="2.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 2" font-scale="2.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 3" font-scale="2.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 3" font-scale="2.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 4" font-scale="2.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 4" font-scale="2.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 5" font-scale="2.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 5" font-scale="2.5"></b-icon>
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">You commented on {{ getBookTitle(review.isbn) }}:</h6>
          <p class="card-text">{{review.review}}</p>
        </div>
      </div>
      </b-row>
    </b-col>
    </b-row>
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
import settings from './subcomponents/ProfileSettings'

export default {
  components: {
    navbar,
    foot,
    settings
  },
  data () {
    return {
      show: true,
      user: {},
      pedidos: [],
      library: [],
      reviews: [],
      wishlist: [],
      transtoshow: 3,
      wishestoshow: 3,
      librarytoshow: 3,
      reviewstoshow: 3
    }
  },
  created () {
    this.fetch_cache()
    this.load_pedidos()
    this.getReviews()
  },
  methods: {
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    load_pedidos () {
      const path = this.$API_URL + 'transactions/' + this.user.email
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.get(path, auth)
        .then((res) => {
          this.pedidos = res.data.transactions
          console.log(this.pedidos)
          this.pedidos = this.pedidos.concat(this.pedidos, this.pedidos)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_library () {
      const path = this.$API_URL + 'library/' + this.user.email
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.get(path, auth)
        .then((res) => {
          this.library = res.data.library
        })
        .catch((error) => {
          console.error(error)
        })
    },
    load_wishlist () {
      const path = this.$API_URL + 'library/' + this.user.email
      const params = {library_type: 'WishList'}
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.get(path, params, auth)
        .then((res) => {
          this.wishlist = res.data.library
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (book) {
      return book.url_imagen
    },
    getReviews () {
      const path = this.$API_URL + 'user/' + this.user.email
      const params = {
        reviews: true
      }
      axios.get(path, { params: params })
        .then((res) => {
          this.reviews = res.data.user.reviews
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getBookTitle (isbn) {
      const path = this.$API_URL + 'book/' + isbn
      var titulo = ''
      axios.get(path)
        .then((res) => {
          titulo = res.data.book.titulo
        })
        .catch((error) => {
          console.error(error)
        })
      return titulo
    }
  }
}
</script>
