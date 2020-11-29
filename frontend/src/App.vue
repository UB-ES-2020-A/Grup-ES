<template>
    <router-view/>
</template>
<script>
export default {
  name: 'App'
}
document.title = 'BookShelter'
</script>

<style>
.modal-backdrop{
  opacity: 0.5;
}

.body{
  display: flex;
  min-height: 100vh;
  flex-direction: column;
}

.foot{
  background-color:#e0dede;
  bottom:0;
  position:sticky;
  width:100%;
}
</style>
