<template>
  <div class="container">
    <a-col :span="8" style="border: #40a9ff solid 1px; background-color: #f0f8ff" class="py-4 rounded">
      <h2 style="font-weight: lighter">
        Sign in
      </h2>
      <a-input
        ref="userNameInput"
        v-model="username"
        placeholder="Login"
        style="width: 90%; margin-bottom: 12px"
        @keypress.enter="submitForm">
        <a-icon slot="prefix" type="user" />
        <a-tooltip slot="suffix" title="Type your username">
          <a-icon type="info-circle" style="color: rgba(0,0,0,.45)" />
        </a-tooltip>
      </a-input>
      <a-input
        ref="passwordInput"
        v-model="password"
        placeholder="Password"
        type="password"
        style="width: 90%; margin-bottom: 12px"
        @keypress.enter="submitForm">
        <a-icon slot="prefix" type="key" />
        <a-tooltip slot="suffix" title="Type your password">
          <a-icon type="info-circle" style="color: rgba(0,0,0,.45)" />
        </a-tooltip>
      </a-input>
      <a-button style="width: 90%; margin-bottom: 24px" @click="submitForm">
        Submit
      </a-button>
    </a-col>
  </div>
</template>

<script>

export default {
  components: {
  },
  layout: 'login',
  data () {
    return {
      username: '',
      password: ''
    }
  },
  methods: {
    submitForm () {
      // hardcode for user credentials below :)
      if (this.username === 'admin' && this.password === 'admin') {
        this.$cookie.set('username', 'admin')
        this.$router.push('/')
      } else {
        this.$message.error('Invalid credentials')
      }
    }
  }
}
</script>

<style>
.container {
  margin: 0 auto;
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
}

</style>
