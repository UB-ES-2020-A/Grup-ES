<template>
<div id="app" v-if="user.role === userRole">
<navbar ref="c" @changeShowState="show = !show"/>
<div class="body" v-if="show === true">
  <settings :user="user"/>
  <b-container>
    <b-row>
    <b-col sm="12" md="6" lg="4" xl="4">
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
      <b-row class="d-flex justify-content-center">
        <h5> Llibres a la biblioteca: {{ pedidos.length }} </h5>
      </b-row>
      <b-row class="d-flex justify-content-center">
        <h5> Llibres a la llista de desitjos: {{ wishlist.length }} </h5>
      </b-row>
      <b-row class="d-flex justify-content-center">
        <h5> Reviews escrites: {{ reviews.length }} </h5>
      </b-row>
      <br>
      <b-row v-for="(review) in reviews" :key="review.user_id" class="d-flex align-items-stretch">
      <div class="card" style="width: 100%">
        <div class="card-body">
          <h5 class="card-title">
            <b-icon icon="star-fill" v-if="review.score >= 1" font-scale="1.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 1" font-scale="1.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 2" font-scale="1.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 2" font-scale="1.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 3" font-scale="1.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 3" font-scale="1.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 4" font-scale="1.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 4" font-scale="1.5"></b-icon>
            <b-icon icon="star-fill" v-if="review.score >= 5" font-scale="1.5"></b-icon>
            <b-icon icon="star" v-if="review.score < 5" font-scale="1.5"></b-icon>
          </h5>
          <h6 class="card-subtitle mb-2 text-muted">You commented on {{ getBookTitle(review.isbn, pedidos) }}:</h6>
          <p class="card-text">{{review.review}}</p>
          <br>
        </div>
      </div>
      </b-row>
    </b-col>
    <b-col sm="12" md="5" lg="7" xl="7" offset-sm="0" offset-md="1" offset-lg="1" offset-xl="1">
      <b-row>
        <h3> La teva biblioteca </h3>
      </b-row>
      <b-row>
        <b-col  v-if="ped <= librarytoshow" v-for="ped in showPartialList (library, librarytoshow)" :key="ped">
        <br>
        <img :src="getURL(library[ped - 1].book)" style="height:209px; width:140px;" alt="">
        <h6>{{ library[ped - 1].book.titulo }}</h6>
        <h5>{{ library[ped - 1].book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-button pill variant="outline-secondary" :disabled = "library.length <= librarytoshow" @click="librarytoshow += 3"> + Veure'n més</b-button>
      </b-row>
      <br>
      <b-row>
        <h3> Les teves últimes compres </h3>
        <br>
      </b-row>
      <b-row>
        <b-table striped hover :items="transactions"></b-table>
      </b-row>
      <br>
      <b-row>
        <b-button pill variant="outline-secondary" @click="goPedidos()"> + Veure'n més</b-button>
      </b-row>
      <br>
      <br>
      <b-row>
        <h3> La teva llista de desitjos </h3>
      </b-row>
      <b-row>
        <b-col  v-if="ped <= wishestoshow" v-for="ped in showPartialList (wishlist, wishestoshow)" :key="ped">
        <br>
        <img :src="getURL(wishlist[ped - 1].book)" style="height:209px; width:140px;" alt="">
        <h6>{{ wishlist[ped - 1].book.titulo }}</h6>
        <h5>{{ wishlist[ped - 1].book.autor }}</h5>
        </b-col>
      </b-row>
      <br>
      <b-row>
        <b-button pill variant="outline-secondary" :disabled = "wishlist.length <= wishestoshow" @click="wishestoshow += 3"> + Veure'n més</b-button>
      </b-row>
      <br>
      <br>
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
      // Roles
      adminRole: 'Admin',
      userRole: 'User',

      user: {},
      transactions: [],
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
    this.redirect()
    this.load_pedidos()
    this.load_library()
    this.load_wishlist()
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
          this.manage_transactions(this.pedidos)
        })
        .catch((error) => {
          console.error(error)
          if (error.response.status === 401) {
            localStorage.removeItem('user_session')
            localStorage.removeItem('cartItems')
            window.location.replace('/userlogin')
          }
        })
    },
    load_library () {
      const path = this.$API_URL + 'userLibrary/' + this.user.email
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.get(path, auth)
        .then((res) => {
          this.library = res.data.library
        })
        .catch((error) => {
          console.error(error)
          if (error.response.status === 401) {
            localStorage.removeItem('user_session')
            localStorage.removeItem('cartItems')
            window.location.replace('/userlogin')
          }
        })
    },
    load_wishlist () {
      const path = this.$API_URL + 'userLibrary/' + this.user.email + '?library_type=WishList'
      // const params = {library_type: 'WishList'}
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.get(path, auth)
        .then((res) => {
          this.wishlist = res.data.library
        })
        .catch((error) => {
          console.error(error)
          if (error.response.status === 401) {
            localStorage.removeItem('user_session')
            localStorage.removeItem('cartItems')
            window.location.replace('/userlogin')
          }
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
    getBookTitle (isbn, array) {
      var i
      for (i = 0; i < array.length; i++) {
        if (array[i][0].book.isbn === isbn) {
          return array[i][0].book.titulo
        }
      }
      return ''
    },
    showPartialList (array, head) {
      if (array.length < head) {
        return array.length
      } else {
        return head
      }
    },
    redirect () {
      if (this.user.role === this.adminRole) {
        window.location.replace('/notfound')
      }
    },
    manage_transactions (ped) {
      var i, j
      for (i = 0; i < ped.length; i++) {
        for (j = 0; j < ped[i].length; j++) {
          this.transactions.push({
            isbn: ped[i][j].isbn,
            titulo: ped[i][j].book.titulo,
            fecha: ped[i][j].date,
            precio: ped[i][j].book.precio,
            cantidad: ped[i][j].quantity
          })
        }
      }
      this.transactions.reverse()
      this.transactions = this.transactions.slice(0, 3)
    },
    goPedidos () {
      this.$router.push({path: '/mispedidos'})
    }
  }
}
</script>
