<template>
  <div>
    <a-icon key="edit" type="edit" @click="modal = !modal" />
    <a-modal
      v-model="modal"
      :title="'Change description for ' + vm.name"
      :ok-text="'Confirm & Save'"
      :confirm-loading="confirmLoading"
      :closable="false"
      @ok="handleSave"
      @cancel="handleCancel">
      <p class="mx-0 px-0 p-1 mb-4">
        <b>Current virtual machine description:</b>
        <br>
        {{ vm.description }}
      </p>
      <p class="mx-0 px-0 p-1 mb-3">
        <b>New virtual machine description:</b>
        <br>
        <a-input placeholder="Enter new description" v-model="newDescription" class="mt-2" />
      </p>
    </a-modal>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VMConfigModal',
  components: {
  },
  props: {
    vm: Object({})
  },
  data () {
    return {
      modal: false,
      newDescription: '',
      confirmLoading: false
    }
  },
  methods: {
    handleSave () {
      if (this.newDescription === '') {
        this.$message.error('New description field can\'t be empty')
        return
      } else if (this.newDescription === this.vm.description) {
        this.$message.error('New description field can\'t be equal to current description')
        return
      }
      this.confirmLoading = true
      const payload = { name: this.vm.name, description: this.newDescription }
      axios({
        method: 'PATCH',
        headers: { Authorization: 'token', 'Content-Type': 'application/json' },
        url: `http://${window.location.hostname}:8080/api/vm`,
        data: payload
      }).then((response) => {
        setTimeout(() => {
          this.confirmLoading = false
          this.modal = false
          this.vm.description = this.newDescription
          this.$message.success(`${this.vm.name} new description: ${this.newDescription}`)
          this.newDescription = ''
        }, 1000)
      }).catch((error) => {
        this.$message.success(`${this.vm.name} update error :(`)
        console.log(error)
      })
    },
    handleCancel () {
      this.newDescription = ''
    }
  }
}
</script>

<style>
.ant-card-body {
  padding-top: 0.7rem !important;
}
</style>
