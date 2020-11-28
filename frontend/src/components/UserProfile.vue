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
        <b-col  v-for="(lib) in library" :key="lib.book.isbn">
        <br>
        <img :src="getURL(lib)" style="height:209px; width:140px;" alt="">
        <h6>{{ lib.book.titulo }}</h6>
        <h5>{{ lib.book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <br>
      <b-row>
        <h3> Les teves últimes compres </h3>
      </b-row>
      <b-row>
        <b-col  v-for="(ped) in pedidos" :key="ped.book.isbn">
        <br>
        <img :src="getURL(lib)" style="height:209px; width:140px;" alt="">
        <h6>{{ ped.book.titulo }}</h6>
        <h5>{{ ped.book.autor }}</h5>
        </b-col>
      </b-row>
      <b-row>
        <h3> La teva llista de desitjos </h3>
      </b-row>
      <b-row>
        <b-col  v-for="(ped) in pedidos" :key="ped.book.isbn">
        <br>
        <img :src="getURL(lib)" style="height:209px; width:140px;" alt="">
        <h6 >{{ ped.book.titulo }}</h6>
        <h5>{{ ped.book.autor }}</h5>
        </b-col>
      </b-row>
      <v-row v-for="(review) in this.reviews" :key="review.id">
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
              <b-icon icon="star" v-if="review.score<4" font-scale="2.5"></b-icon>
              <b-icon icon="star-fill" v-if="review.score >= 5" font-scale="2.5"></b-icon>
              <b-icon icon="star" v-if="review.score < 5" font-scale="2.5"></b-icon>
            </h5>
            <h6 class="card-subtitle mb-2 text-muted">You commented:</h6>
            <p class="card-text">{{review.review}}</p>
          </div>
        </div>
        <br>
      </v-row>
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
      reviews: []
    }
  },
  created () {
    this.fetch_cache()
    this.load_library()
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
          console.log(this.library)
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (lib) {
      return lib.book.url_imagen
    },
    getReviews () {
      const path = this.$API_URL + 'user/' + this.user.email
      const params = {
        reviews: true
      }
      axios.get(path, { params: params })
        .then((res) => {
          this.reviews = res.data.reviews
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
