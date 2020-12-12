<template>
<div id="app">
<navbar @changeShowState="show = !show"/>
<!--body-->
<div class="body">
<br>
<b-container>
  <b-button variant="primary" @click="goHome()">Tornar a l'inici</b-button>
  <b-row class="justify-content-center">
    <h1> La pàgina no és pot mostrar </h1>
    <br>
    <a> <img src="../assets/notfound.png" width="768" height="591"> </a>
  </b-row>
</b-container>

</div>
<foot/>
</div>
</template>

<script>
import navbar from './subcomponents/navbar'
import foot from './subcomponents/foot'

export default {
  components: {
    navbar,
    foot
  },
  data () {
    return {
      show: true
    }
  },
  methods: {
    goHome () {
      window.location.replace('/')
    }
  }
}
</script>
