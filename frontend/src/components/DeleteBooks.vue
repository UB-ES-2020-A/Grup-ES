<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="info">
      <b-navbar-brand href="#">NavBar</b-navbar-brand>
    </b-navbar>
    <b-container>
      <div class="row d-flex justify-content-center">
      <div class="col-sm-4">
      <div class="form-control bg-light" style="margin-top: 100px">
      <div class="form-label-group">
              <div class="row justify-content-center"><h4>Borrar libro</h4></div>
              <b-row>
              <b-container>
              <b-row align-h="between">
                <b-col>
                  <input id="isbn" class="form-control"
                  placeholder="ISBN" required autofocus v-model="isbn" type="number" style="margin-top: 15px">
                </b-col>
              </b-row>
              <b-button v-b-modal.modal-1 variant="primary" style="margin-top: 10px">Borrar libro</b-button>
             </b-container>
             </b-row>

      </div>
      </div>
      </div>

      <!-- modal -->
      <b-modal id="modal-1" hide-footer ref="modal-1" title="Borrar Libro">
        <p class="my-4">¿Estas seguro de borrar el libro con el ISBN: {{isbn}}?</p>
        <b-row align-h="center">
          <b-col cols="2">
            <b-button @click="deleteBook()"> OK </b-button>
          </b-col>
          <b-col cols="2">
            <b-button @click="$bvModal.hide('modal-1')"> NO </b-button>
          </b-col>
        </b-row>
      </b-modal>

      <div class="col-sm-6">
      <b-container style="margin-top: 100px">
        <img :src="'https://placehold.it/240x340/'" >
      </b-container>
      </div>

      </div>
    </b-container>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data () {
    return {
      isbn: ''
    }
  },
  methods: {
    deleteBook () {
      const path = 'https://grup-es.herokuapp.com/book/' + this.isbn
      axios.delete(path)
        .then((res) => {
          console.log('BOOK DELETED')
          this.isbn = ''
          alert('Book deleted from db')
          this.$refs['modal-1'].hide()
        })
        .catch((error) => {
        // eslint-disable-next-line
          console.log(error)
        })
    }
  }
}
</script>
