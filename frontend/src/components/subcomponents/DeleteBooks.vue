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
    showToast (message) {
      // Use a shorter name for this.$createElement
      const h = this.$createElement
      // Increment the toast count
      this.count++
      // Create the message
      const vNodesMsg = h(
        'p',
        { class: ['text-center', 'mb-0'] },
        [message[1]]
      )
      // Create the title
      const vNodesTitle = h(
        'div',
        { class: ['d-flex', 'flex-grow-1', 'align-items-baseline', 'mr-2'] },
        [
          h('strong', { class: 'mb-0' }, message[0])
        ]
      )
      // Pass the VNodes as an array for message and title
      this.$bvToast.toast([vNodesMsg], {
        title: [vNodesTitle],
        toaster: 'b-toaster-top-center',
        solid: true,
        variant: 'info'
      })
    },
    deleteBook () {
      const path = this.$API_URL + 'book/' + this.$props.isbnNum
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.delete(path, auth)
        .then((res) => {
          this.showToast(['Info', 'El libro ha sido borrado de la página'])
          setTimeout(() => location.reload(), 2000)
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
