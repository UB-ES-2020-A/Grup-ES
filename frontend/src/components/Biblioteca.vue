<template>
<div id="app" v-if="user.role === userRole">
<navbar ref="c" @changeShowState="show = !show"/>
<!--body-->
<div class="body">
<div v-if= "show === true">
  <b-container fluid="sm" style="margin-left:100px; margin-right:50px">
  <b-container fluid style="height: 100px; background: #808080;" >
  <b-row align-h="end">
    <b-col sm="3" md="5" lg="5" xl="4">
      <b-input-group class="mb-2" style="margin-top:25px">
      <b-input-group-prepend is-text>
        <b-icon icon="search"></b-icon>
      </b-input-group-prepend>
      <b-form-input type="search" v-model="search"  placeholder="Filter by title"></b-form-input>
    </b-input-group>
    </b-col>
  </b-row>
  </b-container>
  <!--select biblio-->
  <b-row>
    <b-col sm="3" md="5" lg="5" xl="4">
     <b-nav tabs style="margin-top: 40px">
       <b-nav-item @click="choose_bought()" v-on:click="archived = false">Mis Libros</b-nav-item>
       <b-nav-item @click="choose_archive()">Archivo</b-nav-item>
      </b-nav>
    </b-col>
  </b-row>
  <b-row align-h="between" style="margin-top: 20px">
    <b-col sm="3" md="5" lg="5" xl="4">
    <b-form-select
      v-model="selected"
      :options="options"
      class="mb-3"
      value-field="value"
      text-field="text"
      disabled-field="notEnabled"
      @change="getItem($event)"
      v-if="archived === false"
    ></b-form-select>
    </b-col>
    <b-col sm="3" md="5" lg="5" xl="4">
    <b-form-select
      v-model="sFilter"
      :options="filters"
      class="mb-3"
      value-field="value"
      text-field="filter"
      @change="getFilter($event)"
      disabled-field="notEnabled"
    >
    <template #first>
      <b-form-select-option :value="null" disabled>Filtrar Biblioteca </b-form-select-option>
    </template>
    </b-form-select>
    </b-col>
  </b-row>

    <b-row>
      <div class="form-control bg-light" v-if="archived===false">
       <b-row>
       <b-col sm="3" md="5" lg="5" xl="4" style="margin-left:30px; margin-top:50px" v-for="(book) in filteredList" v-bind:key="book.isbn">
       <b-card-group>
       <b-card
         :img-src="getURL(book)"
         img-alt="Image"
         img-top
         tag="article"
         style="max-width: 20rem;"
         class="mb-2"
       >
          <div class="card-title">
          <b-row>
            <b-col cols="9">
              <h5>{{book.titulo}}<h5>
            </b-col>
            <b-col cols="2">
              <b-dropdown variant="link" no-caret>
               <template #button-content>
                <b-icon icon="three-dots"></b-icon>
               </template>
               <b-dropdown-item @click="markFinished(book)">Marcar como Leido</b-dropdown-item>
               <b-dropdown-item @click="markPending(book)">Marcar como Pendientes</b-dropdown-item>
               <b-dropdown-item @click="markReading(book)">Leyendo Actualmente</b-dropdown-item>
               <b-dropdown-item @click="moveArchive(book)">Archivar</b-dropdown-item>
              <b-dropdown-item-button>
            </b-col>
          </b-row>
         </div>
         <h6 class="card-subtitle">{{book.autor}}</h6>
       </b-card>
       </b-card-group>
       </b-col>
       </b-row>
       </div>
       <!--archive-->
       <div class="form-control bg-light" v-if="archived===true">
        <b-row>
        <b-col sm="3" md="5" lg="5" xl="4" style="margin-left:30px; margin-top:50px" v-for="(book) in filteredList" v-bind:key="book.isbn">
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
            <b-row>
              <b-col cols="9">
                <h5>{{book.titulo}}<h5>
              </b-col>
              <b-col cols="2">
                <b-dropdown variant="link" no-caret>
                <template #button-content>
                  <b-icon icon="three-dots"></b-icon>
                </template>
                <b-dropdown-item @click="moveBooks(book)">Sacar del Archivo</b-dropdown-item>
                <b-dropdown-item-button>
              </b-col>
            </b-row>
          </div>
          <h6 class="card-subtitle">{{book.autor}}</h6>
        </b-card>
        </b-card-group>
        </b-col>
        </b-row>
        </div>
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
      // Roles
      adminRole: 'Admin',
      userRole: 'User',

      show: true,
      list: [],
      library: [],
      bought: [],
      archive: [],
      pending: [],
      reading: [],
      finished: [],
      user: {},
      book: {},
      search: '',
      archived: false,
      selected: 'A',
      sFilter: null,
      options: [
        { value: 'A', text: 'Libros' },
        { value: 'B', text: 'Sin Leer' },
        { value: 'C', text: 'Leidos' },
        { value: 'D', text: 'Leyendo' }
      ],
      filters: [
        { value: 'A', filter: 'Titulo: de A a Z' },
        { value: 'B', filter: 'Titulo: de Z a A' },
        { value: 'C', filter: 'Autor: de A a Z' },
        { value: 'D', filter: 'Autor: de Z a A' }
      ]
    }
  },
  created () {
    this.fetch_cache()
    this.redirect()
    this.load_library()
    this.list = this.bought
  },
  methods: {
    gotobook (book) {
      this.$router.push({ path: '/book', query: {bk: book.isbn} })
    },
    load_library () {
      const path = this.$API_URL + 'userLibrary/' + this.user.email
      axios.get(path, {
        auth: {username: this.user.token}
      })
        .then((res) => {
          this.library = res.data.library
          console.log(this.library)
          this.manage_library()
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
    markFinished (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const path2 = this.$API_URL + 'userLibrary/' + this.user.email
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Finished'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.all([
        axios.put(path, parameters, auth),
        axios.get(path2, auth)
      ])
        .then(axios.spread((dataput, dataget) => {
          this.$refs.c.showToast(['Info', 'Libro marcado como leido'])
          this.update_changes()
          this.library = dataget.data.library
          this.manage_library()
        }))
        .catch((error) => {
          console.error(error)
        })
    },
    markPending (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const path2 = this.$API_URL + 'userLibrary/' + this.user.email
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Pending'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.all([
        axios.put(path, parameters, auth),
        axios.get(path2, auth)
      ])
        .then(axios.spread((dataput, dataget) => {
          this.$refs.c.showToast(['Info', 'Libro marcado como pendiente'])
          this.update_changes()
          this.library = dataget.data.library
          this.manage_library()
        }))
        .catch((error) => {
          console.error(error)
        })
    },
    markReading (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/' + book.isbn
      const path2 = this.$API_URL + 'userLibrary/' + this.user.email
      const parameters = {
        isbn: book.isbn,
        library_type: 'Bought',
        state: 'Reading'
      }
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.all([
        axios.put(path, parameters, auth),
        axios.get(path2, auth)
      ])
        .then(axios.spread((dataput, dataget) => {
          this.$refs.c.showToast(['Info', 'Leyendo el libro actualmente'])
          this.update_changes()
          this.library = dataget.data.library
          this.manage_library()
        }))
        .catch((error) => {
          console.error(error)
        })
    },
    goPedidos () {
      this.$router.push({path: '/mispedidos'})
    },
    manage_library () {
      var i
      for (i = 0; i < this.library.length; i++) {
        if (this.library[i].library_type === 'Bought' && this.library[i].visible) {
          this.bought.push(this.library[i].book)
          switch (this.library[i].state) {
            case 'Pending':
              this.pending.push(this.library[i].book)
              break
            case 'Reading':
              this.reading.push(this.library[i].book)
              break
            case 'Finished':
              this.finished.push(this.library[i].book)
              break
          }
        }
        if (!this.library[i].visible) {
          this.archive.push(this.library[i].book)
        }
      }
      console.log(this.bought)
    },
    choose_bought () {
      this.list = this.bought
    },
    choose_archive () {
      this.list = this.archive
      this.archived = true
    },
    choose_pending () {
      this.list = this.pending
    },
    choose_finished () {
      this.list = this.finished
    },
    choose_reading () {
      this.list = this.reading
    },
    getItem (event) {
      console.log(this.selected)
      switch (this.selected) {
        case 'A':
          this.choose_bought()
          break
        case 'B':
          this.choose_pending()
          break
        case 'C':
          this.choose_finished()
          break
        case 'D':
          this.choose_reading()
          break
      }
    },
    getFilter (event) {
      console.log(this.sFilter)
      switch (this.sFilter) {
        case 'A':
          this.list.sort(function (a, b) {
            var title1 = a.titulo.toUpperCase()
            var title2 = b.titulo.toUpperCase()
            if (title1 < title2) {
              return -1
            }
            if (title1 > title2) {
              return 1
            }
            return 0
          })
          break
        case 'B':
          this.list.sort(function (a, b) {
            var title1 = a.titulo.toUpperCase()
            var title2 = b.titulo.toUpperCase()
            if (title1 < title2) {
              return -1
            }
            if (title1 > title2) {
              return 1
            }
            return 0
          })
          this.list.reverse()
          break
        case 'C':
          this.list.sort(function (a, b) {
            var autor1 = a.autor.toUpperCase()
            var autor2 = b.autor.toUpperCase()
            if (autor1 < autor2) {
              return -1
            }
            if (autor1 > autor2) {
              return 1
            }
            return 0
          })
          break
        case 'D':
          this.list.sort(function (a, b) {
            var autor1 = a.autor.toUpperCase()
            var autor2 = b.autor.toUpperCase()
            if (autor1 < autor2) {
              return -1
            }
            if (autor1 > autor2) {
              return 1
            }
            return 0
          })
          this.list.reverse()
          break
      }
    },
    moveArchive (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/visibility/' + book.isbn
      const path2 = this.$API_URL + 'userLibrary/' + this.user.email
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.all([
        axios.delete(path, auth),
        axios.get(path2, auth)
      ])
        .then(axios.spread((datadelete, dataget) => {
          this.$refs.c.showToast(['Info', 'Libro archivado'])
          this.update_changes()
          this.library = dataget.data.library
          this.manage_library()
        }))
        .catch((error) => {
          console.error(error)
        })
    },
    moveBooks (book) {
      const path = this.$API_URL + 'library/' + this.user.email + '/visibility/' + book.isbn
      const path2 = this.$API_URL + 'userLibrary/' + this.user.email
      const auth = {'auth': {
        username: this.user.token}
      }
      axios.all([
        axios.post(path, {}, auth),
        axios.get(path2, auth)
      ])
        .then(axios.spread((datapost, dataget) => {
          this.$refs.c.showToast(['Info', 'Libro desarchivado'])
          this.update_changes()
          this.library = dataget.data.library
          this.manage_library()
        }))
        .catch((error) => {
          console.error(error)
        })
    },
    update_changes () {
      this.library = []
      this.bought = []
      this.archive = []
      this.pending = []
      this.reading = []
      this.finished = []
    },
    redirect () {
      if (this.user.role === this.adminRole) {
        window.location.replace('/notfound')
      }
    }
  },
  computed: {
    filteredList () {
      if (this.list.length !== 0 && this.search !== '') {
        return this.list.filter(book => book.titulo.toLowerCase().includes(this.search.toLowerCase()))
      } else {
        return this.list
      }
    }
  }
}
</script>
