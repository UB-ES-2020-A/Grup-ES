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
      const path = 'https://grup-es.herokuapp.com/book/' + this.$props.isbnNum
      axios.delete(path)
        .then((res) => {
          alert('Book Removed correctly')
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
