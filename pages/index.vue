<template>
  <div style="min-height: 75%">
    <div class="mt-5 text-center font-weight-bolder">
      <div class="pt-5 mb-5">
        <h1> Welcome to the Virtual Manager</h1>
      </div>
      <div>
        <p>Virtual Manager is a test application created with Vue.js & Python aiohttp on the server side.</p>
      </div>
      <div>
        <p>Start your demo tour by clicking some link above.</p>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  components: {

  },
  data () {
    return {
      current: []
    }
  },
  mounted () {
    console.log(window.location.hostname)
  }
}
</script>

<style>

</style>
