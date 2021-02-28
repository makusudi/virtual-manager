<template>
  <div>
    <a-icon key="setting" type="setting" @click="modal = !modal" />
    <a-modal
      v-model="modal"
      :title="'Change hardware configuration for ' + vm.name"
      :ok-text="'Confirm & Save'"
      :confirm-loading="confirmLoading"
      :closable="false"
      @ok="handleSave"
      @cancel="handleCancel">
      <div class="d-flex justify-content-between">
        <p class="mx-0 px-0 p-1">
          Current CPU quantity: {{ vm.cpu }}
        </p>
        <p v-if="vm.cpu !== newCPUValue" class="mx-2 p-1 font-weight-bolder rounded text-white" style="background-color: rgb(82, 196, 26)">
          New value: {{ newCPUValue }}
        </p>
      </div>
      <a-slider
        id="cpu_q"
        v-model="newCPUValue"
        :default-value="vm.cpu"
        :min="1"
        :max="16"
        :step="1"
        class="m-0 p-0 mb-4"/>
      <div class="d-flex justify-content-between">
        <p class="mx-0 px-0 p-1">
          Current RAM quantity: {{ vm.ram }} GB
        </p>
        <p v-if="vm.ram !== newRAMValue" class="mx-2 p-1 font-weight-bolder rounded text-white" style="background-color: rgb(82, 196, 26)">
          New value: {{ newRAMValue }}
        </p>
      </div>
      <a-slider
        id="ram_q"
        v-model="newRAMValue"
        :default-value="vm.ram"
        :min="4"
        :max="64"
        :step="4"
        :current="vm.ram"
        class="m-0 p-0 mb-4"/>
      <div class="d-flex justify-content-between">
        <p class="mx-0 px-0 p-1">
          Current HDD quantity: {{ vm.hdd }} GB
        </p>
        <p v-if="vm.hdd !== newHDDValue" class="mx-2 p-1 font-weight-bolder rounded text-white" style="background-color: rgb(82, 196, 26)">
          New value: {{ newHDDValue }}
        </p>
      </div>
      <a-slider
        id="hdd_q"
        v-model="newHDDValue"
        :default-value="vm.hdd"
        :min="12"
        :max="512"
        :step="4"
        class="m-0 p-0 mb-4"/>
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
      newCPUValue: this.vm.cpu,
      newHDDValue: this.vm.hdd,
      newRAMValue: this.vm.ram,
      confirmLoading: false
    }
  },
  methods: {
    handleSave () {
      this.confirmLoading = true
      const payload = { name: this.vm.name }
      if (this.newCPUValue !== this.vm.cpu) {
        payload.cpu = this.newCPUValue
      }
      if (this.newRAMValue !== this.vm.ram) {
        payload.ram = this.newRAMValue
      }
      if (this.newHDDValue !== this.vm.hdd) {
        payload.hdd = this.newHDDValue
      }
      axios({
        method: 'PATCH',
        headers: { Authorization: 'token', 'Content-Type': 'application/json' },
        url: `http://${window.location.hostname}:8080/api/vm`,
        data: payload
      }).then((response) => {
        setTimeout(() => {
          this.confirmLoading = false
          this.modal = false
          if (payload.cpu) {
            this.vm.cpu = this.newCPUValue
            this.$message.success(`${this.vm.name} CPU new quantity: ${this.newCPUValue}`)
          }
          if (payload.hdd) {
            this.vm.hdd = this.newHDDValue
            this.$message.success(`${this.vm.name} HDD new size: ${this.newHDDValue} GB`)
          }
          if (payload.ram) {
            this.vm.ram = this.newRAMValue
            this.$message.success(`${this.vm.name} RAM new size: ${this.newRAMValue} GB`)
          }
        }, 1000)
      }).catch((error) => {
        this.$message.success(`${this.vm.name} update error :(`)
        console.log(error)
      })
    },
    handleCancel () {
      this.newCPUValue = this.vm.cpu
      this.newRAMValue = this.vm.ram
      this.newHDDValue = this.vm.hdd
    }
  }
}
</script>

<style>
.ant-card-body {
  padding-top: 0.7rem !important;
}
</style>
