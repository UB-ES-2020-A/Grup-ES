<template>
  <div>
    <b-modal
    id="addboks"
    title="Afegir nou llibre"
    @ok="handleOk">
      <form ref="form" @submit.stop.prevent="handleSubmit">
       <b-row>
       <b-col>
        <b-form-group
          label="ISBN"
          label-for="isbn-input"
          invalid-feedback="ISBN invalid, use a 13 digit number"
        >
        <b-form-input
          id="isbn-input"
          v-model="isbn"
          :state="isbnState"
          type="number"
        ></b-form-input>
      </b-form-group>
      <b-form-group
        label="Titol"
        label-for="title-input"
        invalid-feedback="Title field required"
      >
      <b-form-input
        id="title-input"
        v-model="titulo"
        :state="tituloState"
      ></b-form-input>
    </b-form-group>
    <b-form-group
      label="Autor"
      label-for="autor-input"
      invalid-feedback="Autor field required"
    >
      <b-form-input
        id="autor-input"
        v-model="autor"
        :state = "autorState"
      ></b-form-input>
    </b-form-group>

    <b-form-group
      label="Editorial"
      label-for="editorial-input"
      invalid-feedback="Editorial field required"
    >
    <b-form-input
      id="editorial-input"
      v-model="editorial"
      :state = "editorialState"
    ></b-form-input>
    </b-form-group>
    <b-form-group
      label="Stock"
      label-for="stock-input"
      invalid-feedback="Stock field invalid, use a postive number"
    >
    <b-form-input
      id="stock-input"
      :state="stockState"
      v-model="stock"
      type="number"
    ></b-form-input>
  </b-form-group>
    <b-form-group
      label="Preu"
      label-for="price-input"
      invalid-feedback="Price field invalid, use a postive number"
    >
    <b-form-input
      id="price-input"
      :state="precioState"
      v-model="precio"
      type = "number"
    ></b-form-input>
  </b-form-group>
  <b-form-group
    label="Any de publicació"
    label-for="year-input"
    invalid-feedback="Data field required"
  >
  <b-form-input
    id="year-input"
    v-model="date"
    type="date"
    format= 'yyyy-mm-dd'
    :state = "dateState"
  ></b-form-input>
  </b-form-group>
  <b-form-group
    label="URL portada"
    label-for="url-input"
    invalid-feedback="URL field required"
  >
  <b-form-input
    id="url-input"
    v-model="url"
    :state = "urlState"
  ></b-form-input>
</b-col>
<b-col>
<img :src="browseURL()" style="height:209px; width:140px;">
</b-col>
</b-row>
</form>
<b-row>
<b-col>
<b-form-group
  label="Sinopsis"
  label-for="sinopsis-input"
  invalid-feedback="Sinopsis field required"
>
<b-form-textarea
  id="sinopsis-input"
  rows="3"
  max-rows="6"
  v-model="sinopsis"
  :state="sinopsisState"
></b-form-textarea>
</b-form-group>
</b-col>
</b-row>
</b-modal>
</div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isbn: 0,
      stock: 0,
      precio: '',
      titulo: '',
      autor: '',
      editorial: '',
      date: '',
      url: '',
      sinopsis: '',
      isbnState: null,
      stockState: null,
      precioState: null,
      tituloState: null,
      autorState: null,
      urlState: null,
      editorialState: null,
      dateState: null,
      sinopsisState: null,
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
    addBook () {
      const parameters = {
        isbn: this.isbn,
        stock: this.stock,
        precio: this.precio,
        titulo: this.titulo,
        autor: this.autor,
        editorial: this.editorial,
        fecha_de_publicacion: this.date,
        url_imagen: this.url,
        sinopsis: this.sinopsis
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      const path = this.$API_URL + 'book'
      axios.post(path, parameters, auth)
        .then((res) => {
          this.showToast(['Info', 'Libro añadido a nuestra página'])
          this.clearModal()
          setTimeout(() => {
            this.$bvModal.hide('addboks')
            location.reload()
            this.clearModal()
          }, 2000)
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
    },
    clearModal () {
      this.isbn = 0
      this.stock = 0
      this.precio = ''
      this.titulo = ''
      this.autor = ''
      this.editorial = ''
      this.date = null
      this.url = ''
      this.sinopsis = ''
      this.isbnState = null
      this.stockState = null
      this.precioState = null
      this.isbnState = null
      this.stockState = null
      this.precioState = null
      this.tituloState = null
      this.autorState = null
      this.urlState = null
      this.editorialState = null
      this.dateState = null
      this.sinopsisState = null
    },
    browseURL () {
      if (this.url !== '') {
        return this.url
      }
      return 'https://placehold.it/240x340/'
    },
    checkOk () {
      if (this.isbn.length === 13) {
        this.isbnState = true
      } else {
        this.isbnState = false
      }
      if (!isNaN(this.precio) && parseInt(this.precio) > 0) {
        this.precioState = true
      } else {
        this.precioState = false
      }
      if (parseInt(this.stock) <= 0 || this.stock.length < 0) {
        this.stockState = false
      } else {
        this.stockState = true
      }
      if (this.titulo.length < 0 || this.titulo === '') {
        this.tituloState = false
      } else {
        this.tituloState = true
      }
      if (this.autor.length < 0 || this.autor === '') {
        this.autorState = false
      } else {
        this.autorState = true
      }
      if (this.editorial.length < 0 || this.editorial === '') {
        this.editorialState = false
      } else {
        this.editorialState = true
      }
      if (this.url.length < 0 || this.url === '') {
        this.urlState = false
      } else {
        this.urlState = true
      }
      if (this.sinopsis.length < 0 || this.sinopsis === '') {
        this.sinopsisState = false
      } else {
        this.sinopsisState = true
      }
      if (this.date.length < 0 || this.date === '') {
        this.dateState = false
      } else {
        this.dateState = true
      }
      if (this.isbnState && this.precioState && this.stockState &&
      this.autorState && this.editorialState && this.tituloState &&
    this.sinopsisState && this.dateState && this.urlState) {
        this.$nextTick(() => {
          this.addBook()
          this.$bvModal.hide('addboks')
        })
        return true
      }
      return false
    },
    handleOk (bvModalEvt) {
      bvModalEvt.preventDefault()
      this.checkOk()
    }
  }
}
</script>
