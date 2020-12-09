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
        })
    }
  }
}
</script>
