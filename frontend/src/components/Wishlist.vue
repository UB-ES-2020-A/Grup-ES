<template>
<div id="app" v-if="user.role === userRole">
<navbar ref="c" @changeShowState="show = !show"/>
<!--body-->
<div class="body">
<div v-if= "show === true">
  <b-container fluid="sm" style="margin-left:100px; margin-right:50px">
  <!--select biblio-->
  <h1>Llista de Desitjos</h1>
    <b-row>
      <div class="form-control bg-light">
       <b-row>
       <b-col sm="3" md="5" lg="4" xl="3" style="margin-left:30px; margin-top:50px" v-for="(book) in list" v-bind:key="book.isbn">
         <b-card-group>
         <b-card
           :img-src="getURL(book)"
           img-alt="Image"
           img-top
           tag="article"
           style="max-width: 20rem; max-height: 10;"
           class="mb-2 h-100"
         >
           <div class="card-title">
             <h5>{{book.titulo}}<h5>
           </div>
           <h6 class="card-subtitle">{{book.autor}}</h6>
         </b-card>
         </b-card-group>
       </b-col>
       </b-row>
       </div>
       <!--archive-->
    </b-row>
  </b-container>
  <br>
  <br>
</div>
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
      list: [],
      wishlist: [],
      user: {},
      book: {},

      // Roles
      adminRole: 'Admin',
      userRole: 'User'
    }
  },
  created () {
    this.fetch_cache()
    this.redirect()
    this.load_library()
    this.list = this.wishlist
  },
  methods: {
    gotobook (book) {
      this.$router.push({ path: '/book', query: {bk: book.isbn} })
    },
    load_library () {
      const path = this.$API_URL + 'userLibrary/' + this.user.email + '?library_type=WishList'
      axios.get(path, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.library = res.data.library
          this.manage_wishlist()
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
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    manage_wishlist () {
      var i
      for (i = 0; i < this.library.length; i++) {
        this.wishlist.push(this.library[i].book)
      }
    },
    redirect () {
      if (this.user.role === this.adminRole) {
        window.location.replace('/notfound')
      }
    }
  }
}
</script>
