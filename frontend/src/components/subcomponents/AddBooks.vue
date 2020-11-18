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
          :state="isbnState"
          label="ISBN"
          label-for="isbn-input"
          invalid-feedback="ISBN invalid, use a 13 digit number"
        >
        <b-form-input
          id="isbn-input"
          v-model="isbn"
          :state="isbnState"
          type="number"
          required
        ></b-form-input>
      </b-form-group>
      <b-form-group
        label="Titol"
        label-for="title-input"
      >
      <b-form-input
        id="title-input"
        v-model="titulo"
      ></b-form-input>
    </b-form-group>
    <b-form-group
      label="Autor"
      label-for="autor-input"
    >
      <b-form-input
        id="autor-input"
        v-model="autor"
      ></b-form-input>
    </b-form-group>

    <b-form-group
      label="Editorial"
      label-for="editorial-input"
    >
    <b-form-input
      id="editorial-input"
      v-model="editorial"
    ></b-form-input>
    </b-form-group>
    <b-form-group
      label="Stock"
      label-for="stock-input"
      invalid-feedback="Stock field invalid, use a number"
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
      invalid-feedback="Price field invalid, use a number"
    >
    <b-form-input
      id="price-input"
      :state="precioState"
      v-model="precio"
    ></b-form-input>
  </b-form-group>
  <b-form-group
    label="Any de publicació"
    label-for="year-input"
  >
  <b-form-input
    id="year-input"
    v-model="date"
    type="date"
  ></b-form-input>
  </b-form-group>
  <b-form-group
    label="URL portada"
    label-for="url-input"
  >
  <b-form-input
    id="url-input"
    v-model="url"
  ></b-form-input>
</b-form-group>
<b-form-group
  label="Sinopsis"
  label-for="sinopsis-input"
>
<b-form-input
  id="sinopsis-input"
  v-model="sinopsis"
></b-form-input>
</b-form-group>
</b-col>
<b-col>
<img :src="browseURL()" style="height:209px; width:140px;">
</b-col>
</b-row>
    </form>
    </b-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      isbn: '',
      stock: '',
      precio: '',
      titulo: '',
      author: '',
      editorial: '',
      date: '',
      url: '',
      sinopsis: '',
      isbnState: null,
      stockState: null,
      precioState: null
    }
  },
  methods: {
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
      const path = 'https://grup-es.herokuapp.com/book'
      axios.post(path, parameters)
        .then((res) => {
          console.log('BOOK ADDED')
          this.initForm()
          alert('Book ADDED correctly')
        })
        .catch((error) => {
          this.initForm()
          console.error(error)
        })
    },
    clearModal () {
      this.isbn = ''
      this.stock = ''
      this.precio = ''
      this.titulo = ''
      this.autor = ''
      this.editorial = ''
      this.date = ''
      this.url = ''
      this.sinopsis = ''
      this.isbnState = null
      this.stockState = null
      this.precioState = null
    },
    browseURL () {
      if (this.url !== '') {
        return this.url
      }
      return 'https://placehold.it/240x340/'
    },
    checkOk () {
      if (this.isbn.length === 13 && Number.isInteger(this.isbn)) {
        this.isbnState = true
      } else {
        this.isbnState = false
      }
      if (Number.isInteger(this.stock)) {
        this.stockState = true
      } else {
        this.stockState = false
      }
      if (!isNaN(this.precio) && this.precio.toString().indexOf('.') !== -1) {
        this.precioState = true
      } else {
        this.precioState = false
      }
      if (this.isbnState && this.stockState && this.precioState && this.titulo.length > 0 &&
        this.autor.length > 0 && this.editorial.length > 0 &&
        this.precio.length > 0 && this.stock.length > 0) {
        this.$nextTick(() => {
          this.$bvModal.hide('addboks')
        })
        this.clearModal()
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
