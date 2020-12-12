<template>
  <div>
    <b-modal
    id="deletebooks"
    title="Eliminar llibre"
    @ok="deleteBook">
      <form ref="form">
       <b-row>
       <b-col>
        <b-form-group
          label="ISBN"
          label-for="isbn-input"
        >
        <b-form-input
          id="isbn-input"
          v-model="this.$props.isbnNum"
          type="number"
          disabled
        ></b-form-input>
      </b-form-group>
    </form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  props: {
    isbnNum: Number
  },
  data () {
    return {
      user: {}
    }
  },
  created () {
    this.fetch_cache()
  },
  methods: {
    deleteBook () {
      const path = this.$API_URL + 'book/' + this.$props.isbnNum
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.delete(path, auth)
        .then((res) => {
          this.$refs.c.showToast(['Info', 'El libro ha sido borrado de la página'])
          location.reload()
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
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    }
  }
}
</script>
