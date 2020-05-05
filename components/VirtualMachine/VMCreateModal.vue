<template>
  <div>
    <a-button key="1" type="primary" @click="modal = !modal">
      Create
    </a-button>
    <a-modal
      v-model="modal"
      :title="'Creating new virtual machine'"
      :ok-text="'Create'"
      :confirm-loading="confirmLoading"
      :closable="false"
      @ok="handleSave"
      @cancel="handleCancel">
      <a-input placeholder="New virtual machine name" class="mb-4" v-model="vmName" />
      <a-input placeholder="New virtual machine description" class="mb-4" v-model="vmDescription" />
      <p class="m-0 p-0 mb-2" style="font-size: 1rem">
        CPU Quantity: {{ cpuQuantity }}
      </p>
      <a-slider
        id="newcpu_q"
        v-model="cpuQuantity"
        :default-value="1"
        :min="1"
        :max="16"
        :step="1"
        class="m-0 p-0 mb-4"/>
      <p class="m-0 p-0 mb-2" style="font-size: 1rem">
        RAM Quantity: {{ ramQuantity }}
      </p>
      <a-slider
        id="nram_q"
        v-model="ramQuantity"
        :default-value="ramQuantity"
        :min="4"
        :max="64"
        :step="4"
        class="m-0 p-0 mb-4"/>
      <p class="m-0 p-0 mb-2" style="font-size: 1rem">
        HDD Quantity: {{ hddQuantity }}
      </p>
      <a-slider
        id="nhdd_q"
        v-model="hddQuantity"
        :default-value="hddQuantity"
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
  name: 'VMCreateModal',
  components: {
  },
  data () {
    return {
      modal: false,
      vmName: '',
      vmDescription: '',
      cpuQuantity: 1,
      ramQuantity: 4,
      hddQuantity: 12,
      confirmLoading: false
    }
  },
  methods: {
    handleSave () {
      if (this.vmName === '' || this.vmDescription === '') {
        this.$message.error('Name & description fields can\'t be empty')
        return
      }
      this.confirmLoading = true
      const payload = {
        name: this.vmName,
        description: this.vmDescription,
        cpu: this.cpuQuantity,
        ram: this.ramQuantity,
        hdd: this.hddQuantity,
        owner: 'admin'
      }
      axios({
        method: 'POST',
        headers: { Authorization: 'token', 'Content-Type': 'application/json' },
        url: 'http://127.0.0.1:8080/api/new_vm',
        data: payload
      }).then((response) => {
        setTimeout(() => {
          this.confirmLoading = false
          this.modal = false
          this.$message.success(`Virtual machine ${this.vmName} successfully created`)
          this.$emit('addNewVM', {
            name: this.vmName,
            description: this.vmDescription,
            cpu: this.cpuQuantity,
            ram: this.ramQuantity,
            hdd: this.hddQuantity,
            owner: 'admin'
          })
        }, 1000)
      }).catch((error) => {
        this.$message.success('An error occurred :(')
        console.log(error)
      })
    },
    handleCancel () {
    }
  }
}
</script>

<style>
.ant-card-body {
  padding-top: 0.7rem !important;
}
</style>
