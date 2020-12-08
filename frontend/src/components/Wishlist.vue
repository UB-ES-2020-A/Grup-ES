<template>
<div id="app" v-if="user.role === userRole">
<navbar @changeShowState="show = !show"/>
<!--body-->
<div class="body">
<div v-if= "show === true">
  <b-container fluid="sm" style="margin-left:100px; margin-right:50px">
  <!--select biblio-->
  <h1>Llista de Desitjos</h1>
    <b-row>
      <div class="form-control bg-light">
       <b-row>
       <div class="col-2"  style="margin-left:30px; margin-top:50px" v-for="(book) in list" v-bind:key="book.isbn">
       <b-col align-self="center">
       <img :src="getURL(book)" style="height:409px; width:240px;" alt=""  @click = "gotobook(book)">
       <b-row>
       <b-col align-self="center" style="margin-top: 10px">
       <h5 @click = "gotobook(book)">  {{ book.titulo }} </h5>
       </b-col>
       </b-row>
       <b-col>
       <h7>{{ book.autor }}</h7>
       </b-col>
       </b-col>
       </div>
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
      adminRole: 'Admin'
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
          console.log(this.library)
          this.manage_wishlist()
        })
        .catch((error) => {
          console.error(error)
        })
    },
    getURL (book) {
      return book.url_imagen
    },
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        console.log(this.user.username)
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    },
    manage_wishlist () {
      var i
      for (i = 0; i < this.library.length; i++) {
        this.wishlist.push(this.library[i].book)
      }
      console.log(this.wishlist)
    },
    redirect () {
      if (this.user.role === this.adminRole) {
        window.location.replace('/notfound')
      }
    }
  }
}
</script>
