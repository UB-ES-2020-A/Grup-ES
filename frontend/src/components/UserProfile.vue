<template>
<div id="app">
<navbar @changeShowState="show = !show"/>
<div class="body" v-if="show === true">
  <b-container>
    <b-row>
    <b-col sm="12" md="6" lg="4" xl="4" style ="background-color: #e9ecef">
      <b-row class="d-flex justify-content-center">
        <b-icon icon="person-circle" font-scale="4"></b-icon>
        <b-icon icon="pencil-fill" font-scale="1"></b-icon>
      </b-row>
      <br>
      <b-row class="d-flex justify-content-center">
        <h4> {{user.username}} </h4>
      </b-row>
      <br>
      <b-row class="d-flex justify-content-center">
        <b-icon icon="mailbox" font-scale="1"></b-icon>
        <h4> {{user.email}} </h4>
      </b-row>
    </b-col>
    <b-col sm="12" md="6" lg="8" xl="8">
      <b-row>
        <h3> La teva biblioteca </h3>
      </b-row>
      <b-row>

      </b-row>

    </b-col>
    </b-row>
  </b-container>
<!-- footer -->
<br>
<br>
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
      show: true,
      user: {}
    }
  },
  created () {
    this.fetch_cache()
  },
  methods: {
    fetch_cache () {
      var tmpuser = JSON.parse(localStorage.getItem('user_session'))
      if (tmpuser !== null) {
        this.user = tmpuser
        console.log(this.user.username)
        this.session_status = 'Log Out'
        this.session_boolean = true
      }
    }
  }
}
</script>
