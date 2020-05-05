<template>
  <div>
    <a-menu v-model="current" mode="horizontal" class="px-3 mb-4">
      <a-menu-item key="index">
        <router-link to="/" class="d-flex align-items-center">
          <a-icon type="home"/>
          Home
        </router-link>
      </a-menu-item>
      <a-menu-item key="vm">
        <router-link to="/vm" class="d-flex align-items-center">
          <a-icon type="desktop" />
          Virtual Machines
        </router-link>
      </a-menu-item>
      <a-sub-menu style="float: right !important">
        <span
          slot="title"
          class="submenu-title-wrapper">
          <a-icon type="user" />
          User Actions
        </span>
        <a-menu-item disabled key="setting:3">
          My profile
        </a-menu-item>
        <a-menu-item @click="logout" key="setting:4">
          Logout
        </a-menu-item>
      </a-sub-menu>
    </a-menu>
    <nuxt />
  </div>
</template>

<script>
export default {
  components: {
  },
  data () {
    return {
      current: ['index']
    }
  },
  beforeMount () {
    const username = this.$cookie.get('username')
    if (!username || username !== 'admin') {
      this.$router.push('/login')
    }
  },
  methods: {
    logout () {
      this.$cookie.delete('username')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
html {
  font-family: 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
  font-size: 16px;
  word-spacing: 1px;
  -ms-text-size-adjust: 100%;
  -webkit-text-size-adjust: 100%;
  -moz-osx-font-smoothing: grayscale;
  -webkit-font-smoothing: antialiased;
  box-sizing: border-box;
}

*,
*:before,
*:after {
  box-sizing: border-box;
  margin: 0;
}

</style>
