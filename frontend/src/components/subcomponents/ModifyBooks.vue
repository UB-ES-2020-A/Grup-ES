<template>
  <div>
    <b-modal
    id="modifybooks"
    title="Modificar llibre"
    @ok="handleOk"
    @shown="getInfoFromBook">
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
          v-model="this.$props.isbnNum"
          type="number"
          disabled
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
</b-form-group>
<b-form-group
  label="Sinopsis"
  label-for="sinopsis-input"
  invalid-feedback="Sinopsis field required"
>
<b-form-input
  id="sinopsis-input"
  v-model="sinopsis"
  :state="sinopsisState"
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
  props: {
    isbnNum: Number
  },
  data () {
    return {
      stock: '',
      precio: '',
      titulo: '',
      autor: '',
      editorial: '',
      date: '',
      url: '',
      sinopsis: '',
      stockState: null,
      precioState: null,
      tituloState: null,
      autorState: null,
      urlState: null,
      editorialState: null,
      dateState: null,
      sinopsisState: null
    }
  },
  methods: {
    addBook () {
      const parameters = {
        stock: this.stock,
        precio: this.precio,
        titulo: this.titulo,
        autor: this.autor,
        editorial: this.editorial,
        fecha_de_publicacion: this.date,
        url_imagen: this.url,
        sinopsis: this.sinopsis
      }
      const path = this.$API_URL + 'book/' + this.$props.isbnNum
      const headers = {'auth': { username: this.user.token },
        params: parameters}
      axios.put(path, headers)
        .then((res) => {
          alert('Book Modified correctly')
          this.clearModal()
        })
        .catch((error) => {
          console.error(error)
          this.clearModal()
        })
    },
    clearModal () {
      this.stock = ''
      this.precio = ''
      this.titulo = ''
      this.autor = ''
      this.editorial = ''
      this.date = null
      this.url = ''
      this.sinopsis = ''
      this.stockState = null
      this.precioState = null
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
      console.log(this.$props.isbnNum)
      if (!isNaN(this.precio) && this.precio.toString().indexOf('.') !== -1) {
        this.precioState = true
      } else {
        this.precioState = false
      }
      if (this.stock <= 0 || this.stock.length < 0) {
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
      if (this.precioState && this.stockState &&
      this.autorState && this.editorialState && this.tituloState &&
    this.sinopsisState && this.dateState && this.urlState) {
        this.$nextTick(() => {
          this.addBook()
          this.$bvModal.hide('modifybooks')
        })
        return true
      }
      return false
    },
    handleOk (bvModalEvt) {
      bvModalEvt.preventDefault()
      this.checkOk()
    },
    getInfoFromBook () {
      const path = this.$API_URL + 'book/' + this.$props.isbnNum
      axios.get(path)
        .then((res) => {
          this.precio = res.data.book.precio
          this.titulo = res.data.book.titulo
          this.autor = res.data.book.autor
          this.stock = res.data.book.stock
          this.editorial = res.data.book.editorial
          this.date = res.data.book.fecha_de_publicacion
          this.url = res.data.book.url_imagen
          this.sinopsis = res.data.book.sinopsis
        })
        .catch((error) => {
          console.error(error)
        })
    }
  }
}
</script>
